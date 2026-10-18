"""Focused tests for the ``asymmetric_encryption`` node suite.
"""

import hashlib

import math

import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa as c_rsa

from src.cryptography_primitives.asymmetric_encryption import eddsa
from src.cryptography_primitives.asymmetric_encryption import elliptic_curve
from src.cryptography_primitives.asymmetric_encryption import rsa
from src.cryptography_primitives.asymmetric_encryption import serialization as key_serialization
from src.cryptography_primitives.asymmetric_encryption import xdh


# ---------------------------------------------------------------------------
# EdDSA
# ---------------------------------------------------------------------------


class TestEdDSAKeyFormat:
    def test_private_key_format_pem_pkcs8_unencrypted(self):
        priv_bytes, priv_key = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "PEM", "PKCS8", "None", "")
        assert isinstance(priv_bytes, bytes)
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert priv_key is not None

    def test_private_key_format_raw_roundtrip(self):
        priv_bytes, priv_key = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "Raw", "Raw", "None", "")
        assert len(priv_bytes) == 32
        assert priv_key.private_bytes_raw() == priv_bytes

    def test_private_key_format_best_available_without_password_does_not_crash(self):
        # "Best Available" is the node default; with no password it must fall
        # back to an unencrypted key instead of raising UnboundLocalError.
        priv_bytes, priv_key = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "PEM", "PKCS8", "Best Available", "")
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert priv_key is not None

    def test_private_key_format_encrypted_best_available(self):
        priv_bytes, _ = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "PEM", "PKCS8", "Best Available", "hunter2")
        assert priv_bytes.startswith(b"-----BEGIN ENCRYPTED PRIVATE KEY-----")
        loaded = serialization.load_pem_private_key(priv_bytes, b"hunter2")
        assert loaded is not None

    def test_get_private_key_unsupported_type_raises(self):
        with pytest.raises(ValueError, match="Unsupported key type"):
            eddsa.InitNode.get_private_key("Fresh Key", "Bogus")

    def test_get_private_key_from_bytes_requires_bytes(self):
        with pytest.raises(ValueError, match="Private key bytes are required"):
            eddsa.InitNode.get_private_key("From Private Bytes", "Ed25519", None)

    def test_get_private_key_from_bytes_roundtrip(self):
        _, priv_key = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "Raw", "Raw", "None", "")
        raw = priv_key.private_bytes_raw()
        reloaded = eddsa.InitNode.get_private_key("From Private Bytes", "Ed25519", raw)
        assert reloaded.private_bytes_raw() == raw


class TestEdDSASignature:
    def _key(self):
        return eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "PEM", "PKCS8", "None", "")[1]

    def test_sign_fresh_key(self):
        signature = eddsa.EdDSASignature().execute("Fresh Key", "Ed25519", "Hello World", None, None)[0]
        assert isinstance(signature, bytes)
        assert len(signature) == 64

    def test_sign_from_private_bytes(self):
        _, priv_key = eddsa.EdDSAPrivateKeyFormat().execute("Ed25519", "Raw", "Raw", "None", "")
        signature = eddsa.EdDSASignature().execute("From Private Bytes", "Ed25519", "Hello World", None, priv_key.private_bytes_raw())[0]
        assert len(signature) == 64

    def test_sign_from_loaded_key(self):
        priv_key = self._key()
        signature = eddsa.EdDSASignature().execute("From Loaded Key", "Ed25519", "Hello World", priv_key, None)[0]
        assert len(signature) == 64

    def test_sign_and_verify_roundtrip(self):
        priv_key = self._key()
        signature = eddsa.EdDSASignature().execute("From Loaded Key", "Ed25519", "Hello World", priv_key, None)[0]
        result = eddsa.EdDSAVerify().execute(
            "Ed25519",
            priv_key.public_key().public_bytes_raw(),
            None,
            b"Hello World",
            signature,
            True,
        )
        assert result[0] is True

    def test_verify_rejects_tampered_message(self):
        priv_key = self._key()
        signature = eddsa.EdDSASignature().execute("From Loaded Key", "Ed25519", "Hello World", priv_key, None)[0]
        result = eddsa.EdDSAVerify().execute(
            "Ed25519",
            priv_key.public_key().public_bytes_raw(),
            None,
            b"Hello World!",
            signature,
            True,
        )
        assert result[0] is False

    def test_verify_from_loaded_key(self):
        priv_key = self._key()
        signature = eddsa.EdDSASignature().execute("From Loaded Key", "Ed25519", "Hello World", priv_key, None)[0]
        result = eddsa.EdDSAVerify().execute("Ed25519", None, priv_key.public_key(), b"Hello World", signature, False)
        assert result[0] is True

    def test_public_key_format_raw(self):
        pub_bytes, pub_key = eddsa.EdDSAPublicKeyFormat().execute("Fresh Key", "Ed25519", "Raw", "Raw", None, None)
        assert len(pub_bytes) == 32
        assert pub_key.public_bytes_raw() == pub_bytes

    def test_public_key_format_pem(self):
        pub_bytes, _ = eddsa.EdDSAPublicKeyFormat().execute("Fresh Key", "Ed25519", "PEM", "SubjectPublicKeyInfo", None, None)
        assert pub_bytes.startswith(b"-----BEGIN PUBLIC KEY-----")


