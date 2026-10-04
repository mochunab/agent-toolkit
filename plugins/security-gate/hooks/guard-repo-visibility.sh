#!/usr/bin/env bash
# PreToolUse(Bash): keep new GitHub repositories private unless publishing is intended.
# Blocks:
#   1) gh repo create ... --public / --visibility public
#   2) gh repo create <name> without --private/--internal (visibility must be explicit)
#   3) gh repo edit ... --visibility public
# Intentional public repo: ALLOW_PUBLIC_REPO=1 <command>
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "security-gate: jq not found, repo visibility check skipped. Install jq to enable it." >&2
  exit 1
fi
cmd=$(jq -r '.tool_input.command // ""')

printf '%s' "$cmd" | grep -qE 'gh +repo +(create|edit)' || exit 0
printf '%s' "$cmd" | grep -qE 'ALLOW_PUBLIC_REPO=1' && exit 0
[ "${ALLOW_PUBLIC_REPO:-}" = "1" ] && exit 0

block() {
  cat >&2 <<EOF
BLOCKED: public repository attempt ($1).
A public repository is visible to every GitHub user.
  - create privately: gh repo create <name> --private ...
  - intentional public release: ALLOW_PUBLIC_REPO=1 <command>
EOF
  exit 2
}

printf '%s' "$cmd" | grep -qE '(--public|--visibility[= ]+public)' && block "--public requested"

if printf '%s' "$cmd" | grep -qE 'gh +repo +create'; then
  printf '%s' "$cmd" | grep -qE '(--private|--internal|--visibility[= ]+(private|internal))' \
    || block "gh repo create without --private"
fi

exit 0
