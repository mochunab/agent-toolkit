# Semble MCP

[semble_rs](https://github.com/ArcadeLabsInc/semble)를 호출하는 코드 검색 MCP 서버. 서버 정본은 [mochunab/agent-toolkit의 mcp/semble](https://github.com/mochunab/agent-toolkit/tree/main/mcp/semble)이다.

기존 `mochunab/semble-mcp`의 `6e8ae7e`에서 서버 코드·패키지·잠금 파일을 그대로 옮겼다. 도구 이름과 입력 규격은 동일하다.

## 도구

| 도구 | 역할 |
|---|---|
| `search` | BM25·의미 검색 기반 코드 검색, 순위와 줄 번호 반환 |
| `find_related` | 파일 위치와 관련된 코드 탐색 |
| `deps` | 파일의 import와 정의된 심볼 분석 |
| `impact` | 파일 변경의 전이적 영향 범위 분석 |

## 준비

- Node.js 18 이상과 npm.
- `semble_rs` 실행 파일이 `~/.cargo/bin/semble_rs`에 설치돼 있어야 한다. 설치 방법은 [검색 엔진 저장소](https://github.com/ArcadeLabsInc/semble)를 따른다.

이 래퍼는 API 키를 요구하지 않는다. 검색 엔진 바이너리를 설치하거나 포함하지 않는다.

## 설치

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cd agent-toolkit/mcp/semble
npm ci
node --check server.mjs
```

이미 Toolkit을 받았다면 다시 clone하지 않고 이 폴더에서 `npm ci`를 실행한다.

## Claude Code 연결

`mcp/semble` 폴더에서 다음을 실행한다.

```bash
claude mcp list
```

`semble`이 등록되지 않았다면:

```bash
claude mcp add --scope user semble -- node "$PWD/server.mjs"
```

기존 서버를 옮기는 경우 아래 이전 절차를 먼저 따른다. MCP JSON 설정을 직접 관리하는 클라이언트는 [설정 예시](semble.example.json)를 참고한다. `args`에는 자신의 Toolkit 설치 위치에 맞는 절대 경로를 넣는다.

호스트에서 MCP를 다시 연결하거나 재시작하고 `search`, `find_related`, `deps`, `impact`가 노출되는지 확인한다. `node server.mjs`는 MCP stdio 서버이므로 직접 실행하면 입력을 기다리는 것이 정상이다.

## 기존 설치에서 이전

1. 기존 MCP 등록 범위(local/user/project)와 실행 경로를 확인하고 기록한다. Claude Code에서는 `claude mcp get semble`로 확인한다.
2. Toolkit 설치와 `npm ci`를 마친다.
3. 기존 등록과 **같은 범위**에서 `semble`의 실행 경로를 Toolkit의 `mcp/semble/server.mjs`로 변경한다. 여러 범위에 같은 이름으로 중복 등록하지 않는다.
4. 호스트를 다시 연결하고 도구 목록 및 실제 검색·분석 호출을 확인한다.

예를 들어 기존 등록이 user 범위라면 `mcp/semble`에서:

```bash
claude mcp remove --scope user semble
claude mcp add --scope user semble -- node "$PWD/server.mjs"
```

기존 설치 폴더와 설정은 새 경로가 동작하는 것을 확인할 때까지 보관한다. 되돌리려면 같은 범위에 기록한 이전 실행 경로를 다시 등록한다. 서버 로직·입력 규격·검색 엔진 설치 위치는 이번 이전으로 바뀌지 않는다.

## 라이선스

이 MCP 래퍼는 Toolkit의 [MIT 라이선스](../../LICENSE)를 따른다. 외부 검색 엔진과 npm 의존성은 각 프로젝트의 라이선스를 따른다.

## 현재 확인된 제한

- 이번 이전에서 서버 로직은 변경하지 않았다. 기존 설치와 Toolkit 설치의 도구 입력 규격이 같고, 실제 Python 프로젝트에서 `search`, `deps`, `impact` 호출을 양쪽 모두 검증했다.
- 설치된 `semble_rs`에서 `find-related`는 파일·줄 번호를 별도 인수로 받는다. 기존 래퍼는 `파일:줄`을 한 인수로 넘기므로 `find_related` 호출이 실패한다. 기존 설치에서도 재현되는 호환 오류이며 이번 코드 이전으로 수정되지는 않았다.
- 검증에 사용한 검색 엔진은 `.mjs`를 분석 대상으로 인식하지 않았다. 지원 파일 형식은 사용하는 검색 엔진 버전에서 확인한다.
