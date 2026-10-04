# Agent Toolkit

mochunab이 공유하는 에이전트 스킬·플러그인·MCP 서버·가이드 모음. 각 항목의 폴더에서 설치와 사용 안내를 확인한다.

## 도구별 안내

| 항목 | 하는 일 | 설치·사용 문서 |
|---|---|---|
| Aside Browser | 로그인된 브라우저 조작, MCP 연결 확인, exec/repl 선택 | [Aside README](skills/aside-browser/README.md) |
| Semble MCP | BM25·의미 검색 기반 코드 검색과 의존 관계 분석 | [Semble README](mcp/semble/README.md) |
| Mac 앱 테스트 자동화 | Android ADB·iPhone 미러링·Computer Use 설치와 테스트 절차 | [Mac 앱 테스트 README](guides/mac-app-test-automation/README.md) |
| HWP (.hwpx) | 한컴 오피스 없이 hwpx 읽기·마크다운 변환·관공서 양식 채우기 | [HWP README](plugins/hwp/README.md) |
| Security Gate | 증거 기반 보안 점검, 검사 실패·미검증 시 배포 중단, 보안 규칙 자동 적용, 시크릿 노출·공개 저장소·보호 파일 차단 훅 | [Security Gate README](plugins/security-gate/README.md) |

공유할 때는 필요한 항목의 폴더 주소만 전달하면 된다. 도구는 각각 설치한다. Mac 앱 테스트 자동화는 실행 코드가 없는 문서 묶음이며, 필요한 외부 도구는 해당 가이드를 따라 설치한다. `agent-toolkit@mochunab-tools` 플러그인이 제공하는 것은 **Aside 스킬**이며, MCP 서버를 한꺼번에 설치하지 않는다. 보안 스킬·에이전트·훅·규칙은 별도 플러그인 `security-gate@mochunab-tools`로 설치한다. HWP 스킬도 독립 플러그인 `hwp@mochunab-tools`로 설치한다.

## 공유 주소

- [Aside Browser 안내](https://github.com/mochunab/agent-toolkit/tree/main/skills/aside-browser)
- [Semble MCP 안내](https://github.com/mochunab/agent-toolkit/tree/main/mcp/semble)
- [Mac 앱 테스트 자동화 안내](https://github.com/mochunab/agent-toolkit/tree/main/guides/mac-app-test-automation)
- [HWP 안내](https://github.com/mochunab/agent-toolkit/tree/main/plugins/hwp)
- [Security Gate 안내](https://github.com/mochunab/agent-toolkit/tree/main/plugins/security-gate)

## 라이선스

이 저장소의 직접 제작 지침·가이드·템플릿·Semble MCP 래퍼·패키징은 [MIT](LICENSE)로 배포한다. 외부 도구는 각 프로젝트에서 설치하며, 출처와 이용 조건은 해당 자산의 README를 따른다. Security Gate의 일부 체크리스트는 MIT 라이선스의 ECC에서 가져왔으며 고지는 [THIRD_PARTY_NOTICES](plugins/security-gate/THIRD_PARTY_NOTICES.md)에 있다.

개인 인증 파일, 브라우저 데이터와 사용자별 MCP 설정은 포함하지 않는다.
