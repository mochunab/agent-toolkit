# Agent Toolkit

mochunab이 공유하는 에이전트 스킬·플러그인·MCP 서버 모음. 각 항목의 폴더에서 설치와 사용 안내를 확인한다.

## 도구별 안내

| 항목 | 하는 일 | 설치·사용 문서 |
|---|---|---|
| Aside Browser | 로그인된 브라우저 조작, MCP 연결 확인, exec/repl 선택 | [Aside README](skills/aside-browser/README.md) |
| Semble MCP | BM25·의미 검색 기반 코드 검색과 의존 관계 분석 | [Semble README](mcp/semble/README.md) |

공유할 때는 필요한 항목의 폴더 주소만 전달하면 된다. 두 항목은 각각 설치한다. `agent-toolkit@mochunab-tools` 플러그인이 제공하는 것은 **Aside 스킬**이며, MCP 서버를 한꺼번에 설치하지 않는다.

## 공유 주소

- [Aside Browser 안내](https://github.com/mochunab/agent-toolkit/tree/main/skills/aside-browser)
- [Semble MCP 안내](https://github.com/mochunab/agent-toolkit/tree/main/mcp/semble)

## 라이선스

이 저장소의 직접 제작 지침·Semble MCP 래퍼·패키징은 [MIT](LICENSE)로 배포한다. 외부 Aside 앱·CLI·MCP 서버와 `semble_rs` 검색 엔진은 각 프로젝트에서 설치한다.

개인 인증 파일, 브라우저 데이터와 사용자별 MCP 설정은 포함하지 않는다.
