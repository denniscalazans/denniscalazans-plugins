// Regression tests for plugins/cli/skills/cli-as-skill/assets/preflight.sh.
//
// The script ships with __PLACEHOLDER__ values; cli-as-skill substitutes them
// with real values from the bundle's metadata.json at packaging time. We test
// the post-substitution form by reading the asset, doing the substitution
// ourselves, and writing it to a temp file before invoking it.
//
// We avoid depending on host-installed CLIs by routing the version probe
// through a PATH-prepended directory that contains a fake `probe` shell script.

import { describe, it, before, after } from "node:test";
import { spawnSync } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync, mkdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const here = dirname(fileURLToPath(import.meta.url));
const assetPath = resolve(here, "..", "assets", "preflight.sh");

let workDir: string;
let fakeBinDir: string;
let installedScriptPath: string;
let originalPath: string | undefined;

interface RunResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

function buildScript(opts: {
  tool: string;
  builtFor: string;
  versionCmd: string;
  researchedOn: string;
}): string {
  let body = readFileSync(assetPath, "utf8");
  body = body
    .replace(/__TOOL__/g, opts.tool)
    .replace(/__BUILT_FOR__/g, opts.builtFor)
    .replace(/__VERSION_CMD__/g, opts.versionCmd)
    .replace(/__RESEARCHED_ON__/g, opts.researchedOn);
  return body;
}

function writeFakeProbe(version: string): void {
  // The script does `command -v $TOOL`, so we put a real file on PATH that
  // echoes a version line. It also gets called via $VERSION_CMD; that path
  // runs the real command tokens, so we set VERSION_CMD to "probe --version"
  // (no shell metacharacters, no spaces) to keep the contract.
  const probe = join(fakeBinDir, "probe");
  writeFileSync(
    probe,
    `#!/usr/bin/env bash
echo "probe version ${version}"
`,
    { mode: 0o755 },
  );
}

function runInstalledScript(): RunResult {
  const result = spawnSync("bash", [installedScriptPath], {
    env: { ...process.env, PATH: `${fakeBinDir}:${originalPath ?? ""}` },
    encoding: "utf8",
  });
  return {
    exitCode: result.status ?? -1,
    stdout: (result.stdout ?? "").trim(),
    stderr: (result.stderr ?? "").trim(),
  };
}

function readDrift(stdout: string): string | null {
  const m = stdout.match(/^DRIFT=([A-Z_]+)/m);
  return m ? m[1] : null;
}

function install(opts: {
  builtFor: string;
  researchedOn: string;
  installedVersion: string;
  versionCmd?: string;
}): void {
  writeFakeProbe(opts.installedVersion);
  const body = buildScript({
    tool: "probe",
    builtFor: opts.builtFor,
    versionCmd: opts.versionCmd ?? "probe --version",
    researchedOn: opts.researchedOn,
  });
  writeFileSync(installedScriptPath, body);
}

before(() => {
  originalPath = process.env.PATH;
  workDir = mkdtempSync(join(tmpdir(), "preflight-spec-"));
  fakeBinDir = join(workDir, "bin");
  mkdirSync(fakeBinDir, { recursive: true });
  installedScriptPath = join(workDir, "preflight.sh");
});

after(() => {
  rmSync(workDir, { recursive: true, force: true });
});

describe("preflight.sh — version-drift classification", () => {
  it("EXACT: installed version equals built-for", () => {
    install({ builtFor: "2.50.1", researchedOn: "2026-06-14", installedVersion: "2.50.1" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "EXACT");
    assert.equal(r.exitCode, 0);
  });

  it("PATCH: installed is newer patch on same major.minor", () => {
    install({ builtFor: "1.2.4", researchedOn: "2026-06-14", installedVersion: "1.2.5" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "PATCH");
  });

  it("PATCH: installed is newer patch, single-digit minor", () => {
    install({ builtFor: "2.0.0", researchedOn: "2026-06-14", installedVersion: "2.0.9" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "PATCH");
  });

  // Regression for Codex P2 review comment: same major.minor but older patch
  // (e.g. built for 1.2.4, installed 1.2.3) used to fall through to PATCH
  // because the script only compared the minor component. It must be
  // classified as DOWNGRADE — older patches can lack flags the skill relies on.
  it("DOWNGRADE (P2 regression): installed is older patch on same major.minor", () => {
    install({ builtFor: "1.2.4", researchedOn: "2026-06-14", installedVersion: "1.2.3" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "DOWNGRADE");
    assert.match(r.stderr, /DOWNGRADE/);
  });

  it("DOWNGRADE: installed is older minor on same major", () => {
    install({ builtFor: "1.3.0", researchedOn: "2026-06-14", installedVersion: "1.2.9" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "DOWNGRADE");
  });

  it("MINOR: installed is newer minor on same major", () => {
    install({ builtFor: "1.2.4", researchedOn: "2026-06-14", installedVersion: "1.3.0" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "MINOR");
  });

  it("MAJOR: installed is different major (newer)", () => {
    install({ builtFor: "1.9.9", researchedOn: "2026-06-14", installedVersion: "2.0.0" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "MAJOR");
    assert.match(r.stderr, /MAJOR/);
  });

  it("MAJOR: installed is different major (older)", () => {
    install({ builtFor: "2.0.0", researchedOn: "2026-06-14", installedVersion: "1.9.9" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "MAJOR");
  });

  it("UNKNOWN: version string has no parseable number", () => {
    install({ builtFor: "1.0.0", researchedOn: "2026-06-14", installedVersion: "nope" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "UNKNOWN");
  });

  it("handles two-segment versions (no patch) — built 1.2, installed 1.2.0", () => {
    // The script pads with `.0.0`, so BUILT_FOR=1.2 should normalize to 1.2.0.
    install({ builtFor: "1.2", researchedOn: "2026-06-14", installedVersion: "1.2.0" });
    const r = runInstalledScript();
    assert.equal(readDrift(r.stdout), "EXACT");
  });
});

describe("preflight.sh — STALE research-age check", () => {
  it("does not flag STALE for recent research", () => {
    install({ builtFor: "2.50.1", researchedOn: "2026-06-14", installedVersion: "2.50.1" });
    const r = runInstalledScript();
    assert.match(r.stdout, /STALE=no/);
  });

  it("flags STALE=yes for research older than 180 days", () => {
    // 2024-01-01 is well over 180 days before today (2026-06-14).
    install({ builtFor: "2.50.1", researchedOn: "2024-01-01", installedVersion: "2.50.1" });
    const r = runInstalledScript();
    assert.match(r.stdout, /STALE=yes/);
    assert.match(r.stderr, /research is \d+d old/);
  });
});
