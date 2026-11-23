# Brief: 필받음 (복용 기록, 폰 안에만 저장, 계정 없음)

Read AGENT_BRIEF.md first: its tools, rules and final report all apply.
These lines change only what does not fit this app.

- 필받음 is a Korean Android app that records doses (먹음/건너뜀) for yourself or a
  family member. It has no account, no sign-up, no e-mail and no network: ignore every
  account or e-mail part of the base brief and of your persona.
- Use only made-up data: people "가상 엄마", "가상 아빠"; medicines "가상정 10mg", "예시캡슐";
  phone numbers 010-0000-0000. Never type a real name, phone number or address.
- Permission prompts (notifications, alarms): answer as your persona would. If you deny one,
  check what the app tells you afterwards.
- Never press a share target that sends data out of the phone. If a share sheet opens,
  note what it offers, then close it with Back.
- Your goal is your persona's `goal`. Also look at: the empty state on first launch,
  past records (지난 기록), settings (설정), and one wrong input (an empty name).
- Write report.md in Korean. Keep findings.json keys in English as the base brief shows,
  with Korean titles.
- The phone is set to Asia/Seoul and no permission is granted before the app asks.

## Korean text

- `type.py` sends Hangul as the keys of a Korean keyboard and the on-screen keyboard
  composes the syllables. The keyboard must be in 한국어 mode (see its space bar); switch
  it to English with the globe key before Latin letters.
- A text with Hangul and Latin letters is refused: type `"가상정 10"`, switch the keyboard,
  then `python3 scripts/android/type.py --append "mg"`.
- If the screenshot still shows the wrong text, tap the keys of the on-screen keyboard.
  Wrong letters made by the tool are not app bugs.

## Decided by design (not bugs)

Report one of these only if it stops a task or the screen differs from the line.
Sources are in the app repo: `docs/05-ui/screens.md` (SCR-nnn) and
`docs/01-planning/requirements.md`.

- Light colours only: no dark mode yet, even on a dark phone (requirements.md, scope).
- 지난 기록 has no cell before an item was registered, and ‹ goes back only to the month
  of the first item (screens.md SCR-008). A new install has records for today only.
- Time pickers use 5-minute steps. 먹은 시각 고치기 starts on the saved time rounded down
  and its button stays off until another time is picked (SCR-007).
- Tiles under 오늘: two per row at normal text size, one per row from 130% (SCR-004).
- [⋯] and the month arrows are 48 dp touch targets with a small drawn icon (SCR-004,
  SCR-008): judge them by the accessibility check, not by the icon.
- The base time zone line (Asia/Seoul) shows only when the phone's zone differs; 설정 shows
  the zone id itself (SCR-004, SCR-009).
- When exact alarms are not allowed (Android 14 default) the record screen shows a short
  notice with [허용하기]; battery limits are only in 설정 (SCR-004, SCR-009).
- Approved wording, not typos: "[항목 추가]" with brackets on the empty screen (SCR-004),
  the one-phone notice that repeats the person's name (SCR-010), times read aloud as
  "21시" (SCR-006).
- The name error under the field pushes the fields below down (SCR-006). Intro pages
  scroll between the top bar and the buttons at 200% text (SCR-005).
- Already reported, note in one line if you see them: the first reminder time row half
  under the save bar after turning 알림 받기 on, and long item names wrapping over many
  lines (no length limit yet).
