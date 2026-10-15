from src.cryptography_primitives import const_time
from src.cryptography_primitives import kdf
from src.cryptography_primitives import key_wrapper
from src.cryptography_primitives import symm_padding
from src.cryptography_primitives import symmetrical_encrypt


class TestConstantTimeCompare:
    def test_compare_equal(self):
        compare = const_time.ConstantTimeCompare()
        a = b"deadbeef"
        b = b"deadbeef"
        result = compare.compare(a, b)
        assert result[0] is True

    def test_compare_not_equal(self):
        compare = const_time.ConstantTimeCompare()
        a = b"deadbeef"
        b = b"cafebabe"
        result = compare.compare(a, b)
        assert result[0] is False


class TestKeyDerivation:
    def test_argon2id_derive_verify(self):
        derive = kdf.Argon2id_Derive()
        verify = kdf.Argon2id_Verify()

        message = b"Hello World"
        salt = b"00" * 16

        derived_key = derive.execute(message, 32, salt, 1, 4, 65536, b"", b"", True)

        verified = verify.execute(message, 32, salt, 1, 4, 65536, b"", b"", True, derived_key[0])

        assert verified[0] is True

    def test_pbkdf2hmac_derive_verify(self):
        derive = kdf.PBKDF2HMAC_Derive()
        verify = kdf.PBKDF2HMAC_Verify()

        message = b"Hello World"
        salt = b"00" * 16

        derived_key = derive.execute(message, 32, salt, 1000, "SHA256")

        verified = verify.execute(message, 32, salt, 1000, "SHA256", derived_key[0])

        assert verified[0] is True

    def test_scrypt_derive_verify(self):
        derive = kdf.Scrypt_Derive()
        verify = kdf.Scrypt_Verify()

        message = b"Hello World"
        salt = b"00" * 16

        derived_key = derive.execute(message, 32, salt, 14, 8, 1)

        verified = verify.execute(message, 32, salt, 14, 8, 1, derived_key[0])

        assert verified[0] is True


class TestKeyWrapper:
    def test_aeskeywrap(self):
        wrapper = key_wrapper.AESKeyWrap()
        wrapping_key = bytes.fromhex("00" * 32)
        key_to_wrap = bytes.fromhex("11" * 16)

        wrapped_key = wrapper.execute(wrapping_key, key_to_wrap, True)
        unwrapped_key = wrapper.execute(wrapping_key, wrapped_key[0], False)

        assert unwrapped_key[0] == key_to_wrap

    def test_aeskeywrapwithpadding(self):
        wrapper = key_wrapper.AESKeyWrapWithPadding()
        wrapping_key = bytes.fromhex("00" * 32)
        key_to_wrap = bytes.fromhex("11" * 20)  # Not a multiple of 8

        wrapped_key = wrapper.execute(wrapping_key, key_to_wrap, True)
        unwrapped_key = wrapper.execute(wrapping_key, wrapped_key[0], False)

        assert unwrapped_key[0] == key_to_wrap


class TestSymmetricalPadding:
    def test_pkcs7_padding(self):
        padding_node = symm_padding.PaddingNode()
        data = b"Hello World"

        padded_data = padding_node.padding(data, 128, "PKCS7", True)
        unpadded_data = padding_node.padding(padded_data[0], 128, "PKCS7", False)

        assert unpadded_data[0] == data

    def test_ansix923_padding(self):
        padding_node = symm_padding.PaddingNode()
        data = b"Hello World"

        padded_data = padding_node.padding(data, 128, "ANSIX923", True)
        unpadded_data = padding_node.padding(padded_data[0], 128, "ANSIX923", False)

        assert unpadded_data[0] == data


class TestSymmetricalEncryption:
    def test_aes_cbc_encryption_decryption(self):
        enc_dec = symmetrical_encrypt.EncryptDecrypt()

        text = b"Hello World"
        key = bytes.fromhex("00" * 32)
        iv = bytes.fromhex("11" * 16)

        # Pad the text first
        padding_node = symm_padding.PaddingNode()
        padded_text = padding_node.padding(text, 128, "PKCS7", True)

        encrypted_text, _ = enc_dec.execute(padded_text[0], key, iv, None, "AES", "CBC", True, 16, None)

        decrypted_text_bytes, _ = enc_dec.execute(encrypted_text, key, iv, None, "AES", "CBC", False, 16, None)

        # Unpad the decrypted text
        unpadded_data = padding_node.padding(decrypted_text_bytes, 128, "PKCS7", False)

        assert unpadded_data[0] == text
