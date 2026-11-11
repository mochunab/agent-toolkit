# 위탁판매 콘텐츠 (홍보영상)

위탁·스마트스토어 상품의 **30초 홍보 영상**을 같은 품질로 반복해서 만드는 Claude Code 플러그인. 가이드·레슨런·템플릿·보조 스크립트가 들어 있고, 스킬이 절차와 게이트(통과 조건)를 잡아 준다.

| 스킬 | 하는 일 | 핵심 도구 |
|---|---|---|
| `promo-video` | 상세페이지를 8장면·30초 세로(9:16) 영상으로 압축한다. 음악·효과음을 직접 합성해 외부 음원이 없다 | `new_product.py` · `render.py` · `audio.py` · `check_leftovers.py` |

영상은 상세페이지 시안이 끝난 상품에서 시작한다(대본이 상세페이지). 상세페이지 스킬은 0.2.0부터 판매 방식에 상관없이 쓰는 독립 플러그인 [detail-page](../detail-page/README.md)로 옮겼다. **영상을 만들려면 `detail-page` 플러그인을 함께 설치한다.** 문구·증거 규칙은 그쪽 `references/strategy.md`가 우선한다.

## 필요한 환경

- Python 3.9 이상, Google Chrome, `ffmpeg`
- `pip install playwright pillow numpy` (렌더는 `channel="chrome"`으로 설치된 Chrome을 쓴다)
- 인터넷 — 글꼴(Pretendard, G마켓 산스)을 CDN에서 받는다. 이 저장소에 글꼴 파일은 없다. 글꼴 이용 조건은 각 배포처를 확인한다.

## 설치

이 플러그인은 **`promo-video` 스킬만** 추가한다. 다른 스킬·MCP는 설치되지 않는다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install detail-page@mochunab-tools --scope user
claude plugin install consignment-content@mochunab-tools --scope user
```

설치 후 호스트 안내에 따라 플러그인을 다시 로드한다. 0.1.0에서 업데이트하면 `detail-page` 스킬이 이 플러그인에서 빠지므로 위 두 번째 줄로 따로 설치한다.

### 스킬 폴더만 설치 (Codex 등)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cp -R agent-toolkit/plugins/detail-page/skills/detail-page ~/.claude/skills/detail-page   # Codex는 ~/.codex/skills/
cp -R agent-toolkit/plugins/consignment-content/skills/promo-video ~/.claude/skills/promo-video
```

같은 이름의 스킬이 이미 있으면 먼저 비교·백업한다. 플러그인과 수동 설치를 동시에 하지 않는다.

## 사용 예

작업 폴더(예: `~/콘텐츠`)를 정하고 에이전트에게 쉬운 말로 요청한다.

- "이 상품 30초 홍보영상 만들어줘" → 상세페이지 시안을 장면별 문구·근거 표로 줄이고 렌더

직접 폴더만 만들 때(`<promo-video>`는 설치된 promo-video 스킬 폴더):

```bash
python3 "<promo-video>/scripts/new_product.py" video "내상품" --root "$HOME/콘텐츠"
```

만들어지는 구조:

```text
콘텐츠/
├── 상세페이지/상품별초안/<상품명>/    ← detail-page 스킬이 만든 상세페이지(영상의 대본)
└── 홍보영상/상품별/<상품명>/
    ├── 홍보영상_계획.md              ← 구성표·문구 근거(양식 자동 배치)
    └── 소스/                         ← 영상.html · timing.py · audio.py · render.py · assets/
```

## 들어 있는 것

| 위치 | 내용 |
|---|---|
| `skills/promo-video/references/` | 제작 가이드 · 레슨런 · 결정 기록 양식 · 인계서(시작 양식) · 템플릿 사용법 |
| `skills/promo-video/assets/template/` | 8장면 영상 소스(화면·시간표·소리 합성·렌더러) · 계획 양식 |
| `skills/promo-video/assets/sample/` | 현관문 영상 구성표·문구 근거 예시 |

## 동작 확인

1. `python3 "<promo-video>/assets/template/render.py" stills 3.4,6.9,13.9 "$TMPDIR/stills"` → 정지 화면 3장이 만들어지면 정상(이 명령은 출력을 임시 폴더에만 쓴다).
2. `python3 "<promo-video>/scripts/check_leftovers.py" "<promo-video>/assets/template/영상.html"` → 템플릿은 현관문 내용 그대로라 흔적이 나오는 것이 정상이다(새 상품 소스에서 0건이 되어야 한다).

## 제한과 주의

- **공개본은 2026-10 시점의 스냅샷**이다. 원본 문서는 작성자의 작업 폴더에서 계속 바뀌므로 이 저장소와 달라질 수 있다.
- **공급처 사진·경쟁사 캡처·영상 파일은 포함하지 않는다.** 템플릿의 사진은 같은 크기의 자리표시 이미지다. 공급처 이미지를 영상으로 가공해도 되는지는 공급사에 따로 확인한다.
- 예시의 숫자(후기 건수, 규격)는 2026-10 작성 시점의 조사값이며 다른 상품에 쓰지 않는다.
- 영상의 소리는 AI가 들을 수 없어 측정값으로만 검증됐다. 게시 전에 직접 들어 확인한다. 올릴 곳(스마트스토어·릴스·쇼츠)의 영상 규격은 검증하지 않았다.
- 스킬은 Playwright로 Chrome을 띄워 렌더하므로 `playwright`·Chrome이 없으면 렌더 단계에서 멈춘다.

## 출처와 라이선스

스킬·스크립트·문서·템플릿은 mochunab이 작성했으며 [MIT](../../LICENSE)로 배포한다. 글꼴·Playwright·Pillow·numpy·ffmpeg는 이 저장소에 포함하지 않으며 각 프로젝트의 이용 조건을 따른다.
