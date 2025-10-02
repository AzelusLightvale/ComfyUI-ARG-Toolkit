#!/usr/bin/env python

import pytest
import unicodedata
from src.comfyui_arg_toolkit import ciphers
from src.comfyui_arg_toolkit import utils
from src.comfyui_arg_toolkit.cryptography_primitives import auth_encrypt
from src.comfyui_arg_toolkit.cryptography_primitives import hashing
from src.comfyui_arg_toolkit import morse_code

# The entire test suite is designed to be as close to what a regular user would input into the nodes. This means that, for the most part, the test suite will not attempt to test for every edge cases, but rather to test for the most common use cases.
# For the most part, the test suite will not attempt to test for every edge cases, but rather to test for the most common use cases.

# For more information on how the test suite is designed, please refer to the README.md file.


# Test suite for ciphers.py
class TestCiphers:
    def test_atbash_cipher(self):
        atbash_cipher = ciphers.Atbash()
        text = "Hello World"
        alphabet = "ENGLISH"
        encrypted_text = atbash_cipher.atbash(text, alphabet, True, False)
        decrypted_text = atbash_cipher.atbash(encrypted_text[0], alphabet, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_caesar_cipher(self):
        caesar_cipher = ciphers.Caesar()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = 3
        encrypted_text = caesar_cipher.caesar(text, alphabet, key, True, False)
        decrypted_text = caesar_cipher.caesar(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_vigenere_cipher(self):
        vigenere_cipher = ciphers.Vigenere()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = vigenere_cipher.vigenere(text, alphabet, key, True, False)
        decrypted_text = vigenere_cipher.vigenere(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_adfgx_cipher(self):
        adfgx_cipher = ciphers.ADFGX()
        text = "HelloWorld"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key = "KEY"
        encrypted_text = adfgx_cipher.adfgx(text, alphabet, key, True, False)
        decrypted_text = adfgx_cipher.adfgx(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower()

    def test_autokey_cipher(self):
        autokey_cipher = ciphers.Autokey()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = autokey_cipher.autokey(text, alphabet, key, True, False)
        decrypted_text = autokey_cipher.autokey(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_beaufort_cipher(self):
        beaufort_cipher = ciphers.Beaufort()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = beaufort_cipher.beaufort(text, alphabet, key, True, False)
        decrypted_text = beaufort_cipher.beaufort(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_caesarprog_cipher(self):
        caesarprogessive_cipher = ciphers.CaesarProgressive()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = 3
        encrypted_text = caesarprogessive_cipher.caesarprogressive(
            text, alphabet, key, True, False
        )
        decrypted_text = caesarprogessive_cipher.caesarprogressive(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_rot13_cipher(self):
        rot13_cipher = ciphers.Rot13()
        text = "Hello World"
        alphabet = "ENGLISH"
        encrypted_text = rot13_cipher.rot13(text, alphabet, 13, True, False)
        decrypted_text = rot13_cipher.rot13(
            encrypted_text[0], alphabet, 13, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_scytale_cipher(self):
        scytale_cipher = ciphers.Scytale()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = 4
        encrypted_text = scytale_cipher.scytale(text, alphabet, key, True, False)
        decrypted_text = scytale_cipher.scytale(
            encrypted_text[0], alphabet, key, False, False
        )
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_playfair_cipher(self):
        playfair_cipher = ciphers.Playfair()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key = "KEYWORD"
        encrypted_text = playfair_cipher.playfair(text, alphabet, key, True, False)
        decrypted_text = playfair_cipher.playfair(
            encrypted_text[0], alphabet, key, False, False
        )
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_foursquare_cipher(self):
        foursquare_cipher = ciphers.FourSquare()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key_1 = "KEYONE"
        key_2 = "KEYTWO"
        encrypted_text = foursquare_cipher.foursquare(
            text, alphabet, key_1, key_2, True, False
        )
        decrypted_text = foursquare_cipher.foursquare(
            encrypted_text[0], alphabet, key_1, key_2, False, False
        )
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_twosquare_cipher(self):
        twosquare_cipher = ciphers.TwoSquare()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key_1 = "KEYONE"
        key_2 = "KEYTWO"
        encrypted_text = twosquare_cipher.twosquare(
            text, alphabet, key_1, key_2, True, False
        )
        decrypted_text = twosquare_cipher.twosquare(
            encrypted_text[0], alphabet, key_1, key_2, False, False
        )
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_gronsfeld_cipher(self):
        gronsfeld_cipher = ciphers.Gronsfeld()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "1337"
        encrypted_text = gronsfeld_cipher.gronsfeld(text, alphabet, key, True, False)
        decrypted_text = gronsfeld_cipher.gronsfeld(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_trifid_cipher(self):
        trifid_cipher = ciphers.Trifid()
        text = "HelloWorld"
        # Trifid in secretpy uses a 27-char alphabet (letters + separator)
        alphabet = "abcdefghijklmnopqrstuvwxyz."
        key = 5  # period
        encrypted_text = trifid_cipher.trifid(text, alphabet, key, True, False)
        decrypted_text = trifid_cipher.trifid(
            encrypted_text[0], alphabet, key, False, False
        )
        assert decrypted_text[0] == text.lower()

    def test_zigzag_cipher(self):
        zigzag_cipher = ciphers.Zigzag()
        text = "Hello World"
        key = 4  # rails
        # The node wrapper for Zigzag doesn't use an alphabet, it's a pure transposition
        encrypted_text = zigzag_cipher.zigzag(text, key, True, False)
        decrypted_text = zigzag_cipher.zigzag(encrypted_text[0], key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")


# Test suite for utils.py
class TestUtils:
    # Converters
    def test_string_to_binary(self):
        string_to_binary = utils.String2Binary()
        text = "Hello World"
        encoding = "utf-8"
        binary_text = string_to_binary.string2binary(text, encoding, "")
        assert (
            binary_text[0]
            == "1001000 1100101 1101100 1101100 1101111 100000 1010111 1101111 1110010 1101100 1100100"
        )

    def test_binary_to_string(self):
        binary_to_string = utils.Binary2String()
        binary_text = "1001000 1100101 1101100 1101100 1101111 100000 1010111 1101111 1110010 1101100 1100100"
        encoding = "utf-8"
        text = binary_to_string.binary2string(binary_text, encoding, "")
        assert text[0] == "Hello World"

    def test_string_to_hex(self):
        string_to_hex = utils.String2Hex()
        text = "Hello World"
        encoding = "utf-8"
        hex_text = string_to_hex.string2hex(text, encoding, "")
        assert hex_text[0] == "48656c6c6f20576f726c64"

    def test_hex_to_string(self):
        hex_to_string = utils.Hex2String()
        hex_text = "48656c6c6f20576f726c64"
        encoding = "utf-8"
        text = hex_to_string.hex2string(hex_text, encoding, "")
        assert text[0] == "Hello World"

    def test_string_to_base64(self):
        string_to_base64 = utils.String2Base64()
        text = "Hello World"
        encoding = "utf-8"
        base64_text = string_to_base64.string2base64(text, encoding, "")
        assert base64_text[0] == "SGVsbG8gV29ybGQ="

    def test_base64_to_string(self):
        base64_to_string = utils.Base642String()
        base64_text = "SGVsbG8gV29ybGQ="
        encoding = "utf-8"
        text = base64_to_string.base642string(base64_text, encoding, "")
        assert text[0] == "Hello World"

    # Bitwise Operators
    def test_bitwise_and(self):
        bitwise_and = utils.BitwiseAND()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_and.bitwiseand(text1, text2, encoding, "")
        assert result[0] == "6065606c64"

    def test_bitwise_or(self):
        bitwise_or = utils.BitwiseOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_or.bitwiseor(text1, text2, encoding, "")
        assert result[0] == "7f6f7e6c6f"

    def test_bitwise_xor(self):
        bitwise_xor = utils.BitwiseXOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_xor.bitwisexor(text1, text2, encoding, "")
        assert result[0] == "1f0a1e000b"

    def test_bitwise_not(self):
        bitwise_not = utils.BitwiseNOT()
        text = "68656c6c6f"
        encoding = "utf-8"
        result = bitwise_not.bitwisenot(text, encoding, "")
        assert result[0] == "979a939390"


# Test suite for auth_encrypt.py
class TestAuthEncrypt:
    def test_chacha20poly1305(self):
        chacha20poly1305 = auth_encrypt.ChaCha20Poly1305()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = chacha20poly1305.cc20(text, key, nonce, associated_data, True)
        decrypted_text = chacha20poly1305.cc20(
            encrypted_text[0], key, nonce, associated_data, False
        )
        assert decrypted_text[0] == text

    def test_aes_gcm(self):
        aes_gcm = auth_encrypt.AESAuth()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = aes_gcm.aesauth(
            text, key, nonce, associated_data, True, "AES-GCM", 16
        )
        decrypted_text = aes_gcm.aesauth(
            encrypted_text[0], key, nonce, associated_data, False, "AES-GCM", 16
        )
        assert decrypted_text[0] == text

    def test_aes_ccm(self):
        aes_ccm = auth_encrypt.AESAuth()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = aes_ccm.aesauth(
            text, key, nonce, associated_data, True, "AES-CCM", 16
        )
        decrypted_text = aes_ccm.aesauth(
            encrypted_text[0], key, nonce, associated_data, False, "AES-CCM", 16
        )
        assert decrypted_text[0] == text


# Test suite for hashing.py
class TestHashing:
    def test_sha256(self):
        sha256 = hashing.SHA2()
        text = "Hello World"
        hashed_text = (sha256.sha2(key1=text, algorithm="SHA256"),)
        assert (
            hashed_text[0][0]
            == "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        )

    def test_blake2b(self):
        blake2b = hashing.BLAKE2()
        text = "Hello World"
        hashed_text = blake2b.blake2(key1=text, algorithm="BLAKE2b", digest_size=64)
        assert (
            hashed_text[0]
            == "4386a08a265111c9896f56456e2cb61a64239115c4784cf438e36cc851221972da3fb0115f73cd02486254001f878ab1fd126aac69844ef1c1ca152379d0a9bd"
        )

    def test_sha3_256(self):
        sha3_256 = hashing.SHA3()
        text = "Hello World"
        hashed_text = (sha3_256.sha3(key1=text, algorithm="SHA3_256"),)
        assert (
            hashed_text[0][0]
            == "e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51"
        )

    def test_sha1(self):
        sha1 = hashing.SHA1()
        text = "Hello World"
        hashed_text = (sha1.sha1(key1=text, algorithm=None),)
        assert hashed_text[0][0] == "0a4d55a8d778e5022fab701977c5d840bbc486d0"

    def test_md5(self):
        md5 = hashing.MD5()
        text = "Hello World"
        hashed_text = (md5.md5(key1=text, algorithm=None),)
        assert hashed_text[0][0] == "b10a8db164e0754105b7a99be72e3fe5"

    def test_sm3(self):
        sm3 = hashing.SM3()
        text = "Hello World"
        hashed_text = (sm3.sm3(key1=text, algorithm=None),)
        assert (
            hashed_text[0][0]
            == "77015816143ee627f4fa410b6dad2bdb9fcbdf1e061a452a686b8711a484c5d7"
        )

    def test_shake128(self):
        shake128 = hashing.SHAKE()
        text = "Hello World"
        hashed_text = shake128.shake(
            key1=text,
            algorithm="SHAKE128",
            output_length=32,
            digest_size=64,
            squeeze_bytes=16,
            squeeze_times=2,
        )
        assert (
            hashed_text[0][0]
            == "7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef263cb1eea988004b93103cfb0aeefd2a686e01fa4a58e8a3639ca8a1e3f9ae57e2"
        )


# Test suite for morse_code.py
class TestMorseCode:
    def setup_method(self):
        self.morse_code = morse_code.MorseCode()

    def test_latin_morse_code(self):
        text = "Hello World"
        encoded_text = self.morse_code.MorseCode(text, True, "latin", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "latin", ".", "-"
        )
        assert decoded_text[0].lower() == text.lower()

    def test_russian_morse_code(self):
        text = "Привет мир"
        encoded_text = self.morse_code.MorseCode(text, True, "russian", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "russian", ".", "-"
        )
        assert decoded_text[0].lower() == text.lower()

    def test_arabic_morse_code(self):
        text = "مرحبا بالعالم"
        encoded_text = self.morse_code.MorseCode(text, True, "arabic", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "arabic", ".", "-"
        )
        assert decoded_text[0] == text

    def test_hebrew_morse_code(self):
        text = "שלום עולם"
        encoded_text = self.morse_code.MorseCode(text, True, "hebrew", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "hebrew", ".", "-"
        )
        assert decoded_text[0] == "שלומ עולמ"

    def test_greek_morse_code(self):
        text = "Γειά σου Κόσμε"
        encoded_text = self.morse_code.MorseCode(text, True, "greek", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "greek", ".", "-"
        )
        assert decoded_text[0] == "ΓΕΙΑ ΣΟΥ ΚΟΣΜΕ"

    def test_korean_morse_code(self):
        text = "안녕하세요"
        encoded_text = self.morse_code.MorseCode(text, True, "korean", ".", "-")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "korean", ".", "-"
        )
        assert decoded_text[0] == "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"

    def test_japanese_wabun_morse_code(self):
        text = "こんにちは"
        normalized_text = unicodedata.normalize("NFKC", text)
        print(f"Normalized text: {normalized_text}")
        encoded_text = self.morse_code.MorseCode(text, True, "japanese-wabun", ".", "-")
        print(f"Encoded text: {encoded_text}")
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "japanese-wabun", ".", "-"
        )
        print(f"Decoded text: {decoded_text}")
        assert decoded_text == ("コンニチハ",)

    def test_custom_dot_dash_morse_code(self):
        text = "Hello World"
        dot = "1"
        dash = "0"
        encoded_text = self.morse_code.MorseCode(text, True, "latin", dot, dash)
        decoded_text = self.morse_code.MorseCode(
            encoded_text[0], False, "latin", dot, dash
        )
        assert decoded_text[0].lower() == text.lower()
