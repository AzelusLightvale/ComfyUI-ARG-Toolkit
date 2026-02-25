import secretpy
from secretpy import alphabets as al
import math

# Second version, uses secretpy instead of pycipher due to both wider coverage and being more updated than pycipher.

# The defaults used for each cipher in "Cryptography" will be the same one listed in their documentations in secretpy as well as some personal jokes.

# For more information, check https://pycipher.readthedocs.io/en/master/ on how each cipher works, as well as https://secretpy.readthedocs.io/en/latest/ for implementation documents (read *the examples*, not the actual API documentations. They lie quite a few times (as of the time of me making this).).


class BaseCipherNode:
    CATEGORY = "Cryptography/Classical"

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here... (has to match the alphabet's language)",
                    },
                ),
                "alphabet": (
                    "STRING",
                    {
                        "default": "ENGLISH",
                        "multiline": False,
                        "tooltip": "Input your alphabet here. If left blank, uses the alphabet default to the cipher. Uses standard connected format ('abcdef'), but can also accept the alphabets defined in secretpy in alphabets.py.",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "encrypt",
                        "label_off": "decrypt",
                        "tooltip": "Toggle between encrypting or decrypting a message.",
                    },
                ),
                "keep_formatting": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Toggle between preserving the format of the message or remove all spaces, punctuations, and convert to lowercase.",
                    },
                ),
            }
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("encrypted_txt",)

    def alphabet_checker(self, alphabet, as_tuple=True):
        if alphabet.strip():
            alphabet_upper = alphabet.strip().upper()
            if hasattr(al, alphabet_upper):
                predef = getattr(al, alphabet_upper)
            else:
                predef = alphabet

            if as_tuple:
                return tuple(predef)
            else:
                return "".join(predef)
        return None

    def preprocess_text(self, text, allowed_chars=None):
        cleaned = []
        position_map = []  # Maps cleaned position to original position

        for i, ch in enumerate(text):
            if allowed_chars is not None:
                if ch.lower() in allowed_chars:
                    cleaned.append(ch.lower())
                    position_map.append(i)
            else:
                if ch.isalpha():  # keep everything except whitespace
                    cleaned.append(ch.lower())
                    position_map.append(i)

        return "".join(cleaned), position_map

    def restore_formatting(self, original_text, cipher_result, position_map, mode):
        result = list(original_text)
        for pos in position_map:
            result[pos] = ""  # wipe letters, leave punctuation/spaces untouched

        cipher_index = 0
        for original_pos in position_map:
            if cipher_index >= len(cipher_result):
                break
            if original_text[original_pos].isupper():
                result[original_pos] = cipher_result[cipher_index].upper()
            else:
                result[original_pos] = cipher_result[cipher_index].lower()
            cipher_index += 1

        if mode:  # encryption may expand, so append leftovers
            if cipher_index < len(cipher_result):
                last_case = (
                    result[position_map[-1]].isupper() if position_map else False
                )
                tail = cipher_result[cipher_index:]
                if last_case:
                    result.extend(c.upper() for c in tail)
                else:
                    result.extend(c.lower() for c in tail)
        # decrypt case: leftovers automatically dropped

        return "".join(result)

    def execute_cipher(
        self, text, alphabet, key, mode, keep_formatting, allowed_chars=None, **kwargs
    ):
        cipher_name = self.__class__.__name__
        cipher_class = getattr(secretpy, cipher_name)
        cipher_instance = cipher_class()
        key = key.lower() if isinstance(key, str) else key
        cleaned_text, position_map = self.preprocess_text(text, allowed_chars)
        if mode:
            result = cipher_instance.encrypt(cleaned_text, key, alphabet, **kwargs)
        else:
            result = cipher_instance.decrypt(cleaned_text, key, alphabet, **kwargs)
        if keep_formatting and position_map:
            formatted_result = self.restore_formatting(text, result, position_map, mode)
            return (formatted_result,)
        else:
            return (result,)


