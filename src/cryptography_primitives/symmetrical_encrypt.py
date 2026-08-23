from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms
from cryptography.hazmat.decrepit.ciphers import modes as decrepit_modes
from cryptography.hazmat.primitives.ciphers import algorithms
import warnings


class CipherNodes:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Cipher"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The message to encrypt or decrypt. Must be bytes.",
                    },
                ),
                "key": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The encryption key. Must be bytes.",
                    },
                ),
                "iv": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "A random string to initialize from for modes. Use SystemRandom (Random Nonce Generator) to generate this. Note that is also acts like `tweak` for XTS.",
                    },
                ),
                "algorithm": (
                    [
                        "AES",
                        "AES128",
                        "AES256",
                        "Camellia",
                        "ChaCha20",
                        "TripleDES",
                        "SM4",
                        "ARC4",
                        "Blowfish",
                        "CAST5",
                        "SEED",
                        "IDEA",
                    ],
                    {
                        "default": "AES",
                        "tooltip": "The algorithm used for symmetric encryption",
                    },
                ),
                "modes": (
                    [
                        "CBC",
                        "CTR",
                        "OFB",
                        "CFB",
                        "CFB8",
                        "GCM",
                        "XTS",
                        "ECB",
                        "None",
                    ],
                    {
                        "default": "CBC",
                        "tooltip": "The mode used for symmetric encryption",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "Encrypt",
                        "label_off": "Decrypt",
                        "tooltip": "Toggle between encrypting and decrypting.",
                    },
                ),
            },
            "optional": {
                "tag": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The tag bytes to verify during decryption. Exclusively for GCM mode. When encrypting this must be None. When decrypting, it may be None if the tag is supplied on finalization using finalize_with_tag(). Otherwise, the tag is mandatory.",
                    },
                ),
                "min_tag_length": (
                    "INT",
                    {
                        "default": 16,
                        "tooltip": "The minimum length tag must be. Exclusively for GCM mode.",
                    },
                ),
                "nonce": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "A random nonce to instantiate from. Currently only for ChaCha20",
                    },
                ),
            },
        }

    RETURN_TYPES = ("BYTESLIKE", "BYTESLIKE")
    RETURN_NAMES = ("output", "tag")
    FUNCTION = "execute"


class EncryptDecrypt(CipherNodes):
    def execute(self, text, key, iv, nonce, algorithm, modes, mode, min_tag_length, tag=None):
        if iv is None:
            iv = b""
        if nonce is None:
            nonce = b""
        if tag is None:
            tag = b""
        if algorithm == "ChaCha20":
            algorithm = algorithms.ChaCha20(key, nonce)
        elif algorithm in ["ARC4", "Blowfish", "CAST5", "SEED", "IDEA", "Camellia"]:
            warnings.warn(f'[ComfyUI-ARG-Toolkit][WARNING]: Current algorithm used in Symmetric Encrypt/Decrypt ({algorithm}) is a decrepit type and is only meant for full inclusion. Unless you have a specific use case for this, please switch to a more reasonable algorithm.')
            algorithm = getattr(decrepit_algorithms, algorithm)(key)
        else:
            algorithm = getattr(algorithms, algorithm)(key)
        if modes == "GCM":
            min_tag_length = int(min_tag_length)
            modes = ciphers.modes.GCM(iv, tag, min_tag_length)
        elif modes in ["CFB", "OFB", "CFB8"]:
            modes = getattr(decrepit_modes)(iv)
        elif modes == "XTS":
            modes = ciphers.modes.XTS(tweak=iv)
        elif modes == "ECB":
            warnings.warn(f'[ComfyUI-ARG-Toolkit][WARNING]: Mode used in Symmetric Encrypt/Decrypt ({modes}) is inherently insecure and should never be used in anything in production. Unless you have a specific use case for this, please switch to a more reasonable mode.')
            modes = ciphers.modes.ECB()
        elif modes == "None":
            modes = None
        else:
            modes = getattr(ciphers.modes, modes)(iv)
        cipher_engine = ciphers.Cipher(algorithm, modes)
        if mode:
            encryptor = cipher_engine.encryptor()
            data = text
            ct = encryptor.update(data) + encryptor.finalize()
            tag_out = b""
            if isinstance(modes, ciphers.modes.GCM):
                tag_out = encryptor.tag
            return (ct, tag_out)
        else:
            decryptor = cipher_engine.decryptor()
            data = text
            if isinstance(modes, ciphers.modes.GCM):
                pt = decryptor.update(data) + decryptor.finalize_with_tag(tag)
            else:
                pt = decryptor.update(data) + decryptor.finalize()
            return (pt, b"")


NODE_CLASS_MAPPINGS = {
    "SymmetricEncryptDecrypt": EncryptDecrypt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SymmetricEncryptDecrypt": "Symmetric Encrypt/Decrypt",
}