# ---------------------------------------------------------------------------
# Elliptic curve
# ---------------------------------------------------------------------------


class TestEllipticCurve:
    def test_e_curve_standard_name(self):
        assert elliptic_curve.EllipticCurve().e_curve("SECP256R1") is not None

    def test_e_curve_brainpool_prefix_mapping(self):
        curve = elliptic_curve.EllipticCurve().e_curve("BRAINPOOLP256R1")
        assert curve.__name__ == "BrainpoolP256R1"

    def test_private_key_generate_unencrypted(self):
        priv_bytes, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "")
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert priv_key is not None

    def test_private_key_from_private_value(self):
        _, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "12345")
        assert priv_key.private_numbers().private_value == 12345

    def test_public_key_from_fresh(self):
        pub_bytes, pub_key = elliptic_curve.ECPublicKey().execute("SECP256R1", True, None, "PEM", "SubjectPublicKeyInfo")
        assert pub_bytes.startswith(b"-----BEGIN PUBLIC KEY-----")
        assert pub_key is not None

    def test_public_key_from_loaded_key(self):
        _, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "")
        pub_bytes, pub_key = elliptic_curve.ECPublicKey().execute("SECP256R1", False, priv_key, "PEM", "SubjectPublicKeyInfo")
        assert pub_bytes.startswith(b"-----BEGIN PUBLIC KEY-----")
        assert pub_key.public_numbers() == priv_key.public_key().public_numbers()

    def test_sign_and_verify_roundtrip(self):
        _, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "")
        signature = elliptic_curve.ECSign().execute(priv_key, b"payload", "SHA256", False)[0]
        assert elliptic_curve.ECVerify().execute(priv_key.public_key(), signature, b"payload", "SHA256", False)[0] is True

    def test_verify_rejects_wrong_message(self):
        _, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "")
        signature = elliptic_curve.ECSign().execute(priv_key, b"payload", "SHA256", False)[0]
        assert elliptic_curve.ECVerify().execute(priv_key.public_key(), signature, b"other", "SHA256", False)[0] is False

    def test_sign_and_verify_prehashed(self):
        _, priv_key = elliptic_curve.ECPrivateKey().execute("SECP256R1", "PKCS8", "PEM", "None", "", "")
        digest = hashlib.sha256(b"payload").digest()
        signature = elliptic_curve.ECSign().execute(priv_key, digest, "SHA256", True)[0]
        assert elliptic_curve.ECVerify().execute(priv_key.public_key(), signature, digest, "SHA256", True)[0] is True


# ---------------------------------------------------------------------------
# X25519 / X448 key exchange
# ---------------------------------------------------------------------------


