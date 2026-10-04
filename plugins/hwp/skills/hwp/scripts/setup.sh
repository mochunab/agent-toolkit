#!/usr/bin/env bash
# python-hwpx venv 부트스트랩 (idempotent). 이미 있으면 즉시 반환.
set -euo pipefail
VENV="${HWPX_VENV:-$HOME/hwpx-env}"
PY="$VENV/bin/python"

if [ -x "$PY" ] && "$PY" -c "import hwpx" 2>/dev/null; then
  echo "$PY"
  exit 0
fi

# python-hwpx는 Python>=3.10 필요. macOS 기본 python3는 3.9인 경우가 많아 명시적으로 탐색.
BOOT=""
for c in python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    BOOT="$c"; break
  fi
done
if [ -z "$BOOT" ]; then
  echo "python>=3.10 없음 — 'brew install python@3.13' 후 재시도" >&2
  exit 1
fi

# 기존 venv의 python 링크가 끊긴 경우(인터프리터 삭제·업그레이드)에만 비우고 재생성
CLEAR=""
if [ -L "$PY" ] && [ ! -e "$PY" ]; then CLEAR="--clear"; fi
"$BOOT" -m venv $CLEAR "$VENV" >/dev/null 2>&1 || true
"$VENV/bin/pip" install -q --upgrade pip >/dev/null 2>&1 || true
"$VENV/bin/pip" install -q 'python-hwpx>=6.3' >&2

"$PY" -c "import hwpx" || { echo "python-hwpx 설치 실패" >&2; exit 1; }
echo "$PY"
