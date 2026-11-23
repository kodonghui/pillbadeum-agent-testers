"""Replaces the focused field's content. adb cannot type accents: they are
stripped. Korean (Hangul) is sent as the keys of the standard 2-set (dubeolsik)
layout, and the on-screen keyboard (Gboard in 한국어 mode) composes the
syllables, as when you type on a Korean keyboard. No app is installed for this.
Hangul needs the keyboard in Korean mode, Latin letters in English mode, so a
text with both is refused: type each part with the keyboard switched in between,
the second one with --append (keeps what is in the field).
Usage: python3 scripts/android/type.py [--append] "text" """
import re, subprocess, sys, unicodedata

# Dubeolsik keys: initial consonants, vowels and final consonants of a syllable,
# in Unicode order (syllable = 0xAC00 + (initial * 21 + vowel) * 28 + final).
INITIALS = ["r", "R", "s", "e", "E", "f", "a", "q", "Q", "t", "T", "d", "w", "W", "c", "z", "x", "v", "g"]
VOWELS = ["k", "o", "i", "O", "j", "p", "u", "P", "h", "hk", "ho", "hl", "y", "n", "nj", "np", "nl", "b", "m",
          "ml", "l"]
FINALS = ["", "r", "R", "rt", "s", "sw", "sg", "e", "f", "fr", "fa", "fq", "ft", "fx", "fv", "fg", "a", "q", "qt",
          "t", "T", "d", "w", "c", "z", "x", "v", "g"]
# Compatibility jamo typed on their own (ㄱ U+3131 ... ㅣ U+3163)
JAMO = dict(zip(
    "ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ",
    ["r", "R", "rt", "s", "sw", "sg", "e", "E", "f", "fr", "fa", "fq", "ft", "fx", "fv", "fg", "a", "q", "Q", "qt",
     "t", "T", "d", "w", "W", "c", "z", "x", "v", "g"] + VOWELS))


def is_hangul(ch):
    return 0xAC00 <= ord(ch) <= 0xD7A3 or ch in JAMO


def hangul_keys(ch):
    if ch in JAMO:
        return JAMO[ch]
    n = ord(ch) - 0xAC00
    return INITIALS[n // 588] + VOWELS[n % 588 // 28] + FINALS[n % 28]


def keys_for(text):
    """The keys to send for `text`, or raises ValueError when it mixes Hangul and Latin letters."""
    hangul = any(is_hangul(ch) for ch in text)
    out = []
    for ch in text:
        if is_hangul(ch):
            out.append(hangul_keys(ch))
        else:
            plain = unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode()
            if hangul and re.search(r"[A-Za-z]", plain):
                raise ValueError("Hangul and Latin letters in one text: type the Hangul part with the keyboard in "
                                 "한국어 mode, switch it to English (globe key), then type the rest with --append")
            out.append(plain)
    return "".join(out), hangul


def main(argv):
    append = argv[:1] == ["--append"]
    args = argv[1:] if append else argv
    if len(args) != 1:
        sys.exit(__doc__)
    try:
        t, hangul = keys_for(args[0])
    except ValueError as e:
        sys.exit(str(e))
    if not append:
        subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_MOVE_END"])
        subprocess.run(["adb", "shell", "input", "keyevent", *(["67"] * 40)])  # 40 backspaces
    t = re.sub(r"([\\'\"`$&|;<>()*~#])", r"\\\1", t).replace(" ", "%s")
    subprocess.run(["adb", "shell", "input", "text", t])
    if hangul:
        print("typed as Korean keyboard keys: if you see Latin letters, switch the keyboard to 한국어 and type again")
    else:
        print("typed: check it on the next screenshot (if you see Korean jamo, switch the keyboard to English)")


if __name__ == "__main__":
    main(sys.argv[1:])
