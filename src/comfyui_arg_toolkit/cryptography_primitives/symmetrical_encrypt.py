from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms
from cryptography.hazmat.primitives.ciphers import algorithms


class CipherNodes:
    CATEGORY = "Cryptography/Modern/Cipher"

    @classmethod
    def INPUT_TYPES(cls):
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
                "key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                    },
                ),
                "iv": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
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
                        "ChaCha20TripleDES",
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
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
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
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "forceInput": True,
                        "tooltip": "A random nonce to instantiate from. Currently only for ChaCha20",
                    },
                ),
            },
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("encrypted_txt",)


class EncryptDecrypt(CipherNodes):
    def encryptdecrypt(self, text, key, iv, nonce, algorithm, modes, mode, min_tag_length, tag):
        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)
        if algorithm == "ChaCha20":
            algorithm = algorithms.ChaCha20(key, nonce)
        elif algorithm in ["ARC4", "Blowfish", "CAST5", "SEED", "IDEA"]:
            algorithm = getattr(decrepit_algorithms, algorithm)(key)
        else:
            algorithm = getattr(algorithms, algorithm)(key)
        if modes == "GCM":
            if tag == "":
                tag = None
            else:
                tag = tag.encode("utf-8")
            min_tag_length = int(min_tag_length)
            modes = ciphers.modes.GCM(iv, tag, min_tag_length)
        elif modes == "XTS":
            modes = ciphers.modes.XTS(tweak=iv)
        elif modes == "ECB":
            modes = ciphers.modes.ECB()
        elif modes == "None":
            modes = None
        else:
            modes = getattr(ciphers.modes, modes)(iv)
        cipher_engine = ciphers.Cipher(algorithm, modes)
        if mode:
            encryptor = cipher_engine.encryptor()
            if isinstance(text, str):
                # Check if it's hex string (pre-padded data)
                try:
                    # Try to decode as hex first
                    data = bytes.fromhex(text)
                    # If successful, use the binary data directly
                    ct = encryptor.update(data) + encryptor.finalize()
                except ValueError:
                    # If not hex, treat as regular Unicode text
                    data = text.encode("utf-8")
                    ct = encryptor.update(data) + encryptor.finalize()
            else:
                # If text is already bytes, use directly
                data = text
                ct = encryptor.update(data) + encryptor.finalize()
            if isinstance(modes, ciphers.modes.GCM):
                tag = encryptor.tag
                return (ct.hex(), tag.hex())
            return (ct.hex(),)
        else:
            decryptor = cipher_engine.decryptor()
            if isinstance(text, str):
                text = bytes.fromhex(text)
            else:
                text = text
            if isinstance(modes, ciphers.modes.GCM):
                pt = decryptor.update(text) + decryptor.finalize_with_tag(bytes.fromhex(tag))
            else:
                pt = decryptor.update(text) + decryptor.finalize()
            try:
                return (pt.decode("utf-8"),)
            except UnicodeDecodeError:
                return (pt.hex(),)


NODE_CLASS_MAPPINGS = {
    "SymmetricEncryptDecrypt": EncryptDecrypt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SymmetricEncryptDecrypt": "Symmetric Encrypt/Decrypt",
}
