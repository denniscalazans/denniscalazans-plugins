/**
 * client.ts — Dictionary Service API client (write operations)
 *
 * Safety guarantees (enforced at TypeScript level + runtime):
 *   - appId is hardcoded as "FFA" — never a parameter
 *   - Write functions only accept env: 'dev'
 *   - Migration targets only 'test' | 'prod'
 *   - Never uses PUT (only PATCH for imports/single-key upserts)
 *   - Auth token is read from process.env.DS_WRITE_TOKEN only
 *
 * Auth setup (token expires ~24h):
 *   1. Open https://dictionary-service.akelius.com, log in
 *   2. DevTools → Network → any API request → copy Authorization header value
 *   3. export DS_WRITE_TOKEN="<bearer-token-value>"
 *
 * Usage:
 *   import { fetchAllKeys, pushKey, importCsv, getMigrationDiff, migrateEnv } from './client';
 */

import * as https from 'https';
import * as http from 'http';

const DS_BASE = 'https://dictionary-service.akelius.com';
const APP_ID = 'FFA' as const;

// ─── Types ────────────────────────────────────────────────────────────────────

export type DsEnv = 'dev' | 'test' | 'stage' | 'prod';
type WriteableEnv = 'dev';
type MigrationTarget = 'test' | 'prod';

export interface FfaTranslations {
  en: string;
  sv: string;
  'en-CA': string;
  en_UK: string;
}

export interface MigrationDiff {
  newTranslations: Record<string, Record<string, string>>;
  updatedTranslations: {
    old: Record<string, Record<string, string>>;
    new: Record<string, Record<string, string>>;
  };
  lnCodes: string[];
}

// ─── HTTP helpers ─────────────────────────────────────────────────────────────

function getWriteToken(): string {
  const token = process.env['DS_WRITE_TOKEN'];
  if (!token) {
    console.error('❌ DS_WRITE_TOKEN is not set.');
    console.error('   To get a token:');
    console.error('     1. Open https://dictionary-service.akelius.com and log in');
    console.error('     2. DevTools → Network → any API request → copy Authorization header value');
    console.error('     3. export DS_WRITE_TOKEN="<value>"');
    throw new Error('DS_WRITE_TOKEN not set');
  }
  return token;
}

interface RequestOptions {
  method: string;
  headers: Record<string, string>;
  body?: string;
}

function request(url: string, options: RequestOptions): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const reqOptions: http.RequestOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || 443,
      path: parsedUrl.pathname + parsedUrl.search,
      method: options.method,
      headers: options.headers,
    };

    const req = https.request(reqOptions, (res) => {
      // Auth failure — print recovery instructions
      if (res.statusCode === 401) {
        reject(
          new Error(
            '401 Unauthorized. Token expired or invalid.\n' +
              '   Recovery: open DS web UI → DevTools → copy fresh Authorization header → re-export DS_WRITE_TOKEN',
          ),
        );
        return;
      }
      if (res.statusCode === 403) {
        reject(
          new Error(
            '403 Forbidden. Your account may lack write permission for this environment.\n' +
              '   Check DS web UI access and confirm env is "dev".',
          ),
        );
        return;
      }
      if (!res.statusCode || res.statusCode < 200 || res.statusCode > 299) {
        let body = '';
        res.on('data', (c: Buffer) => (body += c));
        res.on('end', () => reject(new Error(`HTTP ${res.statusCode}: ${body}`)));
        return;
      }

      let body = '';
      res.on('data', (chunk: Buffer) => (body += chunk));
      res.on('end', () => {
        try {
          resolve(body ? JSON.parse(body) : null);
        } catch {
          resolve(body); // some endpoints return plain text
        }
      });
    });

    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

function getHeaders(contentType = 'application/json'): Record<string, string> {
  const token = getWriteToken();
  return {
    'Content-Type': contentType,
    Authorization: `Bearer ${token}`,
  };
}

// ─── Public API ───────────────────────────────────────────────────────────────

/**
 * Fetch all translation keys for an environment.
 * No auth required — this is a public endpoint.
 */
export async function fetchAllKeys(
  env: DsEnv,
): Promise<Record<string, Record<string, string>>> {
  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/${env}/translations`;
  return new Promise((resolve, reject) => {
    https
      .get(url, (res) => {
        let body = '';
        res.on('data', (c: Buffer) => (body += c));
        res.on('end', () => {
          try {
            resolve(JSON.parse(body) as Record<string, Record<string, string>>);
          } catch (e) {
            reject(new Error(`JSON parse error: ${e}`));
          }
        });
      })
      .on('error', reject);
  });
}

/**
 * Upsert a single translation key to DS dev.
 * Uses PATCH — safe: adds/updates only, never deletes.
 * env is locked to 'dev' at the type level.
 */
export async function pushKey(
  key: string,
  translations: FfaTranslations,
  env: WriteableEnv = 'dev',
): Promise<void> {
  if (env !== 'dev') {
    throw new Error(`Write blocked: env must be 'dev', got '${env as string}'`);
  }

  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/${env}/translations/${encodeURIComponent(key)}`;
  const body = JSON.stringify({
    translation: translations,
    data: {},
  });

  await request(url, {
    method: 'PATCH',
    headers: { ...getHeaders('application/json'), 'Content-Length': Buffer.byteLength(body).toString() },
    body,
  });
}

/**
 * Import a CSV of translations to DS dev.
 * Uses PATCH /translations/transfer — safe: upsert-only, no deletes.
 * env is locked to 'dev' at the type level.
 */
export async function importCsv(csvContent: string, env: WriteableEnv = 'dev'): Promise<void> {
  if (env !== 'dev') {
    throw new Error(`Write blocked: env must be 'dev', got '${env as string}'`);
  }

  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/${env}/translations/transfer`;
  await request(url, {
    method: 'PATCH',
    headers: {
      ...getHeaders('text/plain'),
      'Content-Length': Buffer.byteLength(csvContent).toString(),
    },
    body: csvContent,
  });
}

/**
 * Preview what would change if fromEnv keys were migrated to targetEnv.
 * Calls PATCH /migration-diff — read-only preview, no changes applied.
 */
export async function getMigrationDiff(
  fromEnv: DsEnv,
  targetEnv: MigrationTarget,
): Promise<MigrationDiff> {
  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/${fromEnv}/migration-diff`;
  const body = JSON.stringify({ targetEnv });
  return (await request(url, {
    method: 'PATCH',
    headers: { ...getHeaders('application/json'), 'Content-Length': Buffer.byteLength(body).toString() },
    body,
  })) as MigrationDiff;
}

/**
 * Migrate translations from fromEnv → targetEnv.
 * Only migrates the specified keys (selective, not bulk replacement).
 * Caller MUST call getMigrationDiff and get explicit user confirmation first.
 */
export async function migrateEnv(
  fromEnv: DsEnv,
  targetEnv: MigrationTarget,
  keys: string[],
): Promise<void> {
  if (keys.length === 0) {
    throw new Error('migrateEnv: keys array is empty — nothing to migrate');
  }

  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/${fromEnv}/migrate`;
  const body = JSON.stringify({ targetEnv, migrateApplicationSettings: false, keys });
  await request(url, {
    method: 'PATCH',
    headers: { ...getHeaders('application/json'), 'Content-Length': Buffer.byteLength(body).toString() },
    body,
  });
}
