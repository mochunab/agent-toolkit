# Computer Use 활성화 가이드북 — 설치부터 첫 조작까지

> 대상: 다른 컴퓨터에서 Computer Use를 처음 설정하는 사용자.
> 목표: 설치·권한·연결을 확인하고, 계산기에 42를 입력하는 실제 조작까지 완료.

최초 작성: 2026-10-03 · 개편·출처 확인: 2026-10-04

Claude Code 사용자는 [전용 설치·사용 가이드북](claude-code-computer-use-guide.md)에서 플러그인 설치부터 시작할 수 있습니다.

**처음에는 공식 앱에서 작동을 확인하세요. Claude Code에서 쓰려면 그다음 브리지를 연결하세요.** 설치 완료 메시지나 스킬 목록만으로 설정 완료를 판단하지 마세요.

## 1. 무엇을 설치해야 하나요?

Computer Use는 AI가 앱 화면을 읽고 클릭·입력하는 기능입니다. 이 문서는 다음 질문 순서로 안내합니다: 어디서 사용할지 → 어떻게 켤지 → 권한을 어떻게 줄지 → 실제 작동을 어떻게 확인할지 → 막히면 무엇을 볼지.

| 사용할 환경 | 따라갈 경로 | 적용 범위 |
| --- | --- | --- |
| ChatGPT 데스크톱 앱의 Work 또는 Codex | 2장 → 3장 → 4장 | 공식 안내의 지원 지역·환경에서 macOS/Windows 사용 |
| Claude Code | 공식 앱에서 4장 완료 → 5장 | macOS용 비공식 브리지 추가 설치 |
| Orca 등 다른 호스트 | 해당 호스트의 설치·연결 안내 확인 → 3·4장 검증 | 이 문서에는 검증된 Orca 설치 절차가 없음 |

