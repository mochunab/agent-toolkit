#!/usr/bin/env bash
# PreToolUse(Edit|Write|MultiEdit): block direct edits to secrets, keys, lockfiles and .git.
# Lockfiles should change through the package manager, not by hand.
# Example env files (.env.example, .env.sample, .env.template) stay editable.
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "security-gate: jq not found, protected-file check skipped. Install jq to enable it." >&2
  exit 1
fi
input=$(cat)

# Claude Code sends tool_input.file_path. Codex sends an apply_patch body with
# "*** Update File: <path>" lines, so both shapes are read.
files=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // ""')
if [ -z "$files" ]; then
  files=$(printf '%s' "$input" \
    | jq -r '.tool_input.command // .tool_input.input // ""' \
    | sed -nE "s/^\\*\\*\\* (Update|Add|Delete) File: //p")
fi

protected=(
  "(^|/)\.env($|\.)"
  "(^|/)\.envrc$"
  "(^|/)\.git/"
  "(^|/)package-lock\.json$"
  "(^|/)yarn\.lock$"
  "(^|/)pnpm-lock\.yaml$"
  "\.pem$"
  "\.key$"
  "(^|/)secrets/"
)
allowed="(^|/)\.env\.(example|sample|template)$"

while IFS= read -r file; do
  [ -z "$file" ] && continue
  printf '%s' "$file" | grep -qiE "$allowed" && continue
  for pattern in "${protected[@]}"; do
    if printf '%s' "$file" | grep -qiE "$pattern"; then
      echo "BLOCKED: '$file' is a protected file (secrets, keys, lockfiles or .git). Explain why this edit is needed and let the user make it, or use the package manager for lockfiles." >&2
      exit 2
    fi
  done
done <<< "$files"
exit 0