class TestXDH:
    def test_private_key_format_unencrypted(self):
        priv_bytes, priv_key = xdh.XPrivateKeyFormat().execute("x25519", "PEM", "PKCS8", "None", "")
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert priv_key is not None

    def test_private_key_format_raw(self):
        priv_bytes, _ = xdh.XPrivateKeyFormat().execute("x25519", "Raw", "Raw", "None", "")
        assert len(priv_bytes) == 32

    def test_private_key_format_best_available_without_password_does_not_crash(self):
        priv_bytes, _ = xdh.XPrivateKeyFormat().execute("x25519", "PEM", "PKCS8", "Best Available", "")
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")

    def test_public_key_format_from_private_bytes(self):
        priv_bytes, _ = xdh.XPrivateKeyFormat().execute("x25519", "Raw", "Raw", "None", "")
        pub_bytes, pub_key = xdh.XPublicKeyFormat().execute(False, "x25519", "Raw", "Raw", priv_bytes)
        assert len(pub_bytes) == 32
        assert pub_key.public_bytes_raw() == pub_bytes

    def test_exchange_shared_secret_matches_both_sides(self):
        a_priv = xdh.XPrivateKeyFormat().execute("x25519", "Raw", "Raw", "None", "")[1]
        b_priv = xdh.XPrivateKeyFormat().execute("x25519", "Raw", "Raw", "None", "")[1]
        a_pub = a_priv.public_key().public_bytes_raw()
        b_pub = b_priv.public_key().public_bytes_raw()
        shared_a = xdh.XExchange().execute(False, "x25519", b_pub, a_priv.private_bytes_raw())[0]
        shared_b = xdh.XExchange().execute(False, "x25519", a_pub, b_priv.private_bytes_raw())[0]
        assert shared_a == shared_b
        assert len(shared_a) == 32

    def test_exchange_with_fresh_key(self):
        priv = xdh.XPrivateKeyFormat().execute("x25519", "Raw", "Raw", "None", "")[1]
        shared = xdh.XExchange().execute(True, "x25519", priv.public_key().public_bytes_raw(), None)[0]
        assert isinstance(shared, bytes)

    def test_get_private_key_unsupported_type_raises(self):
        with pytest.raises(ValueError, match="Unsupported key type"):
            xdh.InitNode.get_private_key(True, "bogus")

    def test_get_private_key_from_bytes_requires_bytes(self):
        with pytest.raises(ValueError, match="Private key bytes are required"):
            xdh.InitNode.get_private_key(False, "x25519", None)


# ---------------------------------------------------------------------------
# Key serialization / loading
# ---------------------------------------------------------------------------


class TestKeySerializationLoaders:
    @pytest.fixture
    def rsa_key(self):
        return c_rsa.generate_private_key(65537, 2048)

    def test_pem_private_key(self, rsa_key):
        pem = rsa_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        loaded = key_serialization.PEMPrivateKey().execute(pem, None)[0]
        assert loaded.private_numbers() == rsa_key.private_numbers()

    def test_pem_private_key_with_password(self, rsa_key):
        pem = rsa_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.BestAvailableEncryption(b"pw"),
        )
        loaded = key_serialization.PEMPrivateKey().execute(pem, b"pw")[0]
        assert loaded.private_numbers() == rsa_key.private_numbers()

    def test_pem_public_key(self, rsa_key):
        pem = rsa_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        loaded = key_serialization.PEMPublicKey().execute(pem)[0]
        assert loaded.public_numbers() == rsa_key.public_key().public_numbers()

    def test_der_private_key(self, rsa_key):
        der = rsa_key.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        loaded = key_serialization.DERPrivateKey().execute(der, None)[0]
        assert loaded.private_numbers() == rsa_key.private_numbers()

    def test_der_public_key(self, rsa_key):
        der = rsa_key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        loaded = key_serialization.DERPublicKey().execute(der)[0]
        assert loaded.public_numbers() == rsa_key.public_key().public_numbers()

    def test_ssh_public_key(self, rsa_key):
        ssh = rsa_key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        loaded = key_serialization.SSHPublicKey().execute(ssh)[0]
        assert loaded.public_numbers() == rsa_key.public_key().public_numbers()

    def test_ssh_private_key(self, rsa_key):
        ssh = rsa_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.OpenSSH, serialization.NoEncryption())
        loaded = key_serialization.SSHPrivateKey().execute(ssh, None, False)[0]
        assert loaded.private_numbers() == rsa_key.private_numbers()

    def test_ssh_public_key_fingerprint_sha256(self, rsa_key):
        ssh = rsa_key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        fingerprint = key_serialization.SSHPublicKeyFingerprint().execute(ssh, "SHA-256")[0]
        expected = serialization.ssh_key_fingerprint(rsa_key.public_key(), hashes.SHA256())
        assert fingerprint == bytes(expected)

    def test_ssh_public_identity_returns_key(self, rsa_key):
        ssh = rsa_key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        certificate, key = key_serialization.SSHPublicIdentity().execute(ssh)
        assert certificate is None
        assert key.public_numbers() == rsa_key.public_key().public_numbers()


