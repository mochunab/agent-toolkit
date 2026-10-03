# Claude Code에서 Codex Computer Use 사용하기

> 대상: Mac에서 Claude Code로 앱 화면을 읽고 조작하려는 사용자.
> 목표: `claude-codex-computer-use` 플러그인 설치 → 도구 연결 → 계산기 검증 → 아이폰 미러링 테스트.

작성·출처 확인: 2026-10-04 · 제작자 플러그인 버전 확인: `0.1.2`

**OpenAI Computer Use를 먼저 준비한 뒤 Claude Code에 연결하세요.** 이 플러그인은 이미 설치된 OpenAI 실행 프로그램을 사용하는 비공식 연결 도구입니다.

공통 설치·macOS 권한·레슨런은 [Computer Use 활성화 가이드북](computer-use-guide.md), 아이폰 테스트 흐름은 [아이폰 미러링 방법론](아이폰-미러링-테스트-자동화-방법론.md)을 참고하세요.

## 1. 시작 전에 준비하세요

| 준비물 | 확인 방법 | 없을 때 |
| --- | --- | --- |
| Mac | `sw_vers -productVersion` | Windows/Linux에서는 이 브리지 절차 적용하지 않기 |
| Claude Code | `claude --version` 및 로그인 | [Claude Code 설치 안내](https://code.claude.com/docs/en/setup) 확인 |
| Node | `node --version` | 브리지 서버가 실행할 수 있는 Node 준비 |
| OpenAI Computer Use | 공식 앱에서 계산기 화면 읽기·42 입력 성공 | [공통 가이드의 공식 활성화 절차](computer-use-guide.md#2-공식-앱에서-computer-use를-켜세요) 진행 |
| 시스템 권한 | 실제 런타임의 손쉬운 사용·화면 녹화 허용 | 공통 가이드 3장 진행 |

먼저 터미널에서 버전을 확인하세요.

```sh
/usr/bin/sw_vers -productVersion
claude --version
node --version
```

확인한 제작자 README의 런타임 요구사항은 macOS 14.4 이상이며, Claude Code 2.1.223은 제작자의 검증 버전입니다. 모든 새 버전의 호환성을 보장하는 뜻은 아닙니다. Node 실행은 [플러그인 서버 설정](https://github.com/songkeys/claude-codex-computer-use/blob/main/.claude-plugin/plugin.json)에 명시돼 있습니다.

**성공 신호:** 버전 명령 정상 출력, 공식 앱의 Computer Use 실제 조작 성공. 버전 확인만으로 런타임 동작까지 검증됐다고 판단하지 마세요.

## 2. 플러그인을 설치하세요

아래 방법 중 하나를 선택하세요. 기존 Claude Code 사용자에게는 터미널 방식이 바로 실행하기 편합니다.

### 방법 A. 터미널에서 설치

두 명령을 순서대로 실행하세요.

```sh
claude plugin marketplace add songkeys/claude-codex-computer-use
claude plugin install claude-codex-computer-use@songkeys
```

첫 명령은 설치 목록을 제공하는 마켓플레이스를 등록하고, 두 번째 명령은 실제 플러그인을 설치합니다.

### 방법 B. Claude Code 대화 안에서 설치

대화 입력창에서 아래 명령을 하나씩 입력하세요. 일반 터미널에 입력하는 명령이 아닙니다.

```text
/plugin marketplace add songkeys/claude-codex-computer-use
/plugin install claude-codex-computer-use@songkeys
```

**성공 신호:** 등록·설치 완료 메시지. 설치가 끝나면 기존 대화를 종료하고 Claude Code의 새 세션을 시작하세요. [제작자 설치 안내](https://github.com/songkeys/claude-codex-computer-use#install-as-a-claude-code-plugin)

## 3. 새 세션에서 도구 연결을 확인하세요

Claude Code 대화 입력창에서 확인하세요.

```text
/plugin
/mcp
```

| 확인 | 다음 단계로 넘어갈 신호 |
| --- | --- |
| 플러그인 | `claude-codex-computer-use` 설치·활성화 |
| MCP 서버 | 플러그인의 `computer-use` 서버 연결 |
| 실제 호출 | 앱 상태 읽기 도구 `get_app_state` 등 사용 가능 |

MCP는 AI와 외부 도구를 연결하는 방식입니다. 스킬이 보이는 것과 실제 도구가 연결된 것은 별개입니다. 도구가 연결됐다면 4장으로 진행하세요. 실패하면 6장에서 오류를 확인하세요.

### 권한 화면은 CLI로 열고, 허용은 직접 수행하세요

자동 안내가 없으면 [공통 가이드의 권한 CLI·실행 지침](computer-use-guide.md#3-2-claudecodex가-cli로-권한-설정-화면을-여세요)에 따라 손쉬운 사용·화면 녹화 화면을 열어주세요.

허용할 항목은 일반적으로 `Codex Computer Use`이며 실제 요청 앱을 기준으로 확인하세요. Claude 앱 전체에 권한을 줬다는 사실만으로 충분하다고 판단하지 마세요. 토글·Touch ID·암호 입력은 사용자가 수행합니다.

## 4. 계산기에 42를 입력해 검증하세요

새 Claude Code 세션에 아래 요청을 붙여 넣으세요.

```text
설치된 claude-codex-computer-use 플러그인의 실제 도구로 계산기를 조작해줘.
먼저 get_app_state로 계산기 화면을 읽고, 초기화한 뒤 42를 입력해줘.
조작 후 화면을 다시 읽고 표시값 42와 스크린샷을 확인해줘.
도구가 없거나 연결 오류가 나면 오류 원문과 실패 단계를 알려줘.
터미널로 앱을 여는 것만으로 Computer Use 성공으로 처리하지 마.
```

**성공 신호:** 화면 읽기 → 클릭·입력 → 새 화면에서 42 확인. 이 세 가지를 마치면 Claude Code에서 기본 사용을 시작할 수 있습니다.

## 5. 아이폰 미러링 테스트에 사용하세요

1. Mac의 `iPhone 미러링` 앱을 연결하고 아이폰 화면이 보이는지 확인하세요.
2. 아래 요청으로 Claude가 미러링 앱의 현재 상태를 읽도록 하세요.
3. 표시된 화면을 기준으로 테스트할 앱·동작을 지정하세요.

```text
Computer Use로 Mac의 iPhone 미러링 앱 화면을 읽어줘.
앱 이름으로 찾지 못하면 앱 목록에서 실제 이름·식별자를 확인해줘.
현재 화면을 확인한 다음 [대상 앱]의 [버튼/흐름]을 조작해줘.
조작 후 새 화면을 읽고 [기대 결과]가 나타났는지 확인해줘.
미러링 연결·보안 인증이 필요하면 사용자에게 필요한 조작을 안내해줘.
```

이 방식으로 기본 화면 조작이 가능합니다. 새 Mac·호스트에서는 미러링 화면 읽기 → 한 번 조작 → 결과 재확인을 실제로 수행하세요. 반복 회귀 테스트의 안정성은 별도로 측정해야 합니다.

재현 단계와 후속 테스트 항목은 [아이폰 미러링 방법론](아이폰-미러링-테스트-자동화-방법론.md)에 정리돼 있습니다.

## 6. 설치했는데 안 되면

| 증상 | 먼저 확인할 일 |
| --- | --- |
| `node`를 못 찾음 | 플러그인 서버가 실행되는 환경의 Node 경로 확인 |
| 스킬만 있고 도구 없음 | 새 세션 시작 후 `/mcp` 연결 확인 |
| `Computer Use client is missing` | 공식 앱에서 Computer Use 설치·활성화. 실제 런타임 경로 확인 |
| `CONNECTION_CLOSED` | 서버 로그·클라이언트·서명된 런처 경로 확인. 원인을 권한 문제로 단정하지 않기 |
| 화면 읽기·입력 실패 | 실제 런타임의 손쉬운 사용·화면 녹화 확인 |
| `Sender process is not authenticated` | 런타임 직접 실행 중단. 브리지가 서명된 Codex 실행 파일을 찾는지 확인 |
| 버전 불일치 | 제작자 안내대로 ChatGPT 종료·재실행 후 다시 검증 |
| Esc 취소 메시지 | 작업 중단. 사용자가 계속하라고 할 때 재개 |
| `errAETimeout` | 한 번 재시도. 반복되면 대상 앱 재실행, 마지막으로 ChatGPT 재실행 |
| 플러그인 업데이트가 반영 안 됨 | 마켓플레이스 갱신·재설치 후 새 세션 시작 |

설치본 갱신은 Claude Code 대화 입력창에서 아래 순서로 진행하세요.

```text
/plugin marketplace update songkeys
/plugin install claude-codex-computer-use@songkeys
```

경로·환경변수 진단은 [공통 가이드의 브리지 경로 확인](computer-use-guide.md#5-3-연결-실패-시에만-실행-경로를-확인하세요)을 참고하세요. 제작자 문서의 [오류별 조치](https://github.com/songkeys/claude-codex-computer-use#troubleshooting)도 함께 확인하세요.

### MCP만 직접 등록하는 대안

플러그인 설치를 쓸 수 없는 경우 제작자는 아래 대안을 제공합니다.

```sh
claude mcp add computer-use -- npx -y claude-codex-computer-use@latest
```

이 방식은 사용 지침인 스킬을 함께 설치하지 않습니다. 기본 경로는 플러그인 설치이며, 두 방식을 중복 등록하지 마세요. [제작자 MCP 설치 안내](https://github.com/songkeys/claude-codex-computer-use#install-the-mcp-bridge-from-npm)

## 7. 다른 Mac의 Claude Code에 전달할 설정 요청

이 문서와 공통 가이드 경로를 함께 전달하고 아래 요청을 사용하세요.

```text
이 가이드에 따라 현재 Mac의 Claude Code에 Computer Use를 연결해줘.
1. Claude Code·Node·OpenAI Computer Use 런타임 존재 여부를 확인해.
2. 런타임이 없으면 공통 가이드의 공식 설치·활성화부터 안내해.
3. 플러그인이 없으면 문서의 CLI로 마켓플레이스 등록·플러그인 설치를 진행해.
4. 새 세션이 필요하면 설치 결과를 알려주고 새 세션에서 연결을 확인하게 해줘.
5. 시스템 권한이 부족하면 공통 가이드의 CLI로 설정 화면을 하나씩 열어줘.
   허용할 실제 앱을 안내하고 사용자의 권한 허용 완료 응답을 기다려줘.
6. 실제 도구로 계산기 초기화·42 입력·새 화면 확인까지 검증해.
7. 설치 완료·도구 연결·실제 조작 성공을 구분해서 보고해.
```

이 요청은 현재 대화에 없는 도구를 만들어내지 않습니다. 설치 결과가 새 세션에 반영될 때까지 실제 조작 검증을 완료로 보고하지 마세요.

## 사용 방식과 근거

0.1.2 브리지는 앱 접근 승인 요청을 자동 수락하며, macOS 시스템 권한 허용과는 별개입니다. 화면·접근성 정보가 Claude Code의 모델 제공자에게 전달될 수 있습니다. 이 차이는 [제작자 데이터 흐름 설명](https://github.com/songkeys/claude-codex-computer-use#security-and-data-flow)에 명시돼 있습니다.

- [제작자 README](https://github.com/songkeys/claude-codex-computer-use): 준비물·설치 명령·실제 도구 사용·문제 해결.
- [플러그인 설정](https://github.com/songkeys/claude-codex-computer-use/blob/main/.claude-plugin/plugin.json): 2026-10-04 확인 버전 `0.1.2`, Node 기반 서버 실행.
- [Claude Code 공식 설치 안내](https://code.claude.com/docs/en/setup): Claude Code 설치·버전 확인.
- [공통 활성화 가이드북](computer-use-guide.md): 공식 앱 준비·권한 경로·CLI·레슨런.
- [아이폰 미러링 방법론](아이폰-미러링-테스트-자동화-방법론.md): 연결 요건·첫 조작·테스트 절차.

기준일 이후 버전이 달라지면 제작자 문서와 실제 설치본을 다시 대조하세요. 이 문서는 설치·사용 절차를 작성한 것이며 새 Mac의 설치나 실제 호출을 대신 검증한 기록은 아닙니다.
