# 필받음 2차 QA AI 테스터 시범

[mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers) v0.1.0(`48f8bf3`, MIT)을 그대로 가져와, 필받음(judangbang-ops/pillbadeum_release) 2차 빌드를 AI 테스터가 써 보게 하는 시범 저장소예요.

- 바꾼 것: `results_public.pem`(이 저장소의 결과 암호화 공개키), `personas.json`에 한국어 Android 페르소나 셋(`pb_sunja`, `pb_jihye`, `pb_taeho`), 브리프 둘(`briefs/pillbadeum.md` 기본 탐색, `briefs/pillbadeum-card.md` 건강 카드 핵심 흐름).
- Claude는 구독 토큰(`CLAUDE_CODE_OAUTH_TOKEN`)만 써요. API 키는 두지 않아요. 한 번에 세 대까지 돌려요.
- 결과·로그·화면은 공개키로 암호화해 올라가요. 개인 키는 저장소 주인의 PC에만 있어요.
- 이 시범은 TC 시험, 실기기 확인, 릴리즈 게이트(release gate)를 대신하지 않아요.

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
