import unicodedata
from src.comfyui_arg_toolkit import morse_code

# Test suite for morse_code.py
class TestMorseCode:
    def setup_method(self):
        self.morse_code = morse_code.MorseCode()

    def test_latin_morse_code(self):
        text = "Hello World"
        encoded_text = self.morse_code.MorseCode(text, True, "latin", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "latin", ".", "-")
        assert decoded_text[0].lower() == text.lower()

    def test_russian_morse_code(self):
        text = "Привет мир"
        encoded_text = self.morse_code.MorseCode(text, True, "russian", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "russian", ".", "-")
        assert decoded_text[0].lower() == text.lower()

    def test_arabic_morse_code(self):
        text = "مرحبا بالعالم"
        encoded_text = self.morse_code.MorseCode(text, True, "arabic", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "arabic", ".", "-")
        assert decoded_text[0] == text

    def test_hebrew_morse_code(self):
        text = "שלום עולם"
        encoded_text = self.morse_code.MorseCode(text, True, "hebrew", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "hebrew", ".", "-")
        assert decoded_text[0] == "שלומ עולמ"

    def test_greek_morse_code(self):
        text = "Γειά σου Κόσμε"
        encoded_text = self.morse_code.MorseCode(text, True, "greek", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "greek", ".", "-")
        assert decoded_text[0] == "ΓΕΙΑ ΣΟΥ ΚΟΣΜΕ"

    def test_korean_morse_code(self):
        text = "안녕하세요"
        encoded_text = self.morse_code.MorseCode(text, True, "korean", ".", "-")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "korean", ".", "-")
        assert decoded_text[0] == "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"

    def test_japanese_wabun_morse_code(self):
        text = "こんにちは"
        normalized_text = unicodedata.normalize("NFKC", text)
        print(f"Normalized text: {normalized_text}")
        encoded_text = self.morse_code.MorseCode(text, True, "japanese-wabun", ".", "-")
        print(f"Encoded text: {encoded_text}")
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "japanese-wabun", ".", "-")
        print(f"Decoded text: {decoded_text}")
        assert decoded_text == ("コンニチハ",)

    def test_custom_dot_dash_morse_code(self):
        text = "Hello World"
        dot = "1"
        dash = "0"
        encoded_text = self.morse_code.MorseCode(text, True, "latin", dot, dash)
        decoded_text = self.morse_code.MorseCode(encoded_text[0], False, "latin", dot, dash)
        assert decoded_text[0].lower() == text.lower()