# ---------------------------------------------------------------------------
# RSA
# ---------------------------------------------------------------------------


class TestRSAKeyFormat:
    def test_private_key_format(self):
        key_obj, priv_bytes, numbers = rsa.RSAPrivateKeyFormat().execute(65537, 1024, "PEM", "PKCS8", "None", "")
        assert priv_bytes.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert key_obj.private_numbers() == numbers

    def test_public_key_format_from_fresh_key(self):
        key_obj, pub_bytes, numbers = rsa.RSAPublicKeyFormat().execute("Fresh Key", "PEM", "SubjectPublicKeyInfo", None, 1024, 65537)
        assert pub_bytes.startswith(b"-----BEGIN PUBLIC KEY-----")
        assert key_obj.public_numbers() == numbers

    def test_public_key_format_from_loaded_key(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        key_obj, pub_bytes, _ = rsa.RSAPublicKeyFormat().execute("From Loaded Key", "PEM", "SubjectPublicKeyInfo", priv, None, None)
        assert key_obj.public_numbers() == priv.public_key().public_numbers()
        assert pub_bytes.startswith(b"-----BEGIN PUBLIC KEY-----")

    def test_public_key_format_from_loaded_key_without_key_raises(self):
        with pytest.raises(ValueError, match="Missing private keys"):
            rsa.RSAPublicKeyFormat().execute("From Loaded Key", "PEM", "SubjectPublicKeyInfo", None, None, None)

    def test_public_key_format_rejects_non_private_key_object(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        with pytest.raises(ValueError, match="Missing private keys"):
            rsa.RSAPublicKeyFormat().execute("From Loaded Key", "PEM", "SubjectPublicKeyInfo", priv.public_key(), None, None)  # ty: ignore[invalid-argument-type]. Intended testing for wrong wiring.


class TestRSASignVerify:
    @pytest.fixture
    def rsa_key(self):
        return c_rsa.generate_private_key(65537, 2048)

    def test_pss_max_length_roundtrip(self, rsa_key):
        signature = rsa.RSASign().execute(rsa_key, b"payload", "Max Length", 0, "SHA256", "PSS", False)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), b"payload", signature, "Max Length", 0, "SHA256", "PSS", False)[0] is True

    def test_pss_digest_length_roundtrip(self, rsa_key):
        signature = rsa.RSASign().execute(rsa_key, b"payload", "Digest Length", 0, "SHA512", "PSS", False)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), b"payload", signature, "Digest Length", 0, "SHA512", "PSS", False)[0] is True

    def test_pss_manual_salt_length_roundtrip(self, rsa_key):
        signature = rsa.RSASign().execute(rsa_key, b"payload", "Manual", 20, "SHA256", "PSS", False)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), b"payload", signature, "Manual", 20, "SHA256", "PSS", False)[0] is True

    def test_pkcs1v15_roundtrip(self, rsa_key):
        signature = rsa.RSASign().execute(rsa_key, b"payload", "Max Length", 0, "SHA256", "PKCS1v15", False)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), b"payload", signature, "Max Length", 0, "SHA256", "PKCS1v15", False)[0] is True

    def test_verify_rejects_wrong_message(self, rsa_key):
        signature = rsa.RSASign().execute(rsa_key, b"payload", "Max Length", 0, "SHA256", "PSS", False)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), b"other", signature, "Max Length", 0, "SHA256", "PSS", False)[0] is False

    def test_prehashed_pss_roundtrip(self, rsa_key):
        digest = hashlib.sha256(b"payload").digest()
        signature = rsa.RSASign().execute(rsa_key, digest, "Max Length", 0, "SHA256", "PSS", True)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), digest, signature, "Max Length", 0, "SHA256", "PSS", True)[0] is True

    def test_pkcs1v15_prehashed_roundtrip(self, rsa_key):
        digest = hashlib.sha256(b"payload").digest()
        signature = rsa.RSASign().execute(rsa_key, digest, "Max Length", 0, "SHA256", "PKCS1v15", True)[0]
        assert rsa.RSAVerify().execute(rsa_key.public_key(), digest, signature, "Max Length", 0, "SHA256", "PKCS1v15", True)[0] is True

    def test_pkcs1v15_prehashed_verify_rejects_wrong_digest(self, rsa_key):
        digest = hashlib.sha256(b"payload").digest()
        signature = rsa.RSASign().execute(rsa_key, digest, "Max Length", 0, "SHA256", "PKCS1v15", True)[0]
        other = hashlib.sha256(b"other").digest()
        assert rsa.RSAVerify().execute(rsa_key.public_key(), other, signature, "Max Length", 0, "SHA256", "PKCS1v15", True)[0] is False


