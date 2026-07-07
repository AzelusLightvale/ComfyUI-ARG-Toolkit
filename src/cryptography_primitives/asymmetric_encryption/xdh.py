# Elliptic curve (X/EC) Diffie-Hellman (DH) key exchange
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519, x448


class InitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

    @staticmethod
    def get_private_key(key_source, key_type, private_key_bytes=None):
        if key_type == "x25519":
            pk_cls = x25519.X25519PrivateKey
        elif key_type == "x448":
            pk_cls = x448.X448PrivateKey
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        if key_source:  # True means "Fresh Key"
            return pk_cls.generate()
        else:  # False means "From Private Bytes"
            if private_key_bytes is None:
                raise ValueError("Private key bytes are required when key_source is 'From Private Bytes'")
            return pk_cls.from_private_bytes(private_key_bytes)


class XPrivateKeyFormat(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_type": (
                    ["x25519", "x448"],
                    {"default": "x25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "encoding": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the private key.",
                    },
                ),
                "formatting": (
                    [
                        "PKCS8",
                        "Raw",
                    ],
                    {
                        "default": "PKCS8",
                        "description": "What format to serialize the key in.",
                    },
                ),
                "encryption": (["Best Available", "None"], {"default": "Best Available"}),
            },
            "optional": {
                "encryption_password": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The password to use to encrypt the private key. Required if encryption is used.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("private_bytes", "private_key")

    def execute(self, key_type, encoding, formatting, encryption: str, encryption_password=""):
        private_key = self.get_private_key(key_source="Fresh Key", key_type=key_type)
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PrivateFormat, formatting)

        if encryption == "Best Available":
            if encryption_password:
                enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        else:
            enc_alg = serialization.NoEncryption()

        output = private_key.private_bytes(encoding=encode, format=formatting, encryption_algorithm=enc_alg)
        return (output, private_key)


class XPublicKeyFormat(InitNode):
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "Fresh Key",
                        "label_off": "From Private Bytes",
                        "tooltip": "The source of the private key to be used to generate the public key.",
                        "default": True,
                    },
                ),
                "key_type": (
                    ["x25519", "x448"],
                    {"default": "x25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "encoding": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the public key.",
                    },
                ),
                "formatting": (
                    ["SubjectPublicKeyInfo", "Raw"],
                    {
                        "default": "SubjectPublicKeyInfo",
                        "description": "What format to serialize the key in. OpenSSH requires PEM encoding.",
                    },
                ),
            },
            "optional": {
                "private_key": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is 'From Private Bytes'.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("public_bytes", "public_key")

    def execute(self, key_source, key_type, encoding, formatting, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)
        public_key = private_key_obj.public_key()
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)
        output = public_key.public_bytes(encoding=encode, format=formatting)
        return (output, public_key)


class XExchange(InitNode):
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "Fresh Key",
                        "label_off": "From Private Bytes",
                        "tooltip": "The source of the private key to be used to create the shared key.",
                        "default": True,
                    },
                ),
                "key_type": (
                    ["x25519", "x448"],
                    {"default": "x25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "public_key": (
                    "BYTESLIKE",
                    {
                        "tooltip": "The public key (assumed in Raw formatting) to derive the shared key from.",
                    },
                ),
            },
            "optional": {
                "private_key": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is 'From Private Bytes'.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("shared_key",)

    def execute(self, key_source, key_type, public_key, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)

        if key_type == "x25519":
            public_key_obj = x25519.X25519PublicKey.from_public_bytes(public_key)
        elif key_type == "x448":
            public_key_obj = x448.X448PublicKey.from_public_bytes(public_key)
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        shared_key = private_key_obj.exchange(public_key_obj)
        return (shared_key,)


NODE_CLASS_MAPPINGS = {
    "XPrivateKeyFormat": XPrivateKeyFormat,
    "XPublicKeyFormat": XPublicKeyFormat,
    "XExchange": XExchange,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "XPrivateKeyFormat": "ECDH Private Key Bytes",
    "XPublicKeyFormat": "ECDH Public Key Bytes",
    "XExchange": "ECDH Shared Key Exchange",
}
