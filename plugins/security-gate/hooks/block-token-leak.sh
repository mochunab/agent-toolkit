#!/usr/bin/env bash
# PreToolUse(Bash): block commands that carry a secret in plain text.
# A secret passed as a command argument stays in the transcript and shell history.
# The matched value is never printed back; only the pattern name is shown.
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "security-gate: jq not found, secret-leak check skipped. Install jq to enable it." >&2
  exit 1
fi
cmd=$(jq -r '.tool_input.command // ""')

# name|ERE. Minimum lengths keep false positives down.
secret_patterns=(
  "Slack token|xox[bpasr]-[0-9A-Za-z-]{10,}"
  "Slack app token|xapp-[0-9A-Za-z-]{10,}"
  "AWS access key|(AKIA|ASIA)[0-9A-Z]{12,}"
  "GitHub token|gh[posru]_[A-Za-z0-9]{20,}"
  "GitHub fine-grained PAT|github_pat_[A-Za-z0-9_]{20,}"
  "sk- secret key|(^|[^A-Za-z0-9_])sk-[A-Za-z0-9_-]{16,}"
  "Google API key|AIza[0-9A-Za-z_-]{30,}"
  "Google OAuth token|ya29\.[0-9A-Za-z_-]{20,}"
  "JWT|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
  "Bearer token|[Bb]earer [A-Za-z0-9._~+/-]{20,}"
  "Private key|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)

for entry in "${secret_patterns[@]}"; do
  name=${entry%%|*}
  pattern=${entry#*|}
  if printf '%s' "$cmd" | grep -qE -- "$pattern"; then
    cat >&2 <<EOF
BLOCKED: plain-text secret in command (${name}).
Do not pass secrets as command arguments; they remain in the transcript and shell history.
Instead:
  - store the value in an OS keychain or secret manager without typing it into a command
    (macOS: security add-generic-password -w "\$(pbpaste)", Linux: secret-tool/pass,
     cloud: Secrets Manager / Parameter Store)
  - read it at run time into a variable, e.g. TOKEN="\$(security find-generic-password -s SVC -a ACCT -w)"
  - never display or return secrets received from tool output; pipe them straight into storage
EOF
    exit 2
  fi
done
exit 0
