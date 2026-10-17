"""Focused tests for the Fernet symmetric encryption code path in fernet.py.

The FernetSimple node is a critical path for ARG solvers: it encrypts/decrypts
arbitrary text using a 32-byte Fernet key. Its complement, FernetKeygenSimple,
generates fresh keys. These code paths are exercised below with explicit
coverage of every branch (encrypt/decrypt), key generation, and error paths.
"""

import base64

import pytest
from cryptography import fernet
from cryptography.fernet import InvalidToken

from src.fernet import FernetKeygenSimple, FernetSimple


class TestFernetSimple:
    """Test suite covering the complete FernetSimple code path."""

    def test_encrypt_decrypt_roundtrip(self):
        """Encrypt then decrypt should return the original text."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "Hello World!"

        encrypted = node.execute(text, key, True)
        decrypted = node.execute(encrypted[0], key, False)

        assert decrypted[0] == text

    def test_encrypt_returns_fernet_token_format(self):
        """Encrypted output should be a valid Fernet token (base64-urlsafe)."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "Secret message"

        encrypted = node.execute(text, key, True)
        token = encrypted[0]

        # Fernet tokens are base64-urlsafe encoded and start with "gAAAAA"
        assert token.startswith("gAAAAA")
        # Should be valid base64-urlsafe
        decoded = base64.urlsafe_b64decode(token.encode("utf-8"))
        assert len(decoded) > 0

    def test_decrypt_with_wrong_key_raises(self):
        """Decrypting with a different key should raise an error."""
        node = FernetSimple()
        key1 = fernet.Fernet.generate_key()
        key2 = fernet.Fernet.generate_key()
        text = "Hello World!"

        encrypted = node.execute(text, key1, True)

        with pytest.raises(InvalidToken):
            node.execute(encrypted[0], key2, False)

    def test_encrypt_empty_string(self):
        """Encrypting an empty string should still produce a valid token."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()

        encrypted = node.execute("", key, True)
        decrypted = node.execute(encrypted[0], key, False)

        assert decrypted[0] == ""

    def test_encrypt_unicode_text(self):
        """Unicode text should round-trip correctly through Fernet."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "Hello 世界! 🌍"

        encrypted = node.execute(text, key, True)
        decrypted = node.execute(encrypted[0], key, False)

        assert decrypted[0] == text

    def test_encrypt_long_text(self):
        """Long text should round-trip correctly."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "A" * 10000

        encrypted = node.execute(text, key, True)
        decrypted = node.execute(encrypted[0], key, False)

        assert decrypted[0] == text

    def test_decrypt_tampered_token_raises(self):
        """Tampering with the token should cause decryption to fail."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "Hello World!"

        encrypted = node.execute(text, key, True)
        token = encrypted[0]
        # Tamper: flip a character in the middle
        tampered = token[:10] + ("A" if token[10] != "A" else "B") + token[11:]

        with pytest.raises(InvalidToken):
            node.execute(tampered, key, False)

    def test_encrypt_decrypt_with_known_key(self):
        """Deterministic test with a known key and expected token prefix."""
        node = FernetSimple()
        # A known 32-byte key (urlsafe base64 encoded)
        key = base64.urlsafe_b64encode(b"0" * 32)
        text = "Test"

        encrypted = node.execute(text, key, True)
        # Fernet token should start with version byte 'gAAAAA'
        assert encrypted[0].startswith("gAAAAA")

        decrypted = node.execute(encrypted[0], key, False)
        assert decrypted[0] == text

    def test_decrypt_invalid_token_raises(self):
        """Decrypting a completely invalid token should raise InvalidToken."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()

        with pytest.raises(InvalidToken):
            node.execute("not-a-valid-token", key, False)

    def test_encrypt_decrypt_binary_content(self):
        """Text that looks like binary should round-trip correctly."""
        node = FernetSimple()
        key = fernet.Fernet.generate_key()
        text = "\x00\x01\x02\x03 binary \xff\xfe\xfd"

        encrypted = node.execute(text, key, True)
        decrypted = node.execute(encrypted[0], key, False)

        assert decrypted[0] == text


class TestFernetKeygenSimple:
    """Test suite covering the FernetKeygenSimple code path."""

    def test_generate_key_returns_bytes(self):
        """Generated key should be a string suitable for Fernet."""
        node = FernetKeygenSimple()
        result = node.execute()

        assert isinstance(result[0], bytes)

    def test_generate_key_is_valid_fernet_key(self):
        """Generated key should be usable by Fernet for encryption."""
        node = FernetKeygenSimple()
        result = node.execute()
        key = result[0]

        # A valid Fernet key is 32 bytes urlsafe-base64 encoded
        assert isinstance(key, bytes)
        decoded = base64.urlsafe_b64decode(key)
        assert len(decoded) == 32

    def test_generate_key_uniqueness(self):
        """Two generated keys should be different."""
        node = FernetKeygenSimple()
        key1 = node.execute()[0]
        key2 = node.execute()[0]

        assert key1 != key2

    def test_generated_key_works_with_fernet_simple(self):
        """A generated key should work with FernetSimple for round-trip."""
        keygen = FernetKeygenSimple()
        cipher_node = FernetSimple()

        key = keygen.execute()[0]
        text = "Round-trip test"

        encrypted = cipher_node.execute(text, key, True)
        decrypted = cipher_node.execute(encrypted[0], key, False)

        assert decrypted[0] == text

    def test_generate_key_is_properly_encoded(self):
        """Generated key should be valid urlsafe base64."""
        node = FernetKeygenSimple()
        result = node.execute()
        key = result[0]

        # Should not raise - valid urlsafe base64
        decoded = base64.urlsafe_b64decode(key)
        assert len(decoded) == 32
