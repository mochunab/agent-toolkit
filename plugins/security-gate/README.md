# Security Gate

코딩 에이전트가 보안 점검을 **증거 기준**으로 하고, 배포 전에는 검사 결과가 없거나 실패하면 **배포를 멈추게** 하는 Claude Code 플러그인. "보안 점검해줘", "프로젝트에 보안 연결해줘"처럼 쉬운 말로 요청하면 된다.

이 문서만으로 설치·사용할 수 있다. 실제 에이전트 지침은 [security-review 스킬](skills/security-review/SKILL.md)과 [deploy-checker 에이전트](agents/deploy-checker.md)에 있다.

> **현재 상태**: 점검 절차·배포 판정 기준·CI 템플릿을 제공한다. 특정 프로젝트에 자동 검사와 배포 차단을 실제로 연결·검증한 사례는 아직 없다. 템플릿 설치만으로 프로젝트가 보호되지 않는다.

## 무엇이 들어 있나

| 구성 | 역할 | 플러그인 설치 시 |
|---|---|---|
| [security-review 스킬](skills/security-review/SKILL.md) | 요청에 따라 점검·CI 적용·배포 게이트·개발 지원 모드 선택 | 자동 설치 |
| [점검 절차](skills/security-review/references/review-workflow.md) | 읽기 전용 보안 점검과 보고 형식 | 스킬에 포함 |
| [배포 게이트](skills/security-review/references/deployment-gate.md) | 배포 전 필수 검사, Pass·Block·미검증·N/A 판정 | 스킬에 포함 |
| [CI 적용 절차](skills/security-review/references/ci-gate.md) | 프로젝트에 자동 검사·배포 차단을 연결하고 실제로 막히는지 검증 | 스킬에 포함 |
| [CI 템플릿](skills/security-review/assets/security-deploy.yml) | npm 프로젝트용 GitHub Actions 초안. 자동 활성화되지 않음 | 스킬에 포함 |
| [클라우드 보안 체크리스트](skills/security-review/cloud-infrastructure-security.md) | IAM·시크릿·네트워크·CI/CD·로그 점검 참고 | 스킬에 포함 |
| [deploy-checker 에이전트](agents/deploy-checker.md) | 보안 결과를 받아 빌드·Git·CI·보안 최종 판정. 배포는 하지 않음 | 자동 설치 |
| [보안 규칙 예시](templates/security-rules.md) | 항상 적용할 라우팅·배포 게이트·금지 규칙 | **설치 안 됨.** 원하면 직접 복사 |

필요 환경: Claude Code(플러그인·에이전트 지원 버전). Codex는 스킬만 사용할 수 있다. 실제 시크릿 스캔·SAST 도구(예: Gitleaks, Semgrep)는 이 플러그인에 없다. 프로젝트에 맞는 도구를 승인받아 따로 설치한다.

## 설치

설치 방법은 하나만 선택한다. 플러그인과 수동 복사를 함께 하면 같은 스킬이 두 번 보인다.

### Claude Code 플러그인 (권장)

```bash
claude plugin marketplace add mochunab/agent-toolkit
claude plugin install security-gate@mochunab-tools --scope user
```

설치 범위는 이 폴더의 스킬 1개와 에이전트 1개다. 같은 저장소의 `agent-toolkit` 플러그인(Aside)이나 MCP 서버는 설치되지 않고, 사용자의 `CLAUDE.md`·설정 파일도 바꾸지 않는다. 설치 후 호스트 안내에 따라 플러그인을 다시 로드한다.

플러그인 안에서는 이름이 `security-gate:security-review`, `security-gate:deploy-checker`로 표시된다.

### 수동 설치 (Claude Code)

```bash
git clone https://github.com/mochunab/agent-toolkit.git
cd agent-toolkit/plugins/security-gate
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R skills/security-review ~/.claude/skills/
cp agents/deploy-checker.md ~/.claude/agents/
```

같은 이름의 `security-review` 스킬이나 `deploy-checker` 에이전트가 이미 있으면 먼저 내용을 비교하고 백업한다. 덮어쓰기 전에 기존 파일을 지우지 않는다.

### Codex (스킬만)

```bash
mkdir -p ~/.agents/skills
cp -R skills/security-review ~/.agents/skills/
```

