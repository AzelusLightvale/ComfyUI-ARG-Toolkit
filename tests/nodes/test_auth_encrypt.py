from src.cryptography_primitives import auth_encrypt


# Test suite for auth_encrypt.py
class TestAuthEncrypt:
    def test_chacha20poly1305(self):
        chacha20poly1305 = auth_encrypt.ChaCha20Poly1305()
        text = b"Hello World"
        key = b"0" * 32
        nonce = b"0" * 12
        associated_data = b""
        encrypted_text = chacha20poly1305.cc20(text, key, nonce, associated_data, True)
        decrypted_text = chacha20poly1305.cc20(encrypted_text[0], key, nonce, associated_data, False)
        assert decrypted_text[0] == text

    def test_aes_gcm(self):
        aes_gcm = auth_encrypt.AESAuth()
        text = b"Hello World"
        key = b"0" * 32
        nonce = b"0" * 12
        associated_data = b""
        encrypted_text = aes_gcm.aesauth(text, key, nonce, associated_data=associated_data, mode=True, aes_type="AES-GCM", ccm_tag_length=16)
        decrypted_text = aes_gcm.aesauth(encrypted_text[0], key, nonce, associated_data=associated_data, mode=False, aes_type="AES-GCM", ccm_tag_length=16)
        assert decrypted_text[0] == text

    def test_aes_ccm(self):
        aes_gcm = auth_encrypt.AESAuth()
        text = b"Hello World"
        key = b"0" * 32
        nonce = b"0" * 12
        associated_data = b""
        encrypted_text = aes_gcm.aesauth(text, key, nonce, associated_data=associated_data, mode=True, aes_type="AES-CCM", ccm_tag_length=16)
        decrypted_text = aes_gcm.aesauth(encrypted_text[0], key, nonce, associated_data=associated_data, mode=False, aes_type="AES-CCM", ccm_tag_length=16)
        assert decrypted_text[0] == text

    def test_aes_siv(self):
        aes_siv = auth_encrypt.AESAuth()
        text = b"Hello World"
        key = b"0" * 32
        nonce = b"0" * 12
        associated_data = b""
        encrypted_text = aes_siv.aesauth(text, key, nonce, associated_data=associated_data, mode=True, aes_type="AES-SIV", ccm_tag_length=16)
        decrypted_text = aes_siv.aesauth(encrypted_text[0], key, nonce, associated_data=associated_data, mode=False, aes_type="AES-SIV", ccm_tag_length=16)
        assert decrypted_text[0] == text
