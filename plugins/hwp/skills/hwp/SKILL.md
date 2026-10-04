---
name: hwp
description: |
  한글 문서(.hwpx)를 한컴 오피스 없이 직접 읽고·만들고·양식 채우는 스킬.
  순수 파이썬(python-hwpx)이라 macOS·CI에서 그대로 돈다. 관공서 제출용 양식
  (위치기반서비스 사업계획서·신고서·각종 신청서)에 값 주입, 마크다운 원고를
  hwpx로 변환, 받은 hwpx를 마크다운으로 읽어 검토하는 3가지 작업을 커버.
  원본 서식·이미지·표 구조는 무손실 보존하고, 저장 후 스키마 검증까지 자동.

  트리거 (자연어):
  - "한글 문서 만들어줘", "hwpx로 뽑아줘", "hwp로 변환", "이 양식 채워줘",
    "hwpx 읽어줘", "한글 파일 내용 보여줘", "사업계획서 작성해줘"(+.hwpx 양식), "/hwp"
  - .hwpx 파일 경로 + 읽기/작성/채우기 의도
  - ⚠️ .hwp(구 바이너리)는 대상 아님 — 한컴 SDK(유료)/pyhwpx(Win) 안내로 라우팅
  - ⚠️ 문서 "내용" 작성 자체가 아니라, 완성된 내용의 hwpx 변환·주입 담당
---

# hwp — 한글 문서(.hwpx) 직접 작성

한컴 오피스 없이 `.hwpx`를 읽고 쓴다. **관공서 양식 채우기**가 주 용도.

> 근거: `python-hwpx` 6.3+ (순수 파이썬, HWPX=ZIP+XML OWPML 표준). 실측 검증 완료 —
> 2.8MB 실제 관공서 양식(표 32개·문단 314개·BinData 22MB) 왕복 후 46개 엔트리 전량 보존.

## 0. 환경 (매 실행 첫 단계)

```bash
HWP_DIR=<이 SKILL.md가 있는 폴더>   # 예: ~/.claude/skills/hwp, 플러그인 설치 시 캐시 내 skills/hwp
PY=$("$HWP_DIR"/scripts/setup.sh)   # ~/hwpx-env 없으면 자동 생성(HWPX_VENV로 변경 가능), 있으면 즉시 반환
```
이후 모든 스크립트는 `$PY`로 실행. 시스템 python3로 실행하면 안 됨.

## 1. 모드 판별

| 사용자가 준 것 | 모드 | 스크립트 |
|---|---|---|
| .hwpx 파일만 + "읽어줘/뭐라고 써있어" | **A. 읽기** | `hwpx_read.py` |
| 내용(md·텍스트·대화) + "한글로 만들어" | **B. 신규작성** | `hwpx_build.py` |
| .hwpx 양식 + 채울 값 | **C. 양식채우기** | `hwpx_fill.py` |

## 2. 모드 A — 읽기

```bash
$PY "$HWP_DIR"/scripts/hwpx_read.py FILE.hwpx              # 구조 요약 + 표 인덱스
$PY "$HWP_DIR"/scripts/hwpx_read.py FILE.hwpx --md         # 본문 마크다운 전문
$PY "$HWP_DIR"/scripts/hwpx_read.py FILE.hwpx --table 5    # 표 5번 격자 전체
$PY "$HWP_DIR"/scripts/hwpx_read.py FILE.hwpx --grep 상호  # 텍스트 검색(표 좌표 포함)
```

**큰 양식은 `--md` 먼저 던지지 말 것** — 수만 자라 컨텍스트 폭발. 요약 → `--grep`으로 좁힘 → 필요한 표만 `--table`.

## 3. 모드 B — 신규작성 (마크다운 → hwpx)

내용을 먼저 **마크다운으로** 쓰고 변환한다. 내용 정리는 먼저 끝내고(필요하면 다른 문서 작성 스킬 활용) 이 단계로 넘김.

```bash
$PY "$HWP_DIR"/scripts/hwpx_build.py 원고.md -o 결과.hwpx --title "문서 제목"
```

지원 문법: `#`~`######` 제목 · 문단 · `| 표 |` · `-` 목록 · `1.` 번호목록 · `>` 인용 · `---` 구분선.
인라인 `**굵게**`·`` `코드` ``·`[링크](url)`는 **텍스트만 남고 서식은 안 붙는다** — 굵게가 중요하면 사용자에게 알리고 한글에서 직접 처리.

## 4. 모드 C — 양식 채우기 (핵심)

관공서 양식은 표 구조가 곧 서식이라 **새로 만들지 말고 원본에 주입**한다.

