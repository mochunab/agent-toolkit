# HWP (.hwpx) 스킬

한컴 오피스 없이 한글 문서(`.hwpx`)를 **읽고 · 마크다운에서 만들고 · 관공서 양식에 값을 채우는** Claude Code 플러그인. 순수 파이썬([python-hwpx](https://pypi.org/project/python-hwpx/))이라 macOS·Linux·CI에서 그대로 동작한다. 에이전트 지침은 [SKILL.md](skills/hwp/SKILL.md)에 있다.

| 모드 | 하는 일 | 스크립트 |
|---|---|---|
| A. 읽기 | 구조 요약, 표 격자, 텍스트 검색, 마크다운 변환 | `hwpx_read.py` |
| B. 신규 작성 | 마크다운 → hwpx (제목·문단·표·목록·인용·구분선) | `hwpx_build.py` |
| C. 양식 채우기 | 원본 서식·이미지·표 구조를 보존한 채 값 주입, 저장 후 자동 검증 | `hwpx_fill.py` |

## 필요한 환경

- Python 3.10 이상 (macOS 기본 `python3`가 3.9이면 `brew install python@3.13`)
- 인터넷 (첫 실행 때 `python-hwpx>=6.3` 설치)
- 대상은 **`.hwpx`** 뿐. 구 바이너리 `.hwp`는 지원하지 않는다.

## 설치

이 플러그인은 **hwp 스킬만** 추가한다. 다른 스킬·MCP는 설치되지 않는다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install hwp@mochunab-tools --scope user
```

설치 후 호스트 안내에 따라 플러그인을 다시 로드한다.

### 스킬 폴더만 설치 (Codex 등)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cp -R agent-toolkit/plugins/hwp/skills/hwp ~/.claude/skills/hwp   # Codex는 ~/.codex/skills/hwp
```

같은 이름의 스킬이 이미 있으면 먼저 비교·백업한다. 플러그인과 수동 설치를 동시에 하지 않는다.

## 사용 예

에이전트에게 쉬운 말로 요청한다.

- "이 hwpx 뭐라고 써있는지 요약해줘" → 읽기
- "이 마크다운을 hwpx로 뽑아줘" → 신규 작성
- "이 신청서 양식에 상호·대표자 채워줘" → 양식 채우기 (dry-run으로 변경 전/후를 먼저 보여주고, 확인 후 저장)

직접 실행할 때는 `HWP_DIR`을 스킬 폴더로 지정한다.

```bash
HWP_DIR=~/.claude/skills/hwp
PY=$("$HWP_DIR"/scripts/setup.sh)                 # ~/hwpx-env 자동 생성 (HWPX_VENV로 경로 변경)
$PY "$HWP_DIR"/scripts/hwpx_build.py 원고.md -o 결과.hwpx --title "제목"
$PY "$HWP_DIR"/scripts/hwpx_read.py 결과.hwpx --md
```

## 동작 확인

위 build → read 예시로 만든 파일이 `--grep`으로 읽히면 정상이다. 양식 채우기는 `--apply` 때 표·문단 개수 대조, 스키마 검증, 치환 잔존 검사를 자동 수행하며 하나라도 어긋나면 종료 코드 1을 반환한다.

## 제한과 주의

- 마크다운의 `**굵게**`·`` `코드` ``·링크는 서식 없이 텍스트만 남는다.
- 이미지 삽입·머리말·페이지 설정 등은 스크립트 범위 밖이다. [references/api.md](skills/hwp/references/api.md)의 API 치트시트로 직접 코딩한다.
- 라벨 매칭은 내부 공백을 보존한다. 자간용 공백이 있는 양식(`상      호`)은 `--labels` 출력을 그대로 복사해야 한다.
- 양식 원본은 덮어쓰지 않는다 (출력은 항상 새 경로).
- 사업계획서·신청서에는 주민번호·주소 등 개인정보가 들어간다. 채운 결과물을 git·공개 URL에 올리지 않는다.
- 실제 관공서 양식으로 왕복 검증(표 32개·문단 314개·이미지 포함 엔트리 전량 보존)했으나, 모든 양식·한컴 버전에서의 호환은 보증하지 않는다. 제출 전 한글 프로그램에서 열어 확인한다.

## 출처와 라이선스

스킬·스크립트·문서는 mochunab이 작성했으며 [MIT](../../LICENSE)로 배포한다. 문서 처리는 외부 라이브러리 `python-hwpx`(별도 설치, 해당 프로젝트 라이선스 따름)를 사용하며 이 저장소에 포함하지 않는다. HWPX는 한컴의 OWPML 표준 형식이다.
