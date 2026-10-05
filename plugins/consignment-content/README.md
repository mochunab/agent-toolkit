# 위탁판매 콘텐츠 (상세페이지 + 홍보영상)

위탁·스마트스토어 상품의 **상세페이지 이미지 시안**과 **30초 홍보 영상**을 같은 품질로 반복해서 만드는 Claude Code 플러그인. 가이드·레슨런·템플릿·보조 스크립트가 들어 있고, 두 스킬이 절차와 게이트(통과 조건)를 잡아 준다. 새 상품이 생길 때마다 같은 문서를 다시 읽고 같은 복사·검사를 반복하지 않게 하는 것이 목적이다.

| 스킬 | 하는 일 | 핵심 도구 |
|---|---|---|
| `detail-page` | 구매 망설임 하나를 정하고 11개 섹션 시안을 만든다. 사진 자르기 → HTML → 섹션별 PNG(860px) → 문구·숫자 검사 | `new_product.py` · `render.py` · `image_tools.py` · `check_copy.py` |
| `promo-video` | 상세페이지를 8장면·30초 세로(9:16) 영상으로 압축한다. 음악·효과음을 직접 합성해 외부 음원이 없다 | `new_product.py` · `render.py` · `audio.py` · `check_leftovers.py` |

영상은 상세페이지 시안이 끝난 상품에서 시작한다(대본이 상세페이지). **두 스킬을 함께 설치한다.**

## 필요한 환경

- Python 3.9 이상, Google Chrome
- `pip install playwright pillow numpy` (렌더는 `channel="chrome"`으로 설치된 Chrome을 쓴다)
- 영상: `ffmpeg`
- 인터넷 — 글꼴(Pretendard, G마켓 산스)을 CDN에서 받는다. 이 저장소에 글꼴 파일은 없다. 글꼴 이용 조건은 각 배포처를 확인한다.

## 설치

이 플러그인은 **이 두 스킬만** 추가한다. 다른 스킬·MCP는 설치되지 않는다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install consignment-content@mochunab-tools --scope user
```

설치 후 호스트 안내에 따라 플러그인을 다시 로드한다.

### 스킬 폴더만 설치 (Codex 등)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cp -R agent-toolkit/plugins/consignment-content/skills/detail-page ~/.claude/skills/detail-page   # Codex는 ~/.codex/skills/
cp -R agent-toolkit/plugins/consignment-content/skills/promo-video ~/.claude/skills/promo-video
```

같은 이름의 스킬이 이미 있으면 먼저 비교·백업한다. 플러그인과 수동 설치를 동시에 하지 않는다.

## 사용 예

작업 폴더(예: `~/콘텐츠`)를 정하고 에이전트에게 쉬운 말로 요청한다.

- "이 상품 상세페이지 초안부터 만들어줘" → 전략서 기준으로 결정 네 줄·증거 단계를 채우고 초안 작성
- "초안 끝났으니 시안 만들어줘" → 템플릿 복사 → 사진 자르기 → `render.py`로 PNG → 문구 검사
- "이 상품 30초 홍보영상 만들어줘" → 상세페이지 시안을 장면별 문구·근거 표로 줄이고 렌더

직접 폴더만 만들 때(`<스킬>`은 설치된 스킬 폴더):

```bash
python3 "<스킬>/scripts/new_product.py" detail "내상품" --root "$HOME/콘텐츠"
python3 "<스킬>/scripts/new_product.py" video  "내상품" --root "$HOME/콘텐츠"
```

만들어지는 구조:

```text
콘텐츠/
├── 상세페이지/상품별초안/<상품명>/
│   ├── 상세페이지_초안.md            ← 무엇을 말할지(양식 자동 배치)
│   └── 상세페이지_디자인/            ← 템플릿 복사본: 상세페이지.html · style.css · render.py · 도구/ · 원본이미지/ · 이미지/
└── 홍보영상/상품별/<상품명>/
    ├── 홍보영상_계획.md              ← 구성표·문구 근거(양식 자동 배치)
    └── 소스/                         ← 영상.html · timing.py · audio.py · render.py · assets/
```

