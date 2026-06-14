#!/usr/bin/env bash
# Version-drift preflight for a generated <tool>-cli skill.
# Read-only. Loud banner to stderr, machine-readable verdict to stdout. Never mutates.
#
# cli-as-skill fills the four __PLACEHOLDER__ values when generating a per-tool skill.
set -euo pipefail

TOOL="__TOOL__"                    # e.g. gh
BUILT_FOR="__BUILT_FOR__"          # e.g. 2.62.0
VERSION_CMD="__VERSION_CMD__"      # e.g. "gh --version" (simple, space-delimited; runs unquoted)
RESEARCHED_ON="__RESEARCHED_ON__"  # e.g. 2026-06-14
STALE_DAYS=180                     # warn if research is older than this

emit()   { echo "DRIFT=$1 BUILT_FOR=$BUILT_FOR INSTALLED=${2:-unknown} RESEARCHED_ON=$RESEARCHED_ON STALE=$STALE AGE_DAYS=$AGE"; }
banner() { echo "$1" >&2; }

# Compute research age in days (best-effort; supports GNU and BSD/macOS date). 0 if undeterminable.
research_age_days() {
  local now then_ts
  now=$(date +%s 2>/dev/null) || { echo 0; return; }
  then_ts=$(date -d "$RESEARCHED_ON" +%s 2>/dev/null \
            || date -j -f "%Y-%m-%d" "$RESEARCHED_ON" +%s 2>/dev/null) || { echo 0; return; }
  echo $(( (now - then_ts) / 86400 ))
}
AGE=$(research_age_days)
STALE=no
if [ "$AGE" -gt "$STALE_DAYS" ] 2>/dev/null; then
  STALE=yes
  banner "⚠️  [$TOOL] research is ${AGE}d old (> ${STALE_DAYS}d) — flags may have changed silently. Verify against --help before mutating; consider /cli:learn-a-cli $TOOL."
fi

if ! command -v "$TOOL" >/dev/null 2>&1; then
  banner "🛑 [$TOOL] NOT INSTALLED — this skill cannot operate. Install $TOOL first; do not improvise commands."
  emit MISSING; exit 3
fi

RAW="$($VERSION_CMD 2>&1 | head -1)"
INSTALLED="$(printf '%s' "$RAW" | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || true)"

if [ -z "$INSTALLED" ]; then
  banner "⚠️  [$TOOL] version not parseable ('$RAW'). Built for $BUILT_FOR. Cannot verify drift — check flags against --help before mutating."
  emit UNKNOWN "$RAW"; exit 0
fi

# Split on '.' and keep only the first 3 components, defaulting missing pieces to 0.
# (The previous form appended '.0.0' and read into 3 vars, which left malformed
# trailing segments like '4.0.0' that broke integer comparisons.)
parse_version() {
  local v="$1" parts
  IFS='.' read -r -a parts <<<"${v}.0.0.0"
  printf '%s %s %s\n' "${parts[0]:-0}" "${parts[1]:-0}" "${parts[2]:-0}"
}
read -r bM bm bp < <(parse_version "$BUILT_FOR")
read -r iM im ip < <(parse_version "$INSTALLED")
BUILT_FOR_CANON="$bM.$bm.$bp"

if [ "$INSTALLED" = "$BUILT_FOR" ] || [ "$iM.$im.$ip" = "$BUILT_FOR_CANON" ]; then
  emit EXACT "$INSTALLED"; exit 0
elif [ "$iM" -ne "$bM" ]; then
  banner "🛑 [$TOOL] MAJOR VERSION DRIFT — skill built for $BUILT_FOR, installed is $INSTALLED.
   Flags/commands may have been renamed or removed. Do NOT auto-run mutating or destructive commands.
   Re-run  /cli:learn-a-cli $TOOL  to refresh, or confirm 'proceed anyway' to continue at your own risk."
  emit MAJOR "$INSTALLED"; exit 0
elif [ "$im" -lt "$bm" ] && [ "$iM" -eq "$bM" ]; then
  banner "⚠️  [$TOOL] DOWNGRADE — installed $INSTALLED is older than built-for $BUILT_FOR. Flags this skill relies on may not exist yet; verify against --help before mutating."
  emit DOWNGRADE "$INSTALLED"; exit 0
elif [ "$ip" -lt "$bp" ] && [ "$iM" -eq "$bM" ] && [ "$im" -eq "$bm" ]; then
  banner "⚠️  [$TOOL] DOWNGRADE — installed $INSTALLED is older than built-for $BUILT_FOR (same major.minor, older patch). Flags this skill relies on may not exist yet; verify against --help before mutating."
  emit DOWNGRADE "$INSTALLED"; exit 0
elif [ "$im" -ne "$bm" ]; then
  banner "⚠️  [$TOOL] MINOR drift — built for $BUILT_FOR, installed $INSTALLED. New flags may exist; old ones usually still work. Re-check --help for any flag that errors."
  emit MINOR "$INSTALLED"; exit 0
else
  echo "ℹ️  [$TOOL] patch drift ($BUILT_FOR → $INSTALLED) — contract stable." >&2
  emit PATCH "$INSTALLED"; exit 0
fi
