# Aside Browser

Claude Code·Codex가 로그인된 Aside 브라우저를 사용할 때 읽는 커뮤니티 스킬. MCP 연결을 확인하고, 연결이 없으면 설치·연결을 진행할지 먼저 물으며, 작업에 맞게 `exec` 또는 `repl`을 선택한다.

이 문서만으로 Aside 스킬 설치와 MCP 연결을 준비할 수 있다. 실제 에이전트 지침은 [SKILL.md](SKILL.md)에 있다.

## 무엇이 설치되는가

| 구성 | 역할 | 이 스킬 설치에 포함? |
|---|---|---|
| Aside 스킬 | 에이전트가 읽는 연결 확인·사용 지침 | 포함 |
| Aside Browser 앱 | 실제 웹사이트를 여는 브라우저 | 별도 설치 |
| Aside CLI | 터미널 명령과 MCP 서버 실행 | 별도 설치 |
| Aside MCP 연결 | 코딩 에이전트에서 Aside 도구 호출 | 별도 등록 |

**플러그인을 설치하면 스킬만 추가된다.** 앱·CLI·MCP 연결은 아래 절차를 따른다. 이 페이지의 설치 명령은 Aside 스킬용이다.

## 스킬 설치

사용할 코딩 에이전트가 설치돼 있어야 한다. Claude Code는 아래 두 방식 중 하나를 선택하고, Codex는 스킬 폴더 설치 방식을 사용한다.

### Claude Code 플러그인

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install agent-toolkit@mochunab-tools --scope user
```

설치 완료 메시지를 확인하고 호스트 안내에 따라 플러그인을 다시 로드한다. 이후 "Aside로 현재 페이지를 확인해줘"처럼 요청한다.

MCP가 연결되지 않았으면 스킬이 다음처럼 묻는다.

> Aside MCP가 연결되어 있지 않습니다. CLI 설치 여부를 확인하고 MCP 설치·연결을 진행할까요?

사용자가 동의하면 CLI 설치 여부와 기존 MCP 설정을 확인해 연결한다. 이미 설치 작업을 승인했거나 CLI만 쓰기로 선택했다면 같은 질문을 반복하지 않는다.

### 스킬 폴더만 설치

플러그인 대신 스킬 파일을 직접 관리하거나 Codex에서 사용할 때 선택한다.

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cd agent-toolkit
```

이미 저장소를 받았다면 기존 폴더를 사용한다. `skills/aside-browser` 폴더를 사용하는 에이전트의 스킬 디렉터리로 복사한다.

| 에이전트 | 기본 설치 위치 |
|---|---|
| Claude Code | `~/.claude/skills/aside-browser/` |
| Codex | `~/.codex/skills/aside-browser/` |

기존 같은 이름의 스킬이 있으면 먼저 내용을 비교하고 백업한다. 복사 후 해당 폴더에 `SKILL.md`가 있는지 확인하고 호스트의 스킬을 다시 로드한다. 플러그인 설치와 수동 설치를 동시에 하지 않는다.

## Aside 앱과 CLI 준비

