#!/usr/bin/env npx tsx
/**
 * Export storageState from an existing playwright-cli persistent session.
 *
 * Bridges browser-login sessions with navigate flows and other Playwright consumers.
 * The output JSON contains cookies and localStorage — treat it as sensitive.
 *
 * Usage:
 *   npx tsx export-auth.ts <app> <role>
 *
 * Examples:
 *   npx tsx export-auth.ts my-app admin
 *   npx tsx export-auth.ts ffa manager
 *
 * Output:
 *   .agents.tmp/.auth/<app>-<role>.json
 *
 * SECURITY: This script ONLY prints the output file path.
 * It NEVER prints storageState contents to stdout.
 */

import { mkdirSync, writeFileSync, renameSync } from 'fs';
import { dirname, join } from 'path';
import { homedir } from 'os';
import { connect as netConnect, type Socket } from 'net';
import {
  validateInput,
  findSessionFile,
  parseSessionFile,
  buildAuthOutputPath,
  validateStorageState,
} from './export-auth-utils';


const DAEMON_DIR = join(homedir(), 'Library', 'Caches', 'ms-playwright', 'daemon');


/**
 * Checks if a UNIX socket is alive by attempting a connection.
 *
 * Returns true if the socket responds within the timeout.
 */
async function isSocketAlive(socketPath: string, timeout = 2000): Promise<boolean> {
  return new Promise((resolve) => {
    if (!socketPath) {
      resolve(false);
      return;
    }
    let socket: Socket | undefined;
    const timer = setTimeout(() => {
      socket?.destroy();
      resolve(false);
    }, timeout);

    socket = netConnect(socketPath, () => {
      clearTimeout(timer);
      socket?.destroy();
      resolve(true);
    });
    socket.on('error', () => {
      clearTimeout(timer);
      resolve(false);
    });
  });
}


/**
 * Extracts storageState by connecting to a running browser via CDP.
 *
 * Used when playwright-cli already has the session open (avoids profile lock).
 */
async function extractViaCDP(cdpPort: number): Promise<string> {
  const { chromium } = await import('playwright');
  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${cdpPort}`);
  try {
    const contexts = browser.contexts();
    if (contexts.length === 0) {
      throw new Error('No browser contexts found via CDP. Is the session still active?');
    }
    return await contexts[0].storageState() as unknown as string;
  } finally {
    // Disconnect without closing — the browser belongs to playwright-cli.
    await browser.close();
  }
}


/**
 * Extracts storageState by launching headless against an idle profile.
 *
 * Used when the browser is NOT currently running (no profile lock conflict).
 */
async function extractViaLaunch(userDataDir: string): Promise<string> {
  const { chromium } = await import('playwright');
  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: true,
    timeout: 15_000,
  });
  try {
    return await context.storageState() as unknown as string;
  } finally {
    await context.close();
  }
}


async function main(): Promise<void> {
  const [app, role] = process.argv.slice(2);

  if (!app || !role) {
    console.error('Usage: npx tsx export-auth.ts <app> <role>');
    console.error('Example: npx tsx export-auth.ts my-app admin');
    process.exit(1);
  }

  // 1. Input validation (path traversal prevention).
  validateInput(app, role);

  // 2. Dependency guard.
  try {
    await import('playwright');
  } catch {
    console.error('Error: playwright not found.');
    console.error('Install it: npm i -D playwright');
    process.exit(1);
  }

  // 3. Session discovery.
  const sessionPath = findSessionFile(DAEMON_DIR, app, role, process.cwd());
  if (!sessionPath) {
    console.error(`No session found for "${app}-${role}".`);
    console.error(`Expected: ${DAEMON_DIR}/*/${app}-${role}.session`);
    console.error('');
    console.error('Create one first:');
    console.error(`  /dc:browser-login as ${role} on ${app}`);
    process.exit(1);
  }

  // 4. Parse session file.
  const session = parseSessionFile(sessionPath);

  // 5. Detect browser state and extract storageState.
  const browserRunning = session.socketPath
    ? await isSocketAlive(session.socketPath)
    : false;

  let storageState: unknown;
  if (browserRunning && session.cdpPort) {
    storageState = await extractViaCDP(session.cdpPort);
  } else {
    storageState = await extractViaLaunch(session.userDataDir);
  }

  // 6. Write output atomically with restrictive permissions.
  const outputPath = buildAuthOutputPath(app, role);
  const outputDir = dirname(outputPath);
  mkdirSync(outputDir, { recursive: true, mode: 0o700 });

  const tmpPath = `${outputPath}.tmp.${process.pid}`;
  const data = typeof storageState === 'string'
    ? storageState
    : JSON.stringify(storageState, null, 2);
  writeFileSync(tmpPath, data, { mode: 0o600 });
  renameSync(tmpPath, outputPath);

  // 7. Post-export validation (informational warning, not a hard error).
  const parsed = typeof storageState === 'string'
    ? JSON.parse(storageState)
    : storageState;
  const validation = validateStorageState(parsed);
  if (!validation.valid) {
    console.error(`Warning: ${validation.reason}`);
    console.error('The auth file was written, but the session may not be authenticated.');
    console.error(`Re-run: /dc:browser-login as ${role} on ${app}`);
  }

  // 8. Print ONLY the file path (NEVER the contents — credential leakage prevention).
  console.log(outputPath);
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
