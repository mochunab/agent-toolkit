# Plain Writer (쉬운 글쓰기)

한국어 글을 **결론 먼저, 짧은 문장, 구체적인 말**로 쓰거나 고친다.
업무 메시지·이메일·보고서부터 모임 공지·집주인 문의·환불 요청까지 같은 원칙을 쓴다.
에이전트 지침은 [SKILL.md](skills/plain-writer/SKILL.md)에 있다.

| 모드 | 하는 일 |
|---|---|
| draft (새로 쓰기) | 메모·키워드를 받아 매체에 맞는 글로 쓴다 |
| polish (고치기) | 이미 쓴 글을 고치고, 바꾼 점과 이유를 표로 보여 준다 |

| 파일 | 내용 |
|---|---|
| [rules.md](skills/plain-writer/references/rules.md) | 글쓰기 규칙 (분량·문장·용어·흐린 말·모호어·구조) |
| [channels.md](skills/plain-writer/references/channels.md) | 매체별 형식 (메신저·이메일·문의·공지·문서) |
| [checklist.md](skills/plain-writer/references/checklist.md) | 퇴고 점검표 |

## 필요한 환경

- Claude Code 또는 스킬 폴더를 읽는 에이전트 (Codex 등)
- 외부 프로그램·패키지·인터넷 연결이 필요 없다. 문서만으로 동작한다.

## 설치

이 플러그인은 **plain-writer 스킬만** 추가한다. 다른 스킬·MCP는 설치되지 않는다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install plain-writer@mochunab-tools --scope user
```

설치 후 호스트 안내에 따라 플러그인을 다시 로드한다.

### 스킬 폴더만 설치 (Codex 등)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cp -R agent-toolkit/plugins/plain-writer/skills/plain-writer ~/.claude/skills/plain-writer   # Codex는 ~/.codex/skills/plain-writer
```

같은 이름의 스킬이 이미 있으면 먼저 비교·백업한다. 플러그인과 수동 설치를 동시에 하지 않는다.

## 사용 예

에이전트에게 평소 말로 요청한다.

- "모임 장소 바뀐 거 단톡방 공지로 써줘. 6/1 일요일 2시, 신촌역 ○○카페" → 새로 쓰기
- "이 환불 문의 메일 짧고 분명하게 고쳐줘" + 원문 → 고치기 (수정본 + 바꾼 점 표)
- "팀장님께 보낼 보고 메일인데 읽기 쉽게 다듬어줘" → 고치기

받는 사람·매체·목적·기한 중 모르는 것이 있으면 한 번에 묶어 한 번만 묻는다.
없는 날짜·금액·이름은 지어내지 않는다.

## 동작 확인

설치 후 아래처럼 요청한다.

```
/plain-writer polish 다름이 아니라 혹시 가능하시다면 이번 주 안에 최대한 빨리 회신 부탁드려도 될까요?
```

수정본이 직접 부탁 한 문장으로 바뀌면 정상이다. "이번 주 안에"는 날짜와 요일로 바뀐다.
"바꾼 점" 표에 관용구 삭제와 모호어 수정이 나와야 한다.

## 제한

- 한국어 글 전용이다. 영어 글·코드 주석·커밋 메시지에는 쓰지 않는다.
- 소설·시·광고 카피처럼 표현 자체가 목적인 글에는 맞지 않는다.
- 문체만 다듬는다. 사실이 맞는지는 확인하지 않는다. 내용 검증은 쓰는 사람의 몫이다.
- 문장 길이(60자)와 분량 기준은 권장값이다. 법률 문서·계약서처럼 정확성이 우선인 글은 분량 기준을 느슨하게 적용한다.

## 출처와 라이선스

스킬·규칙·점검표는 mochunab이 작성했다. [MIT](../../LICENSE)로 배포한다.
