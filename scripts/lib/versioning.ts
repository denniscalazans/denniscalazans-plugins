export interface SemVer {
  major: number;
  minor: number;
  patch: number;
  preRelease: string | undefined;
}

export interface ReleaseResult {
  version: string;
  tag: string;
  autoBumped: boolean;
}

export function parseVersion(v: string): SemVer {
  const base = v.replace(/-.*$/, '');
  const preMatch = v.match(/-(.+)$/);
  const [major, minor, patch] = base.split('.').map(Number);
  return { major, minor, patch, preRelease: preMatch?.[1] };
}

export function isHigher(a: SemVer, b: SemVer): boolean {
  if (a.major !== b.major) return a.major > b.major;
  if (a.minor !== b.minor) return a.minor > b.minor;
  return a.patch > b.patch;
}

export function stripPreRelease(version: string): string {
  return version.replace(/-.*$/, '');
}

export function computePrVersion(mainVersion: string, prNumber: number): string {
  const { major, minor, patch } = parseVersion(mainVersion);
  return `${major}.${minor}.${patch + 1}-pr.${prNumber}`;
}

export function computeReleaseVersion(
  pluginName: string,
  currentVersion: string,
  tagExists: (tag: string) => boolean,
): ReleaseResult | null {
  let releaseVersion = stripPreRelease(currentVersion);
  let tag = `${pluginName}-v${releaseVersion}`;

  if (!tagExists(tag)) {
    return { version: releaseVersion, tag, autoBumped: false };
  }

  const { major, minor, patch } = parseVersion(releaseVersion);
  releaseVersion = `${major}.${minor}.${patch + 1}`;
  tag = `${pluginName}-v${releaseVersion}`;

  if (tagExists(tag)) {
    return null;
  }

  return { version: releaseVersion, tag, autoBumped: true };
}