Claude Code 브리지는 OpenAI 실행 프로그램을 포함하지 않습니다. Claude에 플러그인을 설치해도 공식 앱의 Computer Use 설치를 건너뛸 수 없습니다. 공식 설정은 [OpenAI Computer Use 안내](https://learn.chatgpt.com/docs/computer-use), 브리지 설정은 [제작자 README](https://github.com/songkeys/claude-codex-computer-use#requirements)를 기준으로 합니다.

### 시작 전 준비

- [ChatGPT 데스크톱 앱 안내](https://learn.chatgpt.com/docs/app)에 따라 앱 설치·로그인을 완료하세요.
- 사용할 계정에서 Computer Use가 제공되는지 확인하세요. 메뉴가 없으면 계정·지역·앱 버전·조직 정책 확인이 먼저입니다.
- Mac 사용자는 시스템 설정에서 권한을 변경할 수 있어야 합니다. Touch ID·암호 입력은 직접 수행하세요.
- Claude Code 사용자는 플러그인을 지원하는 Claude Code가 추가로 필요합니다. 확인한 브리지 0.1.2 README는 macOS 14.4 이상을 요구하며 Claude Code 2.1.223을 검증 버전으로 적고 있습니다. 전체 앱의 현재 요구사항은 별도로 확인하세요.

**다른 PC가 Windows라면 공식 앱 경로를 사용하세요. 이 문서의 Claude 브리지 명령과 macOS 권한 화면을 그대로 적용하지 마세요.**

## 2. 공식 앱에서 Computer Use를 켜세요

다음 메뉴 경로는 [공식 활성화 안내](https://learn.chatgpt.com/docs/computer-use#set-up-computer-use)를 요약한 것입니다. 메뉴가 다르면 최신 공식 문서와 실제 앱 화면을 대조하세요.

| 단계 | 할 일 | 다음 단계로 넘어갈 신호 |
| --- | --- | --- |
| 1 | ChatGPT 데스크톱 앱에서 ChatGPT의 Work 또는 Codex 선택 | 해당 모드 진입 |
| 2 | `Plugins → Computer Use`에서 `Install plugin` 또는 `Enable` 선택 | 활성화됨 |
| 3 | Computer Use의 서버·스킬 토글 모두 켜기 | 두 토글 켜짐 |
| 4 | `Try now` 선택 | 작업 시작 가능 |

Mac이면 다음 권한 설정으로 진행하세요. Windows는 대상 앱을 활성 데스크톱에 표시하고 4장의 실제 조작을 확인하세요.

## 3. Mac에서는 두 권한을 직접 확인하세요

### 3-1. 손쉬운 사용과 화면 녹화를 켜세요

자동 안내가 안 떠도 `시스템 설정 → 개인정보 보호 및 보안`을 직접 열어 확인하세요. 공식 안내에서 확인할 항목은 **Codex Computer Use**입니다.

| 설정 | 허용하는 동작 | 확인할 항목 |
| --- | --- | --- |
| 손쉬운 사용 | 앱 제어·클릭·키보드 입력 | `Codex Computer Use` 켜짐 |
| 화면 및 시스템 오디오 녹음 / 화면 기록 | 대상 화면 읽기·캡처 | `Codex Computer Use` 켜짐 |
| 전체 디스크 접근 권한 | 보호된 파일·다른 앱의 데이터 접근 | 파일 작업에 따라 판단. 위 두 권한을 대신하지 않음 |

Computer Use 기본 설정에서는 첫 두 항목을 우선 확인하세요. 전체 디스크 접근을 켠 사실만으로 화면 읽기나 제어가 허용됐다고 판단하지 마세요. 역할 구분은 [Apple 개인정보 보호 및 보안 설명](https://support.apple.com/guide/mac-help/change-privacy-security-settings-mchl211c911f/mac)과 [브리지 요구사항](https://github.com/songkeys/claude-codex-computer-use#requirements)에 근거합니다.

1. `손쉬운 사용`을 열고 실제 Computer Use 실행 프로그램을 허용하세요.
2. `화면 및 시스템 오디오 녹음`을 열고 같은 실행 프로그램을 허용하세요.
3. macOS가 종료·재실행을 요구하면 안내대로 진행하세요.
4. 항목이 없으면 공식 앱의 설치·활성화를 먼저 확인하고 첫 작업을 시도하세요. 손쉬운 사용의 `+`로 추가해야 할 경우 실제 설치된 앱을 선택하세요.

앱 이름만 보고 `ChatGPT`, `Claude`, `Orca` 전체를 일괄 허용하지 마세요. 별도 실행 프로그램인 `Codex Computer Use`, `Orca Computer Use` 등이 권한을 요청할 수 있으므로 실제 요청 항목을 확인하세요.

### 3-2. Claude·Codex가 CLI로 권한 설정 화면을 여세요

macOS 13 이상에서는 아래 명령으로 해당 설정 화면을 열 수 있습니다. **화면 열기와 권한 허용은 별개**입니다. AI는 화면을 열고 필요한 앱을 안내하며, 사용자는 토글·Touch ID·암호 입력을 직접 수행하세요.

먼저 운영체제 버전을 확인하세요.

```sh
/usr/bin/sw_vers -productVersion
```

**첫째, 손쉬운 사용 화면을 여세요.** 경로: `시스템 설정 → 개인정보 보호 및 보안 → 손쉬운 사용`.

```sh
/usr/bin/open 'x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_Accessibility'
```

실제 권한 요청 앱인 `Codex Computer Use` 등을 허용한 뒤 다음 명령으로 진행하세요. 두 설정 화면을 연속으로 열어 첫 화면을 덮지 마세요.

**둘째, 화면 녹화 화면을 여세요.** 경로: `시스템 설정 → 개인정보 보호 및 보안 → 화면 및 시스템 오디오 녹음`.

```sh
/usr/bin/open 'x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_ScreenCapture'
```

해당 런타임을 허용하고 재실행 안내가 있으면 따르세요. `open`의 종료 코드가 0이어도 권한이 허용됐거나 원하는 화면이 열렸다고 단정하지 마세요.

이 URL은 [Chromium의 macOS 설정 화면 열기 구현](https://chromium.googlesource.com/chromium/src/base/+/121663451b5528be114956be2c939ecc1d31551b/mac/mac_util.mm)을 참고했습니다. OS 버전에 따라 동작이 달라질 수 있습니다. macOS 12 이하는 URL의 `com.apple.settings.PrivacySecurity.extension` 대신 `com.apple.preference.security`를 사용하며, 기본 브리지 요구사항은 macOS 14.4 이상입니다.

원하는 세부 화면이 안 열리면 다음 명령으로 시스템 설정을 열고 위 경로로 직접 이동하세요.

```sh
/usr/bin/open -a 'System Settings'
```

전체 디스크 접근은 `시스템 설정 → 개인정보 보호 및 보안 → 전체 디스크 접근 권한`에 있습니다. 보호된 파일 작업에 필요할 때만 확인하세요.

### 3-3. 다른 PC의 Claude·Codex에 전달할 실행 지침

아래 지침을 문서와 함께 전달하세요. 설치·연결·설정 화면 열기·실제 검증은 AI가 수행하고, 시스템 권한 허용 단계만 사용자에게 안내하도록 구성했습니다.

```text
이 가이드에 따라 현재 PC의 Computer Use를 설정하고 실제 작동을 검증해줘.
1. OS와 사용 호스트를 확인하고 설치된 런타임·현재 호출 가능한 Computer Use 도구를 확인해.
2. 런타임이나 도구가 없으면 먼저 이 문서의 설치·활성화·MCP 연결 절차를 진행해.
3. Mac이면 3-2의 CLI로 손쉬운 사용 화면을 열고 실제 허용할 앱 이름을 알려줘.
4. 사용자가 허용했다고 답하면 화면 녹화 설정을 열고 같은 방식으로 허용을 안내해.
5. 항목이 없으면 연결된 실제 Computer Use 도구로 계산기 상태 읽기를 한 번 시도해.
   발생한 권한 요청은 사용자가 승인하도록 안내하고 오류는 원문으로 기록해.
6. 필요한 재실행 후 계산기 화면 읽기 → 초기화·42 입력 → 새 화면 확인까지 수행해.
7. 확인된 설치·연결 상태, 필요한 사용자 조작, 검증 결과를 구분해서 보고해.
설정 화면을 열거나 파일을 발견한 것만으로 권한 허용·활성화 성공을 선언하지 마.
```

권한 요청을 유도할 때는 **실제 Computer Use 런타임을 사용하는 연결된 도구**를 호출하세요. Claude 브리지 0.1.2는 `get_app_state`로 계산기를 대상으로 삼습니다. Codex는 현재 세션에 제공된 Computer Use 도구와 사용 지침을 따르세요. 도구가 없다면 존재하지 않는 호출 명령을 만들어내지 말고 설치·연결을 해결하세요.

별도 Swift·Python 프로그램이나 `screencapture`로 테스트하면 Computer Use와 다른 실행 주체의 권한을 요청할 수 있습니다. 이를 Computer Use 런타임의 권한 요청·검증으로 대체하지 마세요. 권한 초기화 명령이나 권한 DB 수정을 기본 설정 절차에 넣지 마세요.

### 3-4. 안내가 안 뜨면 무엇을 의심하나요?


설치·연결 실패 때문에 실제 권한 요청 단계까지 도달하지 못했을 가능성이 있습니다. 브리지의 앱 사용 승인 처리 방식도 공식 앱과 다릅니다. 단, 안내가 없는 현상만으로 권한 누락이나 연결 오류 중 하나를 확정할 수 없습니다.

팝업 유무 대신 **실제 설정 화면과 다음 장의 조작 결과**를 확인하세요.

## 4. 계산기로 실제 작동을 확인하세요

새 대화에서 아래 요청을 입력하세요. 계산기에 기존 값이 있어도 검증할 수 있도록 초기화를 포함했습니다.

```text
Computer Use로 계산기를 열어줘.
현재 화면을 읽고, 계산기를 초기화한 다음 42를 입력해줘.
입력 후 화면을 다시 읽고, 표시값이 42인지 스크린샷과 함께 확인해줘.
```

공식 앱은 대상 앱 사용을 요청할 때 승인할 수 있습니다. 지속 허용 앱은 `Settings → Computer use`에서 검토하세요. macOS 권한·대상 앱 승인·셸 실행 승인은 서로 별도입니다.

| 확인 | 성공 신호 | 실패 시 이동 |
| --- | --- | --- |
| 화면 읽기 | 계산기 화면·상태 반환 | 3장 권한 확인 |
| 클릭·입력 | 초기화 후 숫자 입력 | 손쉬운 사용 확인 |
| 결과 재확인 | 새 화면의 표시값 `42`와 스크린샷 | 6장 문제 해결 |

이 세 가지가 모두 확인돼야 기본 설정 완료입니다. 터미널로 앱을 열거나 AI가 성공했다고 말한 것만으로 완료 처리하지 마세요.

### 이제 업무 요청을 시작하세요

```text
Computer Use로 [대상 앱]의 [화면/흐름]을 확인해줘.
작업 전 화면을 읽고, [할 동작]을 수행한 뒤 결과 화면을 다시 확인해줘.
```

공식 앱에서는 `@Computer`·`@앱이름`으로 대상을 지정할 수도 있습니다. Windows는 작업 중 전면 입력을 사용합니다. 기본 검증은 잠금 해제 상태에서 진행하고, Mac 잠금 중 사용은 별도 기능으로 [공식 Locked use 안내](https://learn.chatgpt.com/docs/computer-use#locked-use)를 확인하세요.

관리자 인증·보안 권한 승인은 사용자가 수행해야 합니다. 공식 기능의 터미널 앱·ChatGPT 자체 제어 제한은 [공식 사용 제한](https://learn.chatgpt.com/docs/computer-use#safety-guidance)을 확인하세요.

## 5. Claude Code에서 쓸 때만 브리지를 추가하세요

**전제: 공식 앱에서 계산기 검증 완료.** 여기부터는 `claude-codex-computer-use` 0.1.2 문서 기준입니다. 공식 앱 설정과 혼동하지 마세요.

이 브리지는 MCP(Model Context Protocol: AI와 외부 도구를 연결하는 방식)로 Claude Code에 도구를 제공합니다. 스킬은 사용 설명서, MCP 서버는 실제 실행 연결입니다.

### 5-1. 연결 구조와 승인 방식을 확인하세요

```text
Claude Code
  → 비공식 MCP 브리지
  → ChatGPT/Codex에 포함된 서명된 Codex 실행 파일
  → 설치된 OpenAI Computer Use 클라이언트
  → OpenAI Computer Use 서비스
  → 대상 macOS 앱
```

브리지는 서명된 실행 파일을 통해 클라이언트를 시작합니다. 직접 실행하면 프로세스 인증 오류가 발생할 수 있습니다.

또한 **0.1.2 브리지는 MCP의 앱 접근 승인 요청을 자동 수락**한다고 설명합니다. 따라서 공식 앱과 같은 대상 앱 승인 팝업이 나타날 것으로 기대하지 마세요. 이 동작은 macOS 손쉬운 사용·화면 녹화 권한을 대신하지 않습니다. 화면·접근성 정보는 Claude Code의 모델 제공자에게 전달될 수 있습니다. [브리지 동작·데이터 흐름](https://github.com/songkeys/claude-codex-computer-use#how-it-works)

### 5-2. Claude Code에 설치하고 새 세션을 시작하세요

터미널에서 아래 두 명령을 순서대로 실행하세요.

```sh
claude plugin marketplace add songkeys/claude-codex-computer-use
claude plugin install claude-codex-computer-use@songkeys
```

Claude Code를 새로 시작한 뒤 세션 안에서 확인하세요.

```text
/plugin
/mcp
```

**성공 신호:** 플러그인 활성화, MCP 서버 연결, 실제 Computer Use 도구 제공. 연결됐다면 Claude Code에서 4장의 계산기 요청을 다시 수행하세요.

0.1.2 브리지의 실제 도구는 `get_app_state` 등입니다. 공식 앱이나 다른 버전이 반드시 같은 도구 이름을 노출하는 것은 아닙니다. [설치 명령](https://github.com/songkeys/claude-codex-computer-use#install-as-a-claude-code-plugin) · [도구 사용 스킬](https://github.com/songkeys/claude-codex-computer-use/tree/main/skills/computer-use)

### 5-3. 연결 실패 시에만 실행 경로를 확인하세요

기본 클라이언트 위치:

```text
~/.codex/computer-use/Codex Computer Use.app/Contents/SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient
```

`CODEX_HOME`을 사용하는 환경은 `~/.codex` 대신 해당 위치를 확인하세요. Orca 등 호스트별·계정별 환경이 같다고 가정하지 마세요.

다음 명령은 파일 존재 여부만 확인합니다. 터미널에서 본 경로가 MCP 서버의 환경과 같다는 보장은 없습니다.

```sh
cu_data_dir="${CODEX_HOME:-$HOME/.codex}"
cu_client_path="${COMPUTER_USE_CLIENT_PATH:-$cu_data_dir/computer-use/Codex Computer Use.app/Contents/SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient}"
if [ -x "$cu_client_path" ]; then
  printf '클라이언트 발견: %s\n' "$cu_client_path"
else
  printf '클라이언트 없음 또는 실행 불가: %s\n' "$cu_client_path"
fi
```

런처 탐색 순서는 지정 경로 → `/Applications/ChatGPT.app/Contents/Resources/codex` → `/Applications/Codex.app/Contents/Resources/codex`입니다.

| 환경변수 | 필요한 경우 |
| --- | --- |
| `COMPUTER_USE_CLIENT_PATH` | 실제 클라이언트 전체 경로 지정 |
| `COMPUTER_USE_CODEX_LAUNCHER_PATH` | 실제 서명된 Codex 실행 파일 전체 경로 지정 |
| `COMPUTER_USE_BRIDGE_DEBUG=1` | 브리지 종료 원인을 진단 로그로 확인 |
| `COMPUTER_USE_BRIDGE_IDLE_TIMEOUT_MS` | 유휴 종료 조정. 0.1.2 기본값 `60000`ms |

변수는 실제 브리지 서버를 시작하는 환경에 전달해야 합니다. 터미널 설정이 GUI 앱에도 전달된다고 가정하지 마세요. `CODEX_HOME`을 무작정 덮어쓰지 말고 [브리지 설정 안내](https://github.com/songkeys/claude-codex-computer-use#configuration)와 실제 파일 위치를 대조하세요.

## 6. 막히면 실패한 단계부터 확인하세요

| 증상 | 먼저 확인·실행할 일 |
| --- | --- |
| 공식 앱에서 Computer Use 메뉴 없음 | 앱 업데이트·계정·지역·조직 정책 확인. 브리지 설치로 해결된다고 가정하지 않기 |
| 화면을 못 읽음 / 클릭·입력 안 됨 | 3장의 두 권한과 실제 요청 앱 확인 |
| 스킬은 있는데 도구 없음 | 해당 호스트의 서버 연결·활성화 확인. Claude Code는 설치 후 새 세션 시작 |
| `CONNECTION_CLOSED` | 브리지 클라이언트·런처 경로와 서버 로그 확인. 오류만으로 권한 문제라고 단정하지 않기 |
| `Computer Use client is missing` | 공식 앱에서 설치·활성화 후 실제 데이터 경로 확인 |
| `Sender process is not authenticated` | 클라이언트 직접 실행 중단. 서명된 Codex 런처 탐색 확인 |
| `Client and server version mismatch` | ChatGPT 종료·재실행 후 실제 조작 다시 확인 |
| `This application session has been explicitly stopped by the user` | Esc 취소 상태. 작업 중단하고 사용자가 재개할 때만 계속 |
| `errAETimeout` | 한 번 재시도. 반복되면 대상 앱 재실행, 마지막으로 ChatGPT 재실행 |
| 플러그인 수정이 반영 안 됨 | Claude Code 재시작 또는 `/plugin marketplace update songkeys` 후 재설치 |
| `Stop Using` 표시가 남음 | 표시만으로 제어 프로세스 생존을 단정하지 않기. 브리지 문서상 세션 기록이 남을 수 있음 |

오류 조치는 [브리지 문제 해결](https://github.com/songkeys/claude-codex-computer-use#troubleshooting) 기준입니다. YOLO 설정은 런타임 설치·MCP 연결·macOS 권한의 대체 수단이 아닙니다.

## 7. 설정 시행착오를 줄이는 레슨런

| 문제 | 판단할 수 있는 범위 | 다음 행동 |
| --- | --- | --- |
| 플러그인만 설치하고 런타임 준비를 생략 | 브리지는 OpenAI 실행 프로그램을 포함하지 않음 | 공식 앱 계산기 검증부터 완료 |
| 스킬은 보이는데 호출 도구가 없음 | 안내서와 실제 서버 연결은 별개 | MCP 연결·새 세션·도구 목록 확인 |
| 연결 종료 오류만 반복 | 오류 문구만으로 원인 확정 불가 | 최초 오류·서버 로그·실행 경로 확인 |
| 화면은 읽히지만 클릭이 안 됨 | 화면 녹화와 손쉬운 사용은 서로 다른 권한 | 실제 요청 앱의 두 권한 각각 확인 |
| 전체 디스크 접근만 허용 | 화면 읽기·제어 권한을 대신하지 않음 | 손쉬운 사용·화면 녹화 확인 |
| 권한 요청 팝업을 기다리기만 함 | 설치·연결이 요청 단계까지 도달했는지 불명 | 실제 도구 호출 후 설정 화면 직접 확인 |
| 여러 설정을 한꺼번에 바꾸고 성공 | 어떤 변경이 해결했는지 알기 어려움 | 한 단계씩 변경하고 같은 계산기 작업 재검증 |
| 셸 승인 생략을 시스템 권한으로 오해 | 셸 승인과 OS 권한은 별개 | [샌드박스·승인 안내](https://learn.chatgpt.com/docs/sandboxing)와 구분 |

권한 허용, 대상 앱 사용 승인, MCP 연결을 따로 기록하세요. 앱 접근 승인 자동 처리는 macOS 권한 안내 누락의 확정 원인이 아닙니다.

## 8. 설정 완료 기록을 남기세요

```text
설정 날짜 / 실행 환경:
운영체제 / 아키텍처:
사용 환경: 공식 앱 Work / Codex / Claude Code / Orca / 기타
앱·호스트·플러그인 버전:
서버·스킬 활성화 / MCP 연결 상태:
손쉬운 사용 허용 앱 / 상태:
화면 녹화 허용 앱 / 상태:
대상 앱 승인 상태 또는 브리지 자동 승인 방식:
클라이언트·서명된 런처 경로(공유 시 사용자 홈 경로는 자리표시자로):
최초 오류 원문:
성공 직전 변경한 설정:
화면 읽기 → 초기화·42 입력 → 새 화면·스크린샷 확인 결과:
남은 문제:
```

공식 앱과 Claude Code를 함께 쓴다면 두 환경의 계산기 검증 결과를 각각 남기세요. 다른 컴퓨터에서 따라 할 수 있는 완료 기록은 설치 목록이 아니라 **어떤 설정으로 실제 읽기·조작이 성공했는지**입니다.

## 참고 문서

- [OpenAI 공식 Computer Use](https://learn.chatgpt.com/docs/computer-use): 활성화·시스템 권한·대상 앱 승인·운영체제 차이.
- [ChatGPT 데스크톱 앱](https://learn.chatgpt.com/docs/app): 앱 설치·시작 안내.
- [Apple 개인정보 보호 및 보안](https://support.apple.com/guide/mac-help/change-privacy-security-settings-mchl211c911f/mac): 권한 역할.
- [비공식 브리지 README](https://github.com/songkeys/claude-codex-computer-use) · [스킬](https://github.com/songkeys/claude-codex-computer-use/tree/main/skills/computer-use): 본문은 0.1.2 문서 기준. 설치할 버전의 요구사항은 다시 확인하세요.