### 순서
1. `hwpx_read.py FILE.hwpx` → 표 인덱스 확보
2. `hwpx_read.py FILE.hwpx --labels` → **채울 라벨 목록** (관공서 양식 플레이스홀더는 보통 `OOO`, `0000년`, `홍길동`)
3. spec.json 작성 — **`labels` 우선, 좌표(`cells`)는 라벨이 없을 때만**
4. **dry-run으로 before→after 사용자 확인** ← 게이트, 건너뛰기 금지
5. `--apply`

```json
{
  "source": "양식.hwpx",
  "output": "작성본.hwpx",
  "labels":     {"상      호>right": "주식회사 예시", "대  표  자>right": "홍길동"},
  "cells":      [{"table": 5, "row": 1, "col": 1, "text": "주식회사 예시"}],
  "replace":    [{"find": "0000년 0월 0일", "with": "2010년 12월 1일"}],
  "paragraphs": [{"index": 12, "text": "새 문단"}]
}
```

```bash
$PY "$HWP_DIR"/scripts/hwpx_fill.py spec.json           # dry-run
$PY "$HWP_DIR"/scripts/hwpx_fill.py spec.json --apply   # 저장 + 자기검증
```

`--apply`는 저장 후 ①표·문단 개수 대조 ②스키마 검증 ③치환 잔존 검사를 자동 수행. 하나라도 어긋나면 exit 1.

### 라벨 문자열 함정 (제일 자주 깨지는 곳)
매칭은 부분문자열이지만 **내부 공백을 뭉개지 않는다**. 관공서 양식은 자간을 공백으로 맞춰서
`상      호`처럼 들어있다 — `"상호"`로 쓰면 **0건 매칭**.
반드시 `--labels` 출력을 그대로 복사. dry-run에 `⚠️ 매칭 0건`이 뜨면 여기부터 의심.

방향 토큰: `right` `left` `below` `above`, `>`로 체이닝(`"라벨>right>below"`).

### replace 주의
`"OOO"` 같은 짧은 플레이스홀더는 **의도치 않은 곳까지 잡는다**. dry-run 매칭 건수가 예상보다
많으면 `labels`로 전환. 표 셀 치환은 라이브러리 기본 API가 못 하는 영역이라
`hwpx_fill.py`가 직접 처리한다 — 직접 코딩할 땐 `references/api.md` 확인.

## 5. 절대 규칙

- **원본 덮어쓰기 금지** — `output`은 항상 새 경로. 양식 원본은 재사용 자산
- **dry-run 확인 없이 `--apply` 금지** — 표 좌표는 눈으로 못 보니 오주입 위험이 큼
- **클라우드 동기화 폴더(Google Drive 등)의 파일은 로컬에 복사 후 작업** — 동기화 폴더에서 직접 이동·쓰기 금지
- **개인정보 주의** — 사업계획서엔 대표자 주민번호·주소·연락처가 들어간다. 채운 결과물을 git·공개 URL·Slack에 올리지 말 것. 로컬 또는 원래 보관 위치에만 둔다
- 완료 보고 시 **출력 경로 + 검증 결과(표/문단/스키마)** 를 함께 제시

## 6. 함정

| 함정 | 내용 |
|---|---|
| `.hwp` ≠ `.hwpx` | 구 바이너리 .hwp는 이 스킬로 못 씀. 상대가 구버전 한글이면 열지 못함 → 제출 전 확인 |
| 6.0 API 이동 | `save()` 없음 → `save_to_path()`. `export_markdown()` → `text.markdown()`. `list_form_fields()` → `fields.all()`. 7.0에서 구 API 제거 |
| 파일명 `inspect.py` | stdlib `inspect` 섀도잉 → 순환 임포트 크래시. 스크립트명 `hwpx_*` 유지 |
| 표 셀 좌표 | 0-based. 병합 셀은 대표 좌표만 먹음 → `--table N`으로 실제 격자 확인 후 지정 |
| 라벨 공백 | `'상호'` ≠ `'상      호'`. `--labels` 출력 그대로 복사 |
| `text.replace` | 본문 문단만 바꾸고 **표 셀은 안 닿음**. 직접 코딩 시 반드시 표 순회 추가 |
| 파일 크기 감소 | 재압축 결과라 정상. BinData 원본 바이트는 보존됨 |

## 7. 검증 (완료 전 필수)

```bash
$PY "$HWP_DIR"/scripts/hwpx_read.py 결과.hwpx --grep "방금 넣은 값"
```
넣은 값이 실제로 읽히는지 왕복 확인. 스키마 OK만으로는 "값이 들어갔다"의 증거가 안 된다.

## 8. 더 깊이

스크립트가 커버 못 하는 작업(이미지 삽입·머리말·페이지 설정·셀 음영·수식)은
`references/api.md` — 6.x API 치트시트 + 6.0 이동 대조표 + 실측 성질.

## 9. 체이닝

- 내용을 먼저 마크다운으로 정리 → **모드 B**
- 받은 양식 검토 → **모드 A**(읽기) → 값 확정 → **모드 C**
