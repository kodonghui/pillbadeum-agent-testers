"""scripts/android/type.py: Korean text sent as dubeolsik keys, Latin text as before. Offline: adb is never called."""
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("android_type", ROOT / "scripts/android/type.py")
typer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(typer)


class HangulKeys(unittest.TestCase):
    def test_words_become_the_keys_of_a_korean_keyboard(self):
        cases = {
            "가상 엄마": "rktkd djaak",
            "아침약": "dkcladir",
            "혈압약 1정": "gufdkqdir 1wjd",
            "까치": "Rkcl",      # double consonant = shift
            "닭": "ekfr",        # two final consonants
            "왜": "dho",         # compound vowel
            "의": "dml",
            "값": "rkqt",
            "ㅋㅋ": "zz",        # jamo on their own
            "010-0000-0000": "010-0000-0000",
        }
        for text, keys in cases.items():
            with self.subTest(text):
                self.assertEqual(typer.keys_for(text)[0], keys)

    def test_tables_have_one_entry_per_unicode_jamo(self):
        self.assertEqual((len(typer.INITIALS), len(typer.VOWELS), len(typer.FINALS)), (19, 21, 28))
        # The syllable tables and the stand-alone jamo table were written separately: they must agree
        initials = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
        finals = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
        vowels = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
        self.assertEqual([typer.JAMO[c] for c in initials], typer.INITIALS)
        self.assertEqual([typer.JAMO[c] for c in finals], typer.FINALS[1:])
        self.assertEqual([typer.JAMO[c] for c in vowels], typer.VOWELS)

    def test_every_syllable_has_keys(self):
        for code in range(0xAC00, 0xD7A4):
            keys = typer.hangul_keys(chr(code))
            self.assertRegex(keys, r"^[A-Za-z]{2,6}$", hex(code))

    def test_hangul_with_latin_letters_is_refused(self):
        with self.assertRaises(ValueError):
            typer.keys_for("가상정 10mg")

    def test_latin_text_is_typed_as_before(self):
        self.assertEqual(typer.keys_for("Café 2"), ("Cafe 2", False))
        self.assertEqual(typer.keys_for("가상"), ("rktkd", True))

    def test_usage_lists_the_append_option(self):
        self.assertTrue(re.search(r"--append", typer.__doc__))


if __name__ == "__main__":
    unittest.main()
