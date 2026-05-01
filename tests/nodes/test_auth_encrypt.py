from src.cryptography_primitives import auth_encrypt

# Test suite for auth_encrypt.py
class TestAuthEncrypt:
    def test_chacha20poly1305(self):
        chacha20poly1305 = auth_encrypt.ChaCha20Poly1305()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = chacha20poly1305.cc20(text, key, nonce, associated_data, True)
        decrypted_text = chacha20poly1305.cc20(encrypted_text[0], key, nonce, associated_data, False)
        assert decrypted_text[0] == text

    def test_aes_gcm(self):
        aes_gcm = auth_encrypt.AESAuth()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = aes_gcm.aesauth(text, key, nonce, associated_data, True, "AES-GCM", 16)
        decrypted_text = aes_gcm.aesauth(encrypted_text[0], key, nonce, associated_data, False, "AES-GCM", 16)
        assert decrypted_text[0] == text

    def test_aes_ccm(self):
        aes_ccm = auth_encrypt.AESAuth()
        text = "Hello World"
        key = "0" * 64
        nonce = "0" * 24
        associated_data = ""
        encrypted_text = aes_ccm.aesauth(text, key, nonce, associated_data, True, "AES-CCM", 16)
        decrypted_text = aes_ccm.aesauth(encrypted_text[0], key, nonce, associated_data, False, "AES-CCM", 16)
        assert decrypted_text[0] == text
