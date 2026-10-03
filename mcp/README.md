# MCP 연결

## Aside

Aside CLI가 제공하는 MCP 서버를 연결하는 예시다. 서버 자체는 Aside가 개발한다.

1. [공식 설치 안내](https://docs.aside.com/help/developers)에 따라 Aside Browser와 CLI를 설치하고 브라우저를 실행한다.
2. Claude Code에서 기존 설정을 확인한다.

```bash
claude mcp list
```

3. Aside가 등록되지 않았다면 사용자 승인 후 연결한다.

```bash
claude mcp add --scope user aside -- "$(command -v aside)" mcp
```

`command -v aside`가 경로를 반환하는지 먼저 확인한다. 다른 MCP 클라이언트에는 [JSON 예시](aside.example.json)를 참고한다. 호스트가 PATH에서 CLI를 찾지 못하면 CLI의 실제 절대 경로를 사용한다.

호스트에서 MCP를 다시 연결하거나 재시작한 뒤 도구가 나타나는지 확인한다. 설정 저장과 실제 연결 성공은 다르다. 이 저장소의 플러그인은 MCP를 자동 등록하지 않으며, 스킬이 연결 누락을 발견하면 진행 여부를 묻는다.

## Semble MCP

mochunab의 기존 공개 프로젝트: [semble-mcp](https://github.com/mochunab/semble-mcp).

BM25와 의미 검색을 결합하는 코드 검색 MCP 래퍼다. 서버 소스와 설치 지침은 해당 저장소에서 관리한다. 기반 검색 엔진은 외부 프로젝트이므로 해당 프로젝트의 설치 조건과 라이선스도 확인한다.
