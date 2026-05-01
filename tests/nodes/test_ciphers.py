from src import ciphers

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
        decrypted_text = caesar_cipher.caesar(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_vigenere_cipher(self):
        vigenere_cipher = ciphers.Vigenere()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = vigenere_cipher.vigenere(text, alphabet, key, True, False)
        decrypted_text = vigenere_cipher.vigenere(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_adfgx_cipher(self):
        adfgx_cipher = ciphers.ADFGX()
        text = "HelloWorld"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key = "KEY"
        encrypted_text = adfgx_cipher.adfgx(text, alphabet, key, True, False)
        decrypted_text = adfgx_cipher.adfgx(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower()

    def test_autokey_cipher(self):
        autokey_cipher = ciphers.Autokey()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = autokey_cipher.autokey(text, alphabet, key, True, False)
        decrypted_text = autokey_cipher.autokey(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_beaufort_cipher(self):
        beaufort_cipher = ciphers.Beaufort()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "KEY"
        encrypted_text = beaufort_cipher.beaufort(text, alphabet, key, True, False)
        decrypted_text = beaufort_cipher.beaufort(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_caesarprog_cipher(self):
        caesarprogessive_cipher = ciphers.CaesarProgressive()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = 3
        encrypted_text = caesarprogessive_cipher.caesarprogressive(text, alphabet, key, True, False)
        decrypted_text = caesarprogessive_cipher.caesarprogressive(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_rot13_cipher(self):
        rot13_cipher = ciphers.Rot13()
        text = "Hello World"
        alphabet = "ENGLISH"
        encrypted_text = rot13_cipher.rot13(text, alphabet, 13, True, False)
        decrypted_text = rot13_cipher.rot13(encrypted_text[0], alphabet, 13, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_scytale_cipher(self):
        scytale_cipher = ciphers.Scytale()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = 4
        encrypted_text = scytale_cipher.scytale(text, alphabet, key, True, False)
        decrypted_text = scytale_cipher.scytale(encrypted_text[0], alphabet, key, False, False)
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_playfair_cipher(self):
        playfair_cipher = ciphers.Playfair()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key = "KEYWORD"
        encrypted_text = playfair_cipher.playfair(text, alphabet, key, True, False)
        decrypted_text = playfair_cipher.playfair(encrypted_text[0], alphabet, key, False, False)
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_foursquare_cipher(self):
        foursquare_cipher = ciphers.FourSquare()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key_1 = "KEYONE"
        key_2 = "KEYTWO"
        encrypted_text = foursquare_cipher.foursquare(text, alphabet, key_1, key_2, True, False)
        decrypted_text = foursquare_cipher.foursquare(encrypted_text[0], alphabet, key_1, key_2, False, False)
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_twosquare_cipher(self):
        twosquare_cipher = ciphers.TwoSquare()
        text = "Hello World"
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j
        key_1 = "KEYONE"
        key_2 = "KEYTWO"
        encrypted_text = twosquare_cipher.twosquare(text, alphabet, key_1, key_2, True, False)
        decrypted_text = twosquare_cipher.twosquare(encrypted_text[0], alphabet, key_1, key_2, False, False)
        # secretpy may add padding, so check for inclusion
        assert text.lower().replace(" ", "") in decrypted_text[0]

    def test_gronsfeld_cipher(self):
        gronsfeld_cipher = ciphers.Gronsfeld()
        text = "Hello World"
        alphabet = "ENGLISH"
        key = "1337"
        encrypted_text = gronsfeld_cipher.gronsfeld(text, alphabet, key, True, False)
        decrypted_text = gronsfeld_cipher.gronsfeld(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")

    def test_trifid_cipher(self):
        trifid_cipher = ciphers.Trifid()
        text = "HelloWorld"
        # Trifid in secretpy uses a 27-char alphabet (letters + separator)
        alphabet = "abcdefghijklmnopqrstuvwxyz."
        key = 5  # period
        encrypted_text = trifid_cipher.trifid(text, alphabet, key, True, False)
        decrypted_text = trifid_cipher.trifid(encrypted_text[0], alphabet, key, False, False)
        assert decrypted_text[0] == text.lower()

    def test_zigzag_cipher(self):
        zigzag_cipher = ciphers.Zigzag()
        text = "Hello World"
        key = 4  # rails
        # The node wrapper for Zigzag doesn't use an alphabet, it's a pure transposition
        encrypted_text = zigzag_cipher.zigzag(text, key, True, False)
        decrypted_text = zigzag_cipher.zigzag(encrypted_text[0], key, False, False)
        assert decrypted_text[0] == text.lower().replace(" ", "")
