# 상세페이지 (detail-page)

온라인 판매 상품의 **상세페이지 초안과 이미지 시안**을 같은 품질로 반복해서 만드는 Claude Code 플러그인(스킬 1개). 스마트스토어·쿠팡·자사몰·오픈마켓 어디에 올리든, 자체 제작·브랜드·위탁·수입 상품 어느 쪽이든 쓸 수 있다.

고객의 구매 망설임 하나를 먼저 정하고, 그것을 푸는 순서로 11개 섹션을 HTML로 짠 뒤 섹션마다 PNG로 저장한다. 근거 없는 효과 문구를 막는 증거 단계 규칙과 문구·숫자 검사가 함께 들어 있다.

| 단계 | 하는 일 | 도구 |
|---|---|---|
| 초안 | 결정 네 줄(고객·상황 / 원하는 변화 / 구매 망설임 / 선택할 이유)과 증거 단계(1 자료 확인 / 2 실물 확인 / 3 반복 시험·판매 후)를 채운 초안 md | 초안 양식 · 작성 전략서 |
| 시안 | 템플릿 복사 → 사진 자르기 → HTML에 문구·사진 넣기 → 섹션별 PNG(기본 가로 860px) | `new_product.py` · `image_tools.py` · `render.py` |
| 검사 | 근거 없는 효과 표현·남은 대괄호·확인 필요 표시 검사, 숫자 대조, 디자인 체크리스트 | `check_copy.py` · 디자인 가이드 7장 |
| 기록 | 작업폴더의 결정 기록·레슨런에 남김 | `결정기록.md` 양식 |

## 필요한 환경

- Python 3.9 이상, Google Chrome(렌더에 설치된 Chrome을 쓴다. `playwright install`은 필요 없다)
- 파이썬 패키지: `playwright`, `pillow`
- 인터넷 — 글꼴(Pretendard, G마켓 산스)을 CDN에서 받는다. 글꼴 파일은 이 저장소에 없다. 글꼴 이용 조건은 각 배포처를 확인한다.
- 검증 환경: macOS. Windows·Linux는 실행해 보지 않았다.

```bash
python3 -m pip install playwright pillow
python3 -c "import playwright, PIL; print('ok')"
```

`externally-managed-environment` 오류가 나면(Homebrew Python 등) 가상환경을 만든다. 이때는 아래 명령의 `python3`를 `~/.venvs/detail-page/bin/python`으로 바꿔 실행한다.

```bash
python3 -m venv ~/.venvs/detail-page && ~/.venvs/detail-page/bin/pip install playwright pillow
```

## 설치

이 플러그인은 **`detail-page` 스킬 하나만** 추가한다. 다른 스킬·MCP·훅은 설치되지 않는다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install detail-page@mochunab-tools --scope user
```

설치 후 Claude Code를 다시 시작하거나 호스트 안내에 따라 플러그인을 다시 로드한다. 스킬 폴더는 `~/.claude/plugins/cache/mochunab-tools/detail-page/<버전>/skills/detail-page`에 생긴다.

### 스킬 폴더만 설치 (Codex 등)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cp -R agent-toolkit/plugins/detail-page/skills/detail-page ~/.claude/skills/detail-page   # Codex는 ~/.codex/skills/
```

같은 이름의 스킬이 이미 있으면 먼저 비교·백업한다. 플러그인과 수동 설치를 동시에 하지 않는다.

### 예전 `consignment-content` 플러그인에서 옮겨 오는 경우

`consignment-content` 0.1.0에 들어 있던 `detail-page`가 이 독립 플러그인으로 옮겨졌다(0.2.0부터 빠짐). 위 명령으로 `detail-page@mochunab-tools`를 설치한다. 규칙은 같고, 위탁판매 전용 표현을 일반 표현으로 바꿨다. 증거 단계 이름이 `1 공급처 자료 → 1 자료 확인`, `2 샘플 확인 → 2 실물 확인`으로 바뀌었다.

## 사용 예

작업 폴더(예: `~/콘텐츠`)를 정하고 에이전트에게 쉬운 말로 요청한다.

- "이 상품 상세페이지 초안부터 만들어줘. 작업폴더는 ~/콘텐츠, 스마트스토어용이야" → 결정 네 줄·증거 단계를 채운 초안 작성
- "초안 끝났으니 시안 만들어줘" → 템플릿 복사 → 사진 자르기 → `render.py`로 PNG → 문구 검사
- "쿠팡에도 올릴 거라 그 폭으로도 뽑아줘" → 채널 권장 폭을 확인하고 `render.py --width <폭>`으로 다시 저장

직접 폴더만 만들 때(`<스킬>`은 설치된 스킬 폴더):

```bash
python3 "<스킬>/scripts/new_product.py" detail "내상품" --root "$HOME/콘텐츠"
```

만들어지는 구조:

```text
콘텐츠/상세페이지/
├── 결정기록.md                     ← 작업별 결정·과정·실수(없을 때만 양식으로 만듦)
├── 레슨런.md                       ← (직접 만듦) 이 작업폴더에서 새로 배운 교훈
├── 디자인_템플릿/                  ← (선택) 직접 고친 템플릿. 있으면 스킬 템플릿보다 먼저 씀
└── 상품별초안/<상품명>/
    ├── 상세페이지_초안.md          ← 무엇을 말할지(양식 자동 배치)
    └── 상세페이지_디자인/          ← 상세페이지.html · style.css · render.py · 도구/ · 원본이미지/ · 이미지/
```

## 설정값