class TestRSAEncryptDecrypt:
    @pytest.fixture
    def rsa_key(self):
        return c_rsa.generate_private_key(65537, 2048)

    def test_oaep_roundtrip(self, rsa_key):
        ciphertext = rsa.RSAEncrypt().execute(rsa_key.public_key(), b"secret", "SHA256", "OAEP", None)[0]
        plaintext = rsa.RSADecrypt().execute(rsa_key, ciphertext, "SHA256", "OAEP", None)[0]
        assert plaintext == b"secret"

    def test_oaep_with_label_roundtrip(self, rsa_key):
        ciphertext = rsa.RSAEncrypt().execute(rsa_key.public_key(), b"secret", "SHA256", "OAEP", b"label")[0]
        plaintext = rsa.RSADecrypt().execute(rsa_key, ciphertext, "SHA256", "OAEP", b"label")[0]
        assert plaintext == b"secret"

    def test_pkcs1v15_roundtrip(self, rsa_key):
        ciphertext = rsa.RSAEncrypt().execute(rsa_key.public_key(), b"secret", "SHA256", "PKCS1v15", None)[0]
        plaintext = rsa.RSADecrypt().execute(rsa_key, ciphertext, "SHA256", "PKCS1v15", None)[0]
        assert plaintext == b"secret"


class TestRSANumbers:
    def test_public_numbers_format(self):
        pub_key, numbers = rsa.RSAPublicNumbersFormat().execute(3233, 17)
        assert numbers.n == 3233
        assert numbers.e == 17
        assert pub_key.public_numbers() == numbers

    def test_public_numbers_values_from_key(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        n, e = rsa.RSAPubNumValue().execute(priv.public_key().public_numbers(), None)
        assert n == priv.public_key().public_numbers().n
        assert e == 65537

    def test_private_numbers_values_from_key(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        pub_numbers, p, q, d, dmp1, dmq1, iqmp = rsa.RSAPrivNumValue().execute(priv.private_numbers(), None)
        pn = priv.private_numbers()
        assert pub_numbers == pn.public_numbers
        assert (p, q, d, dmp1, dmq1, iqmp) == (pn.p, pn.q, pn.d, pn.dmp1, pn.dmq1, pn.iqmp)

    def test_private_numbers_format_rebuilds_key(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        pn = priv.private_numbers()
        private_num, rebuilt = rsa.RSAPrivateNumbersFormat().execute(pn.public_numbers, pn.p, pn.q, pn.d, False)
        assert rebuilt.private_numbers() == pn
        assert private_num == pn

    def test_pub_num_value_requires_exactly_one_source(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        with pytest.raises(ValueError, match="Invalid configuration"):
            rsa.RSAPubNumValue().execute(priv.public_key().public_numbers(), priv.public_key())

    def test_priv_num_value_requires_exactly_one_source(self):
        priv = c_rsa.generate_private_key(65537, 1024)
        with pytest.raises(ValueError, match="Invalid configuration"):
            rsa.RSAPrivNumValue().execute(priv.private_numbers(), priv)

    def test_restore_private_exponent(self):
        d = rsa.RSARestoreD().execute(17, 3, 11)[0]
        # rsa_recover_private_exponent reduces modulo lcm(p-1, q-1), not (p-1)(q-1).
        assert (d * 17) % math.lcm(3 - 1, 11 - 1) == 1

    def test_restore_prime_factors(self):
        p, q = rsa.RSARestorePrime().execute(33, 17, 13)
        assert {p, q} == {3, 11}

