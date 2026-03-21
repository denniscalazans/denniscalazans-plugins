#!/bin/bash
# Pre-PR hook: checks if plugin content changed without README.md update.
# Exit 0 = allow, Exit 2 = block with message.

# Only check when command is "gh pr create"
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty' 2>/dev/null)
case "$COMMAND" in
  *'gh pr create'*) ;;
  *) exit 0 ;;
esac

# Get changed files vs main
CHANGED=$(git diff main --name-only 2>/dev/null)

# Check if any plugin-related files changed
PLUGIN_CHANGED=$(echo "$CHANGED" | grep -E '^(plugins/|\.claude-plugin/|\.claude/CLAUDE\.md)' || true)

# Check if README was also updated
README_CHANGED=$(echo "$CHANGED" | grep '^README\.md$' || true)

# No plugin changes = no problem
if [ -z "$PLUGIN_CHANGED" ]; then
  exit 0
fi

# Plugin changed AND README changed = good
if [ -n "$README_CHANGED" ]; then
  exit 0
fi

# Plugin changed but README didn't = block
echo "Plugin content changed but README.md was not updated." >&2
echo "" >&2
echo "Changed plugin files:" >&2
echo "$PLUGIN_CHANGED" | sed 's/^/  /' >&2
echo "" >&2
echo "Update README.md to reflect these changes, or confirm it doesn't need updating." >&2
exit 2
