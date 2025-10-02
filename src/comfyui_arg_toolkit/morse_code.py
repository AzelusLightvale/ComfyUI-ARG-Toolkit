# This implementation is lifted from https://github.com/Aayush9029/encodeDecode, which is left abandoned since 2020. This will attempt to roll that implementation in while implementing more languages that can be supported within reason (so no Chinese telegraph code for Chinese, unfortunately).
import unicodedata


class MorseCode:
    def __init__(self):
        """
        This dictionary is made using Wikipedia as the reference. See https://en.wikipedia.org/wiki/Morse_code_for_non-Latin_alphabets and https://en.wikipedia.org/wiki/Morse_code#Letters,_numbers,_punctuation,_prosigns_for_Morse_code_and_non-Latin_variants for more information.
        """
        self.latin_codes = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "0": "-----",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            ".": ".-.-.-",
            ",": "--..--",
            "?": "..--..",
            "/": "-..-.",
            "-": "-....-",
            "(": "-.--.",
            ")": "-.--.-",
            " ": " ",
        }
        self.russian_codes = {
            "А": ".-",
            "Б": "-...",
            "В": ".--",
            "Г": "--.",
            "Д": "-..",
            "Е": ".",
            "Ж": "...-",
            "З": "--..",
            "И": "..",
            "Й": ".---",
            "К": "-.-",
            "Л": ".-..",
            "М": "--",
            "Н": "-.",
            "О": "---",
            "П": ".--.",
            "Р": ".-.",
            "С": "...",
            "Т": "-",
            "У": "..-",
            "Ф": "..-.",
            "Х": "....",
            "Ц": "-.-.",
            "Ч": "---.",
            "Ш": "----",
            "Щ": "--.-",
            "Ы": "-.--",
            "Ь": "-..-",
            "Э": "..-..",
            "Ю": "..--",
            "Я": ".-.-",
            "Ї": ".---.",
            "0": "-----",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            ".": ".-.-.-",
            ",": "--..--",
            "?": "..--..",
            "/": "-..-.",
            "-": "-....-",
            "(": "-.--.",
            ")": "-.--.-",
            " ": " ",
        }
        self.arabic_codes = {
            "ا": ".-",
            "ب": "-...",
            "ت": "-",
            "ث": "-.-.",
            "ج": ".---",
            "ح": "....",
            "خ": "---",
            "د": "-..",
            "ذ": "--..",
            "ر": ".-.",
            "ز": "---.",
            "س": "...",
            "ش": "----",
            "ص": "-..-",
            "ض": "...-",
            "ط": "..-",
            "ظ": "-.--",
            "ع": ".-.-",
            "غ": "--.",
            "ف": "..-.",
            "ق": "--.-",
            "ك": "-.-",
            "ل": ".-..",
            "م": "--",
            "ن": "-.",
            "ه": "..",
            "و": ".--",
            "ي": "..--",
            "٠": "-----",
            "١": ".----",
            "٢": "..---",
            "٣": "...--",
            "٤": "....-",
            "٥": ".....",
            "٦": "-....",
            "٧": "--...",
            "٨": "---..",
            "٩": "----.",
            "؟": "..--..",
        }
        self.hebrew_codes = {
            "א": ".-",
            "ב": "-...",
            "ג": "--.",
            "ד": "-..",
            "ה": "---",
            "ו": ".",
            "ז": "--..",
            "ח": "....",
            "ט": "..-",
            "י": "..",
            "כ": "-.-",
            "ל": ".-..",
            "מ": "--",
            "נ": "-.",
            "ס": "-.-.",
            "ע": ".---",
            "פ": ".--.",
            "צ": ".--",
            "ק": "--.-",
            "ר": ".-.",
            "ש": "...",
            "ת": "-",
            "ך": "-.-",
            "ם": "--",
            "ן": "-.",
            "ף": ".--.",
            "ץ": ".--",
        }
        self.greek_codes = {
            "Α": ".-",
            "Β": "-...",
            "Γ": "--.",
            "Δ": "-..",
            "Ε": ".",
            "Ζ": "--..",
            "Η": "....",
            "Θ": "-.-.",
            "Ι": "..",
            "Κ": "-.-",
            "Λ": ".-..",
            "Μ": "--",
            "Ν": "-.",
            "Ξ": "-..-",
            "Ο": "---",
            "Π": ".--.",
            "Ρ": ".-.",
            "Σ": "...",
            "Τ": "-",
            "Υ": "-.--",
            "Φ": "..-.",
            "Χ": "----",
            "Ψ": "--.-",
            "Ω": ".--",
        }
        self.korean_codes = {
            "ㄱ": ".-..",
            "ㄴ": "..-.",
            "ㄷ": "-...",
            "ㄹ": "...-",
            "ㅁ": "--",
            "ㅂ": ".--",
            "ㅅ": "--.",
            "ㅇ": "-.-",
            "ㅈ": ".--.",
            "ㅊ": "-.-.",
            "ㅋ": "-..-",
            "ㅌ": "--..",
            "ㅍ": "---",
            "ㅎ": ".---",
            "ㅏ": ".",
            "ㅑ": "..",
            "ㅓ": "-",
            "ㅕ": "...",
            "ㅗ": ".-",
            "ㅛ": "-.",
            "ㅜ": "....",
            "ㅠ": ".-.",
            "ㅡ": "-..",
            "ㅣ": "..-",
            "ㅐ": "--.-",
            "ㅔ": "-.--",
        }
        self.japanese_codes = {
            "ア": "--.--",
            "イ": ".-",
            "ウ": "..-",
            "エ": "-.---",
            "オ": ".-...",
            "カ": ".-..",
            "キ": "-.-..",
            "ク": "...-",
            "ケ": "-.--",
            "コ": "----",
            "サ": "-.-.-",
            "シ": "--.-.",
            "ス": "---.-",
            "セ": ".---.",
            "ソ": "---.",
            "タ": "-.",
            "チ": "..-.",
            "ツ": ".--.",
            "テ": ".-.--",
            "ト": "..-..",
            "ナ": ".-.",
            "ニ": "-.-.",
            "ヌ": "....",
            "ネ": "--.-",
            "ノ": "..--",
            "ハ": "-...",
            "ヒ": "--..-",
            "フ": "--..",
            "ヘ": ".",
            "ホ": "-..",
            "マ": "-..-",
            "ミ": "..-.-",
            "ム": "-",
            "メ": "-...-",
            "モ": "-..-.",
            "ヤ": ".--",
            "ユ": "-..--",
            "ヨ": "--",
            "ラ": "...",
            "リ": "--.",
            "ル": "-.--.",
            "レ": "---",
            "ロ": ".-.-",
            "ワ": "-.-",
            "ヰ": ".-..-",
            "ヱ": ".--..",
            "ヲ": ".---",
            "ン": ".-.-.",
            "゛": "..",
            "゜": "..--.",
            "ー": ".--.-",
            "。": ".-.-..",
            "、": ".-.-.-",
            "（": "-.--.-",
            "）": ".-..-.",
        }
        pass

    CATEGORY = "Utilities/Converter"

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "label_on": "encode",
                        "label_off": "decode",
                        "tooltip": "Toggle between encoding and decoding",
                    },
                ),
                "language": (
                    [
                        "latin",
                        "russian",
                        "arabic",
                        "hebrew",
                        "greek",
                        "korean",
                        "japanese-wabun",
                    ],
                    {
                        "tooltip": """The list of languages supported by this implementation of the Morse code interpreter:
                    - Latin (default)
                    - Russian (Cyrillic)
                    - Arabic
                    - Hebrew
                    - Greek
                    - Korean (equivalent to SKATS)
                    - Japanese-Wabun (Wabun code for Japanese)
                    """
                    },
                ),
            },
            "optional": {
                "dot": (
                    "STRING",
                    {
                        "default": ".",
                        "multiline": False,
                        "tooltip": "The symbol used to represent the dot. Defaults to `.`",
                    },
                ),
                "dash": (
                    "STRING",
                    {
                        "default": "-",
                        "multiline": False,
                        "tooltip": "The symbol used to represent the dash. Defaults to `-`",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("converted_txt",)
    FUNCTION = "MorseCode"

    def morse_remap(self, text, dot, dash, dot_out=".", dash_out="-"):
        norm = []
        for ch in text:
            if ch in dot:
                norm.append(".")
            elif ch in dash:
                norm.append("-")
            else:
                norm.append(ch)  # leave spaces/punctuation alone
        norm = "".join(norm)

        # Map to output symbols
        return norm.replace(".", dot_out).replace("-", dash_out)

    def MorseCode(self, text, mode, language, dot, dash):
        language_table = {
            "latin": self.latin_codes,
            "russian": self.russian_codes,
            "arabic": self.arabic_codes,
            "hebrew": self.hebrew_codes,
            "greek": self.greek_codes,
            "korean": self.korean_codes,
            "japanese-wabun": self.japanese_codes,
        }
        codes = language_table[language]

        def strip_accents(s):
            return "".join(
                c
                for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn"
            )

        def hiragana_to_katakana(s):
            return "".join(
                [
                    chr(ord(char) + 96)
                    if "\u3040" <= char <= "\u309f"
                    else char
                    for char in s
                ]
            )

        def normalize_japanese(s):
            # Normalize width and convert hiragana → katakana
            s = unicodedata.normalize("NFKC", s)
            return hiragana_to_katakana(s)

        def decompose_hangul(text):
            decomposed_text = []
            # Choseong (initial)
            CHOSEONG = [
                "ㄱ",
                "ㄲ",
                "ㄴ",
                "ㄷ",
                "ㄸ",
                "ㄹ",
                "ㅁ",
                "ㅂ",
                "ㅃ",
                "ㅅ",
                "ㅆ",
                "ㅇ",
                "ㅈ",
                "ㅉ",
                "ㅊ",
                "ㅋ",
                "ㅌ",
                "ㅍ",
                "ㅎ",
            ]
            # Jungseong (medial)
            JUNGSEONG = [
                "ㅏ",
                "ㅐ",
                "ㅑ",
                "ㅒ",
                "ㅓ",
                "ㅔ",
                "ㅕ",
                "ㅖ",
                "ㅗ",
                "ㅘ",
                "ㅙ",
                "ㅚ",
                "ㅛ",
                "ㅜ",
                "ㅝ",
                "ㅞ",
                "ㅟ",
                "ㅠ",
                "ㅡ",
                "ㅢ",
                "ㅣ",
            ]
            # Jongseong (final)
            JONGSEONG = [
                "",
                "ㄱ",
                "ㄲ",
                "ㄳ",
                "ㄴ",
                "ㄵ",
                "ㄶ",
                "ㄷ",
                "ㄹ",
                "ㄺ",
                "ㄻ",
                "ㄼ",
                "ㄽ",
                "ㄾ",
                "ㄿ",
                "ㅀ",
                "ㅁ",
                "ㅂ",
                "ㅄ",
                "ㅅ",
                "ㅆ",
                "ㅇ",
                "ㅈ",
                "ㅊ",
                "ㅋ",
                "ㅌ",
                "ㅍ",
                "ㅎ",
            ]

            for char in text:
                if "가" <= char <= "힣":
                    char_code = ord(char) - ord("가")
                    choseong_index = char_code // (21 * 28)
                    jungseong_index = (char_code % (21 * 28)) // 28
                    jongseong_index = char_code % 28

                    decomposed_text.append(CHOSEONG[choseong_index])
                    decomposed_text.append(JUNGSEONG[jungseong_index])
                    if jongseong_index > 0:
                        decomposed_text.append(JONGSEONG[jongseong_index])
                else:
                    decomposed_text.append(char)
            return "".join(decomposed_text)

        # Reverse lookup for decoding
        rev_codes = {}
        for k, v in codes.items():
            if v not in rev_codes:
                rev_codes[v] = k

        # Normalize input Morse (map arbitrary symbols → '.' and '-')
        def normalize(morse_str):
            return "".join(
                "." if ch == dot else "-" if ch == dash else ch for ch in morse_str
            )

        # Encode
        if mode:  # encode
            if language == "japanese-wabun":
                text = normalize_japanese(text)
            elif language == "greek":
                text = strip_accents(text.upper())
            elif language == "korean":
                text = decompose_hangul(text)
            else:
                text = text.upper()
            result = []
            for char in text:
                if char in codes:
                    morse = codes[char].replace(".", dot).replace("-", dash)
                    result.append(morse)
                elif char.isspace():
                    result.append("")  # word separator
            return (" ".join(result),)
        # Decode
        else:
            words = text.strip().split(" ")
            result = []
            for code in words:
                norm = normalize(code)
                if norm in rev_codes:
                    result.append(rev_codes[norm])
                elif code == "":
                    if not result or result[-1] != " ":
                        result.append(" ")  # preserve spaces
            output = "".join(result)
            if language == "japanese-wabun":
                output = normalize_japanese(output)
            return (output,)


NODE_CLASS_MAPPINGS = {"MorseCode": MorseCode}
NODE_DISPLAY_NAME_MAPPINGS = {"MorseCode": "Morse Code"}