Codex는 `~/.agents/skills/`에서 사용자 스킬을 읽는다. `deploy-checker`는 Claude Code 에이전트 형식이라 그대로 등록되지 않는다. Codex에서는 [deploy-checker.md](agents/deploy-checker.md)를 최종 점검 체크리스트로 사용해 별도 검토 단계로 진행한다. Codex에서의 종단 동작은 검증하지 않았다.

### 보안 규칙 (선택)

스킬은 요청할 때 동작한다. "배포할 때는 항상 게이트를 거친다"를 모든 대화에 적용하려면 [보안 규칙 예시](templates/security-rules.md)에서 필요한 부분을 프로젝트 또는 전역 `CLAUDE.md`·`AGENTS.md`에 병합한다. 기존 파일 전체를 이 예시로 바꾸지 않는다.

## 설치 확인

1. Claude Code를 다시 로드하고 `/plugin`(플러그인 설치 시)에서 `security-gate`가 활성화됐는지 확인한다.
2. 아무 프로젝트에서 다음을 요청한다.

```text
이 프로젝트 보안 점검해줘. 읽기만 하고 고치지는 마.
```

점검 대상·실행한 검사·미검증 항목이 구분된 보고가 나오고 파일이 바뀌지 않았으면 정상이다.

## 요청별 동작

CI는 코드가 바뀔 때 자동으로 검사·배포하는 절차다. 사용자가 이 용어를 몰라도 된다.

| 요청 예시 | 동작 |
|---|---|
| "보안 점검해줘", "취약점 확인해줘" | 코드·설정·기존 검사 결과 점검. 기본 읽기 전용 |
| "프로젝트에 보안 연결해줘", "보안 문제 있으면 배포 막아줘" | 자동 보안 검사 + 실패 시 배포 차단을 프로젝트에 연결하고 실제로 막히는지 검증 |
| "보안 연결돼 있는지만 확인해줘" | 연결 상태 점검. 설정을 바꾸지 않음 |
| "배포 전 보안 점검해줘" | 배포 게이트 판정 → deploy-checker 최종 점검 |
| 로그인·API·결제 기능 구현 | 구현하면서 해당 보안 기준 적용 |

모드는 문구가 아니라 요청 의도·대상·이미 받은 권한으로 고른다. 확실히 지정하려면 `/security-gate:security-review`(플러그인) 또는 `/security-review`(수동 설치)로 호출한다.

## 배포 게이트 기준 요약

순서: **security-review → deploy-checker → 검증된 배포 경로**. 상세 기준은 [deployment-gate.md](skills/security-review/references/deployment-gate.md).

- 항목마다 Pass·Block·미검증·N/A로 판정하고 실행 근거를 남긴다. 필수 항목이 Block 또는 미검증이면 배포를 멈춘다.
- 필수 검사: 전체 Git 이력과 현재 배포 파일의 시크릿 스캔, 의존성 HIGH/CRITICAL, 정적 코드 분석(SAST), 인증·권한과 DB 접근 규칙(RLS)의 실제 허용·거부 테스트, 입력·에러 노출, 보안 헤더·HTTPS/TLS·CORS.
- 도구 미설치·실행 실패·권한 부족·얕은 clone은 통과가 아니다. grep만으로 시크릿 스캔이나 SAST를 대신하지 않는다.
- 검사한 커밋·작업 파일·배포 환경이 실제 배포 대상과 같아야 한다. 변경되면 다시 검사한다.
- production DB에 테스트 데이터를 쓰거나 정책을 바꿔 검증하지 않는다. 검증 URL이 필요하면 접근 제한된 preview를 쓴다.

## 프로젝트에 자동 검사 연결하기

"프로젝트에 보안 연결해줘"라고 요청하면 [CI 적용 절차](skills/security-review/references/ci-gate.md)를 따른다. [CI 템플릿](skills/security-review/assets/security-deploy.yml)은 npm + GitHub Actions용 초안이다. pnpm·yarn·다른 언어는 프로젝트 구조에 맞게 바꾼다.

템플릿에 반영된 것: 전체 Git 이력 체크아웃, SHA로 고정한 Actions 버전, 최소 권한, 검사와 배포의 동일 커밋, PR에서 production 시크릿 격리, `npm ci --ignore-scripts`, 보안 job 성공에만 의존하는 배포 job(main push + `SECURITY_DEPLOY_ENABLED=true`일 때만).

프로젝트에서 직접 준비해야 하는 것:

| 항목 | 내용 |
|---|---|
| `security:secrets` | 승인된 스캐너로 전체 이력·현재 파일 검사. 탐지·실행 오류 시 실패 |
| `security:sast` | 버전 고정된 도구·보안 규칙으로 코드 분석 |
| `security:tests` | 격리 환경에서 사용자 A·B·비로그인 권한, 입력 검증 실제 테스트. 필수 테스트 skip도 실패 |
| `security:headers` | 같은 커밋이 실행 중인 검증 URL의 헤더·HTTPS/TLS·CORS 검사 |
| `SECURITY_TEST_BASE_URL` | 해당 커밋의 검증 환경 주소. localhost HTTP는 TLS 근거가 아님 |
| `deploy:production` | 같은 체크아웃을 배포하는 실제 배포 명령과 자격증명 |
| required check | 보호 브랜치에 `security-gate` 필수 검사 등록 |
| 우회 경로 | 호스팅 Git 자동 배포·다른 workflow·CLI·Deploy Hook 확인·제한 |

빈 스크립트나 무조건 성공하는 명령으로 채우지 않는다. 실제 차단 완료는 **같은 조건에서 검사 성공 run은 배포되고, 실패·생략·취소 run은 배포되지 않는 것**을 실제 실행으로 비교하고 우회 경로까지 확인한 뒤 판정한다.

## 내 배포 명령에 게이트 붙이기

배포 스킬이나 명령이 있다면 배포 직전에 다음 단계를 넣는다.

```markdown
## 배포 전 필수 게이트
1. security-review 스킬의 references/deployment-gate.md 기준으로 대상 프로젝트를 판정한다.
2. 결과 요약을 deploy-checker 에이전트에 전달해 최종 판정을 받는다.
3. 필수 항목 Block·미검증, 빌드 실패, CI 실패·생략·취소, 검사 대상 불일치면 배포하지 않는다.
4. 검증된 CI production 경로가 있으면 CLI로 직접 production 배포하지 않는다.
```

## 문제 해결

| 증상 | 확인할 것 |
|---|---|
| 스킬이 발동하지 않음 | 플러그인 활성화·재로드, 명시 호출 `/security-gate:security-review` |
| 같은 이름 스킬이 두 개 보임 | 수동 설치본·다른 플러그인(예: ECC)의 `security-review`와 겹침. 하나만 남김 |
| 점검 결과에 "미검증"이 많음 | 정상 동작. 시크릿 스캐너·SAST·격리 테스트 환경이 없으면 통과로 바꾸지 않음. 도구를 승인·설치한 뒤 재실행 |
| deploy-checker가 항상 중단 판정 | 같은 커밋·작업 트리의 security-review 결과가 있는지, 필수 항목에 미검증이 남았는지 확인 |
| CI 템플릿이 실패 | `.nvmrc`·`package-lock.json`, `security:*` 스크립트 구현 여부 확인. 템플릿은 의도적으로 빈 검사를 실패시킴 |

## 제한과 미검증 항목

- 특정 프로젝트에서 원격 CI 실행·required check·배포 차단까지 종단 검증한 사례는 없다.
- 자연어 요청별 모드 선택은 대표 시나리오로 검토했으며 모든 표현에 대해 검증하지 않았다.
- CI 템플릿은 npm + GitHub Actions 전용이다. 스캐너 설치 단계는 포함하지 않는다.
- Codex에서는 스킬만 사용 가능하며 종단 동작은 검증하지 않았다.
- 체크리스트 예시 코드(Next.js·Supabase·Express 등)는 패턴 설명용이다. 프로젝트 스택에 맞게 적용한다.

## 출처와 라이선스

작성일: 2026-10-04 · mochunab

- 모드 라우팅, `references/`, `assets/`, `agents/deploy-checker.md`, `templates/`, 이 README: 이 저장소에서 작성. [MIT](https://github.com/mochunab/agent-toolkit/blob/main/LICENSE)
- `SKILL.md`의 영문 보안 체크리스트와 `cloud-infrastructure-security.md`: [ECC (affaan-m)](https://github.com/affaan-m/ECC)의 `security-review` 스킬을 가져와 수정. MIT. 고지와 수정 범위는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 도구 근거: [Gitleaks](https://github.com/gitleaks/gitleaks), [Semgrep CI](https://semgrep.dev/docs/semgrep-ci/sample-ci-configs), [GitHub Actions job 의존성](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs), [Claude Code 플러그인 manifest](https://code.claude.com/docs/en/plugins-reference)