class ADFGX(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def adfgx(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class ADFGVX(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in English as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def adfgvx(self, text, alphabet, key, mode, keep_formatting):
        return self.execute_cipher(text, alphabet, key, mode, keep_formatting)


class Affine(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key_1"] = (
            "INT",
            {
                "default": 7,
                "min": 1,
                "tooltip": "The multiplicative part of the Affine key. Allows only numbers with no common factors to the alphabet length (relatively prime).",
            },
        )
        class_input["required"]["key_2"] = (
            "INT",
            {
                "default": 8,
                "min": 0,
                "tooltip": "The additive part of the Affine key. Allows every integer from 0 up to the length of the alphabet minus 1 (imagine an index starting from 0).",
            },
        )
        return class_input

    def affine(self, text, alphabet, key_1, key_2, mode, keep_formatting):
        if len(alphabet) is None or len(alphabet) <= 1:
            raise ValueError("Alphabet size must be >= 2 for Affine.")
        if math.gcd(key_1, key_2) != 1:
            allowed = [
                x for x in range(1, len(alphabet)) if math.gcd(x, len(alphabet) == 1)
            ]
        if key_1 not in allowed:
            raise ValueError(
                f" Invalid key #1 ({key_1}) for the current alphabet size {len(alphabet)}."
            )
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = (key_1, key_2)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Atbash(BaseCipherNode):
    def atbash(self, text, alphabet, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Autokey(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def autokey(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Bazeries(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 32,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def bazeries(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Beaufort(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def beaufort(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Bifid(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 10,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def bifid(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Caesar(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 13,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def caesar(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class CaesarProgressive(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 13,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def caesarprogressive(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Chao(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts an alphabet of equivalent length to the chosen alphabet as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def chao(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class ColTrans(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def coltrans(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class FourSquare(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key_1"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        class_input["required"]["key_2"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        return class_input

    def foursquare(self, text, alphabet, key_1, key_2, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        key_1 = key_1.lower()
        key_2 = key_2.lower()
        key = (key_1, key_2)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Gronsfeld(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts a string of numbers (punctuation optional) as the first key to decrypt/encrypt. Note that anything not a number is ignored.",
            },
        )
        return class_input

    def gronsfeld(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        key_tuple = tuple(int(ch) for ch in key if ch.isdigit())
        if not key_tuple:
            raise ValueError("Invalid Gronsfeld key: must contain at least one digit.")
        return self.execute_cipher(
            text, processed_alphabet, key_tuple, mode, keep_formatting
        )


class Keyword(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def keyword(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class MyszkowskiTransposition(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def myszkowskitransposition(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Nihilist(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def nihilist(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Playfair(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts an alphabet of equivalent length to the chosen alphabet as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def playfair(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Polybius(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts an string of length that matches the square root of the length of your alphabet length.",
            },
        )
        return class_input

    def polybius(self, text, alphabet, key, mode, keep_formatting):
        if key != math.sqrt(len(alphabet)):
            raise ValueError(
                f"Your given key length ({len(key)} does not match the square root of your alphabet size ({math.sqrt(len(alphabet))})). Please check your alphabet and key again"
            )
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Porta(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def porta(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Rot13(BaseCipherNode):
    def rot13(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Rot5(BaseCipherNode):
    def rot5(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Rot18(BaseCipherNode):
    def rot18(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Rot47(BaseCipherNode):
    def rot47(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        key = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Scytale(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 4,
                "min": 1,
                "tooltip": "For Scytale cipher, the key indicates the number of windings around the cylinder the message should have.",
            },
        )
        return class_input

    def scytale(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class SimpleSubstitution(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts an alphabet of equivalent length to the chosen alphabet as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def simplesubstitution(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class ThreeSquare(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key_1"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        class_input["required"]["key_2"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        class_input["required"]["key_3"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        return class_input

    def threesquare(self, text, alphabet, key_1, key_2, key_3, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        key_1 = key_1.lower()
        key_2 = key_2.lower()
        key_3 = key_3.lower()
        key = (key_1, key_2, key_3)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Trifid(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 13,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def trifid(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        allowed_chars = processed_alphabet
        return self.execute_cipher(
            text, processed_alphabet, key, mode, keep_formatting, allowed_chars
        )


class TwoSquare(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key_1"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        class_input["required"]["key_2"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text (or alphabet) in the alphabet's language as the first key to decrypt/encrypt.",
            },
        )
        return class_input

    def twosquare(self, text, alphabet, key_1, key_2, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        key_1 = key_1.lower()
        key_2 = key_2.lower()
        key = (key_1, key_2)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Vic(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts a string of numbers (punctuation optional) as the first key to decrypt/encrypt. Note that anything not a number is ignored.",
            },
        )
        return class_input

    def vic(self, text, alphabet, key, mode, keep_formatting):
        key = str(int(ch) for ch in key if ch.isdigit())
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=True)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Vigenere(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Accepts any text in the alphabet's language as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def vigenere(self, text, alphabet, key, mode, keep_formatting):
        processed_alphabet = self.alphabet_checker(alphabet, as_tuple=False)
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


class Zigzag(BaseCipherNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key"] = (
            "INT",
            {
                "default": 13,
                "min": 1,
                "tooltip": "Accepts any non-negative integer as the key to decrypt/encrypt.",
            },
        )
        return class_input

    def zigzag(self, text, key, mode, keep_formatting):
        processed_alphabet = None
        return self.execute_cipher(text, processed_alphabet, key, mode, keep_formatting)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ADFGX": ADFGX,
    "ADFGVX": ADFGVX,
    "Affine": Affine,
    "Atbash": Atbash,
    "Autokey": Autokey,
    "Bazeries": Bazeries,
    "Beaufort": Beaufort,
    "Bifid": Bifid,
    "CaesarProgressive": CaesarProgressive,
    "Chaocipher": Chao,
    "ColTrans": ColTrans,
    "Foursquare": FourSquare,
    "Gronsfeld": Gronsfeld,
    "Keyword": Keyword,
    "MyszkowskiTransposition": MyszkowskiTransposition,
    "Nihilist": Nihilist,
    "Playfair": Playfair,
    "Polybius": Polybius,
    "Porta": Porta,
    "Rot13": Rot13,
    "Rot5": Rot5,
    "Rot18": Rot18,
    "Rot47": Rot47,
    "Scytale": Scytale,
    "SimpleSubstitution": SimpleSubstitution,
    "ThreeSquare": ThreeSquare,
    "Trifid": Trifid,
    "TwoSquare": TwoSquare,
    "Vic": Vic,
    "Vigenere": Vigenere,
    "Zigzag": Zigzag,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ADFGX": "ADFGX Cipher",
    "ADFGVX": "ADFGVX Cipher",
    "Affine": "Affine Cipher",
    "Atbash": "Atbash (Reverse Alphabet) Cipher",
    "Autokey": "Autokey Cipher",
    "Bazeries": "Bazeries Cipher",
    "Beaufort": "Beaufort Cipher",
    "Bifid": "Bifid Cipher",
    "Caesar": "Caesar (ROT) Cipher",
    "CaesarProg": "Progressive Caesar Cipher",
    "Chaocipher": "Chao Cipher",
    "ColTrans": "Columnar Transposition Cipher",
    "Foursquare": "Foursquare Cipher",
    "Gronsfeld": "Gronsfeld Cipher",
    "Keyword": "Keyword Cipher",
    "MyszkowskiTransposition": "Myszkowski Transposition Cipher",
    "Nihilist": "Nihilist Cipher",
    "Playfair": "Playfair Cipher",
    "Polybius": "Polybius Square Cipher",
    "Porta": "Porta Cipher",
    "Rot13": "Rotate-13 Cipher",
    "Rot5": "Rotate-5 Cipher",
    "Rot18": "Rotate-18 Cipher",
    "Rot47": "Rotate-47 Cipher",
    "Scytale": "Scytale Cipher",
    "SimpleSubstitution": "Simple Substitution Cipher",
    "ThreeSquare": "Three Square Cipher",
    "Trifid": "Trifid (Cylinder) Cipher",
    "TwoSquare": "Two Square (Double Playfair) Cipher",
    "Vic": "Vic Cipher",
    "Vigenere": "Vigenere Cipher",
    "Zigzag": "Zigzag (Rail-fence) Cipher",
}