1. [Aside 공식 개발 문서](https://docs.aside.com/help/developers)에 따라 운영체제에 맞는 Aside Browser 앱과 CLI를 설치한다.
2. Aside 앱을 실행하고 사용할 사이트에 로그인한다.
3. 터미널에서 CLI가 실행되는지 확인한다.

```bash
command -v aside
aside --version
aside guide
```

CLI 경로·버전·사용 안내가 출력되면 준비된 상태다. macOS의 공식 CLI 설치 명령은 다음과 같다.

```bash
curl -fsSL https://releases.aside.com/install.sh | bash
```

다른 운영체제는 공식 문서의 해당 설치 방법을 따른다. `aside guide`를 지원하지 않는 구버전이거나 업데이트가 안내되면 `aside --update` 후 가이드를 다시 읽는다.

## Claude Code에 MCP 연결

스킬에 설치·연결을 승인해 맡기거나 다음 명령으로 직접 등록한다.

1. 기존 서버가 등록돼 있는지 확인한다.

```bash
claude mcp list
```

`aside`가 이미 있으면 `claude mcp get aside`로 설정을 확인하고 연결 오류를 진단한다. 앱이 꺼져 있거나 서버가 비활성화된 경우 재설치보다 실행·재연결이 먼저다.

2. 등록이 없고 `command -v aside`가 실행 경로를 반환하면 연결을 추가한다.

```bash
claude mcp add --scope user aside -- "$(command -v aside)" mcp
```

MCP는 CLI의 `aside mcp`를 실행한다. 브라우저를 두 번 설치하는 구조가 아니다. 다른 MCP 클라이언트는 [JSON 설정 예시](https://github.com/mochunab/agent-toolkit/blob/main/mcp/aside.example.json)를 참고하고, `command`에는 그 환경에서 실행 가능한 Aside CLI 경로를 사용한다.

3. 호스트에서 MCP를 다시 연결하거나 재시작하고 Aside 도구가 나타나는지 확인한다.

`exec`·`repl` 등 도구 이름의 접두사는 호스트에 따라 다를 수 있다. 설정 파일에 항목이 생겼다는 사실만으로 연결 성공을 판단하지 않는다. 실제로 "Aside로 현재 페이지 제목을 확인해줘"를 실행해 결과가 돌아오는지 확인한다.

## exec와 repl 사용

| 방식 | 누가 다음 행동을 결정하나 | 잘 맞는 작업 |
|---|---|---|
| `exec` | Aside 내부 AI 에이전트 | 낯선 사이트 탐색, 여러 사이트 조사, 목표를 주고 위임하는 작업 |
| `repl` | 호출하는 에이전트가 작성한 JavaScript | 확인된 버튼·필드 조작, 필요한 값 추출, DOM·화면 확인 |

탐색과 판단을 위임할 필요가 있으면 `exec`, 대상과 순서가 확인됐으면 `repl`을 선택한다. `exec`는 별도 AI의 판단 과정이 있어 단순 조작에도 사용하면 시간이 더 들 수 있다.

요청 예시:

```text
Aside exec로 여러 쇼핑몰에서 이 상품 가격을 비교해줘.

Aside repl로 현재 페이지 표의 상품명과 가격만 추출해줘.

탐색과 판단이 필요하면 Aside exec를 쓰고,
조작 대상이 확인되면 repl로 필요한 값만 추출해줘.
```

CLI·MCP는 연결 방식이고 `exec`·`repl`은 작업 방식이다. `Agent Tabs`는 에이전트가 쓰는 탭을 모아 표시하는 그룹이므로, 그 그룹만 보고 호출 방식을 구분할 수 없다.

## 문제 해결

| 증상 | 확인할 것 |
|---|---|
| Aside 도구가 안 보임 | MCP 등록·활성화, 호스트 재연결 또는 재시작 |
| CLI를 찾지 못함 | `command -v aside`, PATH, MCP 설정의 실행 경로 |
| 브라우저에 연결하지 못함 | Aside 앱 실행 여부와 연결 대상 호스트 |
| 조작 API가 예상과 다름 | 설치된 버전의 `aside guide`, `aside guide repl` |
| 공식 스킬 재설치 후 지침이 달라짐 | 같은 이름의 사용자 스킬이 교체됐는지 비교 |

스킬은 에이전트가 따르는 지침이며 호스트의 권한 정책을 대신하지 않는다. 이미 승인된 작업은 진행하되, 추가 게시·전송·결제·삭제는 별도 승인 없이 확장하지 않는다.

## 출처와 라이선스

작성일: 2026-10-04. 이 저장소는 연결 확인·라우팅 지침과 스킬 패키징을 제공한다. Aside Browser·CLI·MCP 서버 자체는 Aside가 개발한다.

- [Aside 공식 개발 문서](https://docs.aside.com/help/developers)
- [Agent Tabs 공식 변경 내역](https://docs.aside.com/changelog/native#improved-agent-tabs)
- [커뮤니티 스킬 지침](SKILL.md)
- [MIT 라이선스](https://github.com/mochunab/agent-toolkit/blob/main/LICENSE)

지원 API는 설치된 CLI의 가이드를 우선 확인한다. 공식 스킬을 다시 설치하면 사용자 스킬 사본이 교체될 수 있다.
