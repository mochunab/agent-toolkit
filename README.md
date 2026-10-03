# Agent Toolkit

mochunab이 사용하는 에이전트 워크플로를 공유하는 저장소. 스킬, Claude Code 플러그인, MCP 연결 안내를 필요한 것만 골라 설치한다.

첫 공개에는 **Aside 브라우저 스킬**을 담았다. 사용자별 경로·계정 상태·키가 필요한 자산과 외부에서 설치한 스킬은 묶어서 복사하지 않았다. 다른 직접 제작 자산은 공개용 정리를 마친 뒤 추가한다.

## 포함 항목

| 항목 | 역할 |
|---|---|
| [aside-browser](skills/aside-browser/SKILL.md) | MCP 연결 확인, 설치·연결 승인 요청, exec/repl 선택, 현재 CLI 가이드 확인 |
| Claude Code 플러그인 | 위 스킬을 마켓플레이스로 설치 |
| [Aside MCP 안내](mcp/README.md) | CLI 설치와 MCP 등록을 구분하고 실제 연결 확인 |
| [Semble MCP](https://github.com/mochunab/semble-mcp) | 별도 공개 저장소에서 관리하는 코드 검색 MCP 래퍼 |

## Claude Code: 플러그인으로 설치

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install agent-toolkit@mochunab-tools --scope user
```

설치 후 호스트 안내에 따라 플러그인을 다시 로드한다. "Aside로 현재 페이지를 확인해줘"처럼 요청한다. Aside MCP가 없으면 스킬이 설치·연결 진행 여부를 묻는다.

플러그인은 스킬만 제공한다. Aside 앱·CLI 설치와 MCP 연결은 [연결 안내](mcp/README.md)를 따른다.

## 스킬만 설치

```bash
git clone https://github.com/mochunab/agent-toolkit.git
```

Claude Code는 `skills/aside-browser` 폴더를 `~/.claude/skills/aside-browser`로 복사한다. Codex는 해당 환경의 사용자 스킬 디렉터리(기본 `~/.codex/skills/aside-browser`)에 복사한다. 기존 같은 이름의 스킬이 있으면 먼저 내용을 비교하고 백업한다. 플러그인 설치와 수동 설치 중 하나를 선택해 중복 등록을 피한다.

이 스킬은 MCP가 연결되지 않았을 때 다음처럼 묻도록 한다.

> Aside MCP가 연결되어 있지 않습니다. CLI 설치 여부를 확인하고 MCP 설치·연결을 진행할까요?

사용자가 이미 연결 작업을 승인했거나 CLI만 쓰기로 선택했다면 같은 확인을 반복하지 않는다. 스킬은 에이전트 지침이며 강제 실행 정책을 대신하지 않는다.

## exec와 repl

- `exec`: 목표를 자연어로 전달하고 Aside 내부 에이전트에게 탐색과 판단을 위임한다.
- `repl`: 호출하는 에이전트가 JavaScript로 페이지를 읽고 직접 조작한다.
- CLI·MCP는 연결 방식, `Agent Tabs`는 탭 표시 그룹이다.

특정 버튼·필드·데이터가 확인돼 있으면 `repl`, 탐색과 판단을 위임할 필요가 있으면 `exec`를 선택한다. 지원 API는 설치된 CLI의 `aside guide`와 `aside guide repl`에서 확인한다.

## 출처와 라이선스

이 저장소의 연결 확인·라우팅 지침과 패키징은 커뮤니티 제작물이며 MIT로 배포한다. Aside Browser·CLI·MCP 서버 자체를 포함하거나 재배포하지 않는다. [공식 개발 문서](https://docs.aside.com/help/developers)를 따른다. Aside 공식 스킬을 다시 설치하면 사용자 스킬 사본이 교체될 수 있다.

## 검증

```bash
claude plugin validate .
```

공개본에는 개인 인증 파일, 실행 로그, 브라우저 데이터, 사용자별 MCP 설정을 넣지 않는다.
