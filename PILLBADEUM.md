# 필받음 2차 QA AI 테스터 시범

[mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers) v0.1.0(`48f8bf3`, MIT)을 그대로 가져와, 필받음(judangbang-ops/pillbadeum_release) 2차 빌드를 AI 테스터가 써 보게 하는 시범 저장소예요.

- 바꾼 것: `results_public.pem`(이 저장소의 결과 암호화 공개키), `personas.json`에 한국어 Android 페르소나 셋(`pb_sunja`, `pb_jihye`, `pb_taeho`), 브리프 둘(`briefs/pillbadeum.md` 기본 탐색, `briefs/pillbadeum-card.md` 건강 카드 핵심 흐름).
- Claude는 구독 토큰(`CLAUDE_CODE_OAUTH_TOKEN`)만 써요. API 키는 두지 않아요. 한 번에 세 대까지 돌려요.
- 결과·로그·화면은 공개키로 암호화해 올라가요. 개인 키는 저장소 주인의 PC에만 있어요.
- 이 시범은 TC 시험, 실기기 확인, 릴리즈 게이트(release gate)를 대신하지 않아요.

시범 1번(실행 45228364103) 뒤에 바꾼 것:

- 시간대: 페르소나에 `timezone`(IANA 이름)을 두면 Android 에뮬레이터를 앱 설치 전에 그 시간대로 맞춰요(`scripts/android/run_agent.sh`). 우리 페르소나 셋은 `Asia/Seoul`이고, 키가 없는 템플릿 페르소나는 전처럼 러너의 UTC예요.
- 권한: 설치 때 권한을 미리 주지 않아요. 앱이 알림 권한을 묻는 창과 거부 뒤 안내를 테스터가 봐요. 미리 주려면 `-f grant_permissions=true`.
- 한글 입력: `scripts/android/type.py`가 한글을 두벌식 자판 키로 바꿔 보내고, 화면 키보드(한국어 모드)가 글자를 조합해요. 앱을 더 깔지 않아요. 한글과 영문 글자가 섞인 글은 나눠 적어요(브리프).
- 브리프: `briefs/pillbadeum.md`에 '설계로 정한 것'(시범 1번 오탐의 까닭)과 이미 보고한 두 문제를 더했어요.
- `pb_sunja` 목표: '어제 기록 찾기'는 새 설치에서 이룰 수 없어서 '지난 기록에서 오늘 기록 찾기'로 바꿨어요.

## 실행

기본 탐색:

```
gh workflow run agent-testers.yml -R kodonghui/pillbadeum-agent-testers \
  -f android_personas=pb_sunja,pb_jihye,pb_taeho -f ios_personas=none \
  -f source_repo=judangbang-ops/pillbadeum_release -f ref=<커밋 SHA> \
  -f app_dir=. -f app_id=com.judangbang.pillbadeum -f framework=kmp \
  -f android_build="./gradlew :androidApp:assembleDebug" \
  -f apk_path=androidApp/build/outputs/apk/debug/androidApp-debug.apk \
  -f brief=briefs/pillbadeum.md -f model=sonnet
```

건강 카드 핵심 흐름은 같은 명령에서 `-f brief=briefs/pillbadeum-card.md`만 바꿔요.

결과 받기: `bash scripts/collect.sh <실행 id>` (개인 키 기본 위치 `~/.mobile-agent-testers/kodonghui_pillbadeum-agent-testers.pem`).

### Windows(Git Bash)에서 결과 받기

- 이 저장소를 clone한 폴더 안에서 돌려요. `collect.sh`가 `gh repo view`로 저장소 이름을 읽어요.
- `python3`가 Microsoft Store 바로가기면 마지막 요약 단계가 멈춰요. 작업 폴더 밖의 빈 폴더에 `python3`라는 파일 하나를 두고 `PATH` 앞에 넣어요. 내용은 두 줄이에요: `#!/usr/bin/env bash`, `exec python -X utf8 -I "$@"`.
- `-X utf8`이 없으면 `SUMMARY.md`가 Windows 기본 인코딩(cp949)으로 써져, UTF-8로 열 때 한글이 깨져요. 이미 깨졌으면 각 `findings.json`을 직접 읽어요(UTF-8).
- 찾은 것의 제목을 Claude로 묶지 않으려면 `SUMMARY_GROUPING=0`을 붙여요.

```
PATH="<python3 파일을 둔 폴더>:$PATH" SUMMARY_GROUPING=0 \
  bash scripts/collect.sh <실행 id> ~/.mobile-agent-testers/kodonghui_pillbadeum-agent-testers.pem \
  ~/.mobile-agent-testers/runs/<실행 id>
```
