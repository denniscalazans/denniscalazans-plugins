/**
 * Pure utility functions for the export-auth CLI script.
 *
 * These functions handle session discovery, parsing, input validation,
 * and storageState validation — all without Playwright dependencies.
 *
 * The actual Playwright calls (connectOverCDP, launchPersistentContext)
 * stay in the thin CLI orchestrator (export-auth.ts).
 */

import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

const SAFE_NAME_PATTERN = /^[a-zA-Z0-9_-]+$/;


/** Session metadata extracted from a playwright-cli .session file. */
export interface SessionInfo {
  userDataDir: string;
  cdpPort: number | undefined;
  socketPath: string | undefined;
}


/** Result of storageState validation. */
export interface ValidationResult {
  valid: boolean;
  reason?: string;
}


/**
 * Validates that app and role names contain only safe characters.
 *
 * Prevents path traversal via crafted input (e.g., `../../etc/passwd`).
 */
export function validateInput(app: string, role: string): void {
  if (!SAFE_NAME_PATTERN.test(app)) {
    throw new Error(`Invalid app name: "${app}". Only alphanumeric, hyphens, and underscores are allowed.`);
  }
  if (!SAFE_NAME_PATTERN.test(role)) {
    throw new Error(`Invalid role name: "${role}". Only alphanumeric, hyphens, and underscores are allowed.`);
  }
}


/**
 * Finds a playwright-cli .session file for the given app and role.
 *
 * Searches all hash directories under the daemon directory.
 * When multiple matches exist, prefers the one whose `workspaceDir` matches `cwd`.
 */
export function findSessionFile(
  daemonDir: string,
  app: string,
  role: string,
  cwd?: string,
): string | null {
  const sessionName = `${app}-${role}.session`;
  const matches: string[] = [];

  if (!existsSync(daemonDir)) return null;

  for (const hashDir of readdirSync(daemonDir)) {
    const candidatePath = join(daemonDir, hashDir, sessionName);
    if (existsSync(candidatePath) && statSync(candidatePath).isFile()) {
      matches.push(candidatePath);
    }
  }

  if (matches.length === 0) return null;
  if (matches.length === 1) return matches[0];

  // Multiple matches — prefer the one whose workspaceDir matches cwd.
  if (cwd) {
    for (const match of matches) {
      try {
        const content = JSON.parse(readFileSync(match, 'utf-8'));
        if (content.workspaceDir === cwd) return match;
      } catch {
        // Skip unparseable files.
      }
    }
  }

  // Fallback: return the first match.
  return matches[0];
}


/**
 * Parses a playwright-cli .session JSON file.
 *
 * Extracts the userDataDir, cdpPort, and socketPath needed to connect
 * to or launch the persistent browser context.
 */
export function parseSessionFile(sessionPath: string): SessionInfo {
  let content: Record<string, unknown>;
  try {
    content = JSON.parse(readFileSync(sessionPath, 'utf-8'));
  } catch {
    throw new Error(`Failed to parse session file: ${sessionPath}`);
  }

  // userDataDir can be nested under `browser` or at the top level.
  const browser = content.browser as Record<string, unknown> | undefined;
  const userDataDir = (browser?.userDataDir ?? content.userDataDir) as string | undefined;

  if (!userDataDir) {
    throw new Error(`userDataDir not found in session file: ${sessionPath}`);
  }

  return {
    userDataDir,
    cdpPort: content.cdpPort as number | undefined,
    socketPath: content.socketPath as string | undefined,
  };
}


/**
 * Constructs the output path for a storageState JSON file.
 */
export function buildAuthOutputPath(app: string, role: string): string {
  return `.agents.tmp/.auth/${app}-${role}.json`;
}


/**
 * Validates that a storageState object is non-trivial.
 *
 * An empty storageState (no cookies, no localStorage origins) likely means
 * the session was never authenticated or has expired.
 */
export function validateStorageState(state: unknown): ValidationResult {
  if (!state || typeof state !== 'object') {
    return { valid: false, reason: 'storageState is null or not an object' };
  }

  const { cookies, origins } = state as {
    cookies?: unknown[];
    origins?: unknown[];
  };

  const hasCookies = Array.isArray(cookies) && cookies.length > 0;
  const hasOrigins = Array.isArray(origins) && origins.length > 0;

  if (!hasCookies && !hasOrigins) {
    return {
      valid: false,
      reason: 'storageState is empty — no cookies or localStorage origins found. The session may not be authenticated.',
    };
  }

  return { valid: true };
}