| 항목 | 기본값 | 바꾸는 법 |
|---|---|---|
| 이미지 폭 | 가로 860px(스마트스토어 상세 권장 폭) | `render.py --width <폭>`. 레이아웃은 860px 기준 그대로, 이미지만 비율대로 바뀜. 다른 채널의 권장 폭은 그 채널 판매자 안내에서 확인한다(이 저장소는 채널별 폭을 검증하지 않았다) |
| 금지어 | 최상급·보장·효과·인증·특허·차단·절감 등 기본 목록 | `check_copy.py --extra 단어,단어`로 상품군 표현 추가(예: 문·창호 `외풍,난방비,방음`). 인증서·시험성적서가 있는 단어만 `--allow`로 뺌 |
| 강조색 | 노랑 `#FFE04A` + 주석 빨강 `#EB3B26` | 상품 폴더의 `style.css` 맨 위 `--yellow`·`--red` |
| 템플릿 | 스킬의 `assets/template/` | `<작업폴더>/상세페이지/디자인_템플릿/`에 복사해 고치면 이후 새 상품에 그것을 씀 |

## 동작 확인

샘플을 임시 위치로 복사해서 렌더한다(설치 폴더에 `출력/`을 만들지 않기 위해).

```bash
SK="<설치된 detail-page 스킬 폴더>"
cp -R "$SK/assets/sample/현관문_시안예시" "$TMPDIR/dp-sample"
python3 "$TMPDIR/dp-sample/render.py"
```

섹션별 `s01-첫화면.png: 860x…`처럼 한 줄씩 출력되고 `$TMPDIR/dp-sample/출력/`에 PNG가 생기면 정상이다(사진은 자리표시 이미지로 렌더됨). 폭 변경은 `python3 "$TMPDIR/dp-sample/render.py" --width 1000` → `1000x…`로 출력된다.

새 상품 흐름 확인:

```bash
python3 "$SK/scripts/new_product.py" detail "테스트상품" --root "$TMPDIR/dp-work"
python3 "$TMPDIR/dp-work/상세페이지/상품별초안/테스트상품/상세페이지_디자인/도구/check_copy.py" "$TMPDIR/dp-work/상세페이지/상품별초안/테스트상품/상세페이지_디자인/상세페이지.html"
```

빈 템플릿은 `효과 표현: 0건`, 남은 대괄호·확인 필요 표시가 여러 개로 나오는 것이 정상이다(채우기 전 상태).

## 오류 해결

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: playwright` | 위 「필요한 환경」의 설치 명령. 가상환경이면 그 환경의 python으로 실행 |
| `Chromium distribution 'chrome' is not found` | Google Chrome을 설치한다 |
| 아무 출력 없이 끝남 | `cd … &&`로 잇지 말고 `render.py`를 절대경로로 실행한다(동기화 폴더에서 있었던 문제) |
| 글꼴이 기본 글꼴로 나옴 | 인터넷 연결 확인(글꼴 CDN) |
| `이미 있음 — 덮어쓰지 않고 멈춤` | 같은 상품 폴더가 있다. 다른 이름을 쓰거나 기존 폴더를 직접 정리한다 |
| 한글 파일명 비교가 안 맞음 | 자모 분리(NFD) 이름일 수 있다. 완성형(NFC)으로 맞춘 뒤 비교한다 |

## 제한과 주의

- **사진·캡처는 포함하지 않는다.** 샘플 사진은 같은 크기의 자리표시 이미지다. 새 상품에는 직접 찍었거나 제조사·공급처·브랜드가 사용을 허락한 사진만 쓴다. AI로 제품·사용 장면·후기 이미지를 만들지 않는다.
- 샘플(현관문 고무패킹)과 문서 속 숫자(후기 건수·규격)는 2026-10 작성 시점의 조사값이며 다른 상품에 쓰지 않는다.
- `check_copy.py`는 단어 검사일 뿐이다. 광고 심의·표시 의무·법률 판단(식품·화장품·의료기기·건강기능식품 등)을 대신하지 않는다.
- 860px 외의 채널별 권장 폭과 세로 길이 한도는 검증하지 않았다. 올리기 전에 채널 안내를 확인한다.
- 이 규칙이 실제 구매 전환에 도움이 되는지는 검증되지 않았다(전략서 10절의 비교 방법 참고).
- 홍보 영상(30초 세로)까지 만들려면 위탁판매용 [consignment-content](../consignment-content/README.md) 플러그인의 `promo-video`를 함께 설치한다.

## 들어 있는 것

| 위치 | 내용 |
|---|---|
| `skills/detail-page/SKILL.md` | 절차와 게이트(통과 조건) |
| `skills/detail-page/references/` | 작성 전략서(`strategy.md`) · 디자인 가이드 · 레슨런 · 결정 기록 양식 · 템플릿 사용법 |
| `skills/detail-page/assets/template/` | 11개 섹션 뼈대 HTML · 공통 CSS · PNG 렌더러 · 사진 도구 · 문구 검사 · 초안 양식 |
| `skills/detail-page/assets/sample/` | 현관문 고무패킹 시안 v2(완성 예시, 사진은 자리표시 이미지) |
| `skills/detail-page/scripts/new_product.py` | 새 상품 폴더·양식 만들기 |

## 출처와 라이선스

mochunab이 위탁판매 상품 상세페이지 작업(2026-10)에서 만든 스킬·문서·템플릿을 판매 방식·채널에 상관없이 쓰도록 고친 것이며 [MIT](../../LICENSE)로 배포한다. 글꼴·Playwright·Pillow·Chrome은 이 저장소에 포함하지 않으며 각 프로젝트의 이용 조건을 따른다.