## 들어 있는 것

| 위치 | 내용 |
|---|---|
| `skills/detail-page/references/` | 작성 전략서(`strategy.md`) · 디자인 가이드 · 레슨런 · 결정 기록 양식 · 템플릿 사용법 |
| `skills/detail-page/assets/template/` | 11개 섹션 뼈대 HTML · 공통 CSS · PNG 렌더러 · 사진 도구 · 문구 검사 · 초안 양식 |
| `skills/detail-page/assets/sample/` | **현관문 고무패킹 시안 v2**(완성 예시, 공급처 사진은 자리표시 이미지) |
| `skills/promo-video/references/` | 제작 가이드 · 레슨런 · 결정 기록 양식 · 인계서(시작 양식) · 템플릿 사용법 |
| `skills/promo-video/assets/template/` | 8장면 영상 소스(화면·시간표·소리 합성·렌더러) · 계획 양식 |
| `skills/promo-video/assets/sample/` | 현관문 영상 구성표·문구 근거 예시 |

## 동작 확인

1. 샘플 폴더를 임시 위치로 복사한 뒤 거기서 렌더한다(설치 폴더에 `출력/`을 만들지 않기 위해): `cp -R "<detail-page>/assets/sample/현관문_시안예시" "$TMPDIR/sample" && python3 "$TMPDIR/sample/render.py"` → 섹션별 `가로 860 x 높이`가 한 줄씩 출력되고 `$TMPDIR/sample/출력/`에 PNG가 생기면 정상(자리표시 이미지로 렌더됨).
2. `python3 "<promo-video>/assets/template/render.py" stills 3.4,6.9,13.9 "$TMPDIR/stills"` → 정지 화면 3장이 만들어지면 정상(이 명령은 출력을 임시 폴더에만 쓴다).
3. `python3 "<promo-video>/scripts/check_leftovers.py" "<promo-video>/assets/template/영상.html"` → 템플릿은 현관문 내용 그대로라 흔적이 나오는 것이 정상이다(새 상품 소스에서 0건이 되어야 한다).

## 제한과 주의

- **공개본은 2026-10 시점의 스냅샷**이다. 원본 문서는 작성자의 작업 폴더에서 계속 바뀌므로 이 저장소와 달라질 수 있다.
- **공급처 사진·경쟁사 캡처·영상 파일은 포함하지 않는다.** 샘플과 템플릿의 사진은 같은 크기의 자리표시 이미지다. 새 상품에는 공급처가 사용을 허용한 사진이나 직접 찍은 사진만 쓴다. 공급처 이미지를 영상으로 가공해도 되는지는 공급사에 따로 확인한다.
- 샘플·예시의 숫자(후기 건수, 규격)는 2026-10 작성 시점의 조사값이며 다른 상품에 쓰지 않는다. 후기 분류 수치는 원문 대조 전 요약 기준이었던 항목이 있다(문서에 표시).
- 문구 규칙은 “근거 없는 효과 문구 금지”를 기본으로 한다. 상품군에 맞는 금지어는 `check_copy.py --extra`로 더한다. 법적 표시·광고 심의 판단은 이 도구가 대신하지 않는다.
- 영상의 소리는 AI가 들을 수 없어 측정값으로만 검증됐다. 게시 전에 직접 들어 확인한다. 올릴 곳(스마트스토어·릴스·쇼츠)의 영상 규격은 검증하지 않았다.
- 스킬은 Playwright로 Chrome을 띄워 렌더하므로 `playwright`·Chrome이 없으면 렌더 단계에서 멈춘다.
- 실제 구매 전환에 도움이 되는지는 검증되지 않았다(전략서 10절의 비교 방법 참고).

## 출처와 라이선스

스킬·스크립트·문서·템플릿은 mochunab이 작성했으며 [MIT](../../LICENSE)로 배포한다. 글꼴·Playwright·Pillow·numpy·ffmpeg는 이 저장소에 포함하지 않으며 각 프로젝트의 이용 조건을 따른다.
