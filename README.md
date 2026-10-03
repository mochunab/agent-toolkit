# Agent Toolkit

mochunab이 공유하는 에이전트 스킬·플러그인·MCP 서버·가이드 모음. 각 항목의 폴더에서 설치와 사용 안내를 확인한다.

## 도구별 안내

| 항목 | 하는 일 | 설치·사용 문서 |
|---|---|---|
| Aside Browser | 로그인된 브라우저 조작, MCP 연결 확인, exec/repl 선택 | [Aside README](skills/aside-browser/README.md) |
| Semble MCP | BM25·의미 검색 기반 코드 검색과 의존 관계 분석 | [Semble README](mcp/semble/README.md) |
| Mac 앱 테스트 자동화 | Android ADB·iPhone 미러링·Computer Use 설치와 테스트 절차 | [Mac 앱 테스트 README](guides/mac-app-test-automation/README.md) |

공유할 때는 필요한 항목의 폴더 주소만 전달하면 된다. 도구는 각각 설치한다. Mac 앱 테스트 자동화는 실행 코드가 없는 문서 묶음이며, 필요한 외부 도구는 해당 가이드를 따라 설치한다. `agent-toolkit@mochunab-tools` 플러그인이 제공하는 것은 **Aside 스킬**이며, MCP 서버를 한꺼번에 설치하지 않는다.

## 공유 주소

- [Aside Browser 안내](https://github.com/mochunab/agent-toolkit/tree/main/skills/aside-browser)
- [Semble MCP 안내](https://github.com/mochunab/agent-toolkit/tree/main/mcp/semble)
- [Mac 앱 테스트 자동화 안내](https://github.com/mochunab/agent-toolkit/tree/main/guides/mac-app-test-automation)

## 라이선스

이 저장소의 직접 제작 지침·가이드·템플릿·Semble MCP 래퍼·패키징은 [MIT](LICENSE)로 배포한다. 외부 도구는 각 프로젝트에서 설치하며, 출처와 이용 조건은 해당 자산의 README를 따른다.

개인 인증 파일, 브라우저 데이터와 사용자별 MCP 설정은 포함하지 않는다.
