# Elliptic curve (X/EC) Diffie-Hellman (DH) key exchange
from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization


class InitNode:
    CATEGORY = "Cryptography/Modern/Asymmetric"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    @staticmethod
    def get_private_key(key_source, key_type, private_key_bytes=None):
        if key_type == "x25519":
            pk_cls = asymmetric.x25519.X25519PrivateKey
        elif key_type == "x448":
            pk_cls = asymmetric.x448.X448PrivateKey
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
                "encoding_format": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the private key.",
                    },
                ),
                "formatting": (
                    ["PKCS8", "Raw", "OpenSSH"],
                    {
                        "default": "PKCS8",
                        "description": "What format to serialize the key in. OpenSSH requires PEM encoding.",
                    },
                ),
                "encryption_algorithm": (["Best Available", "None"], {"default": "Best Available"}),
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

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("private_key",)

    def xprivatekeyformat(self, key_type, encoding_format, formatting, encryption_algorithm, encryption_password=""):
        if key_type == "x25519":
            private_key = asymmetric.x25519.X25519PrivateKey.generate()
        elif key_type == "x448":
            private_key = asymmetric.x448.X448PrivateKey.generate()
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        encode = getattr(serialization.Encoding, encoding_format)

        if formatting == "PKCS8":
            format_ = serialization.PrivateFormat.PKCS8
        elif formatting == "Raw":
            format_ = serialization.PrivateFormat.Raw
        elif formatting == "OpenSSH":
            format_ = serialization.PrivateFormat.OpenSSH
        else:
            raise ValueError(f"Unsupported formatting: {formatting}")

        if encryption_algorithm == "Best Available":
            if encryption_password:
                enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
            else:
                enc_alg = serialization.NoEncryption()
        elif encryption_algorithm == "None":
            enc_alg = serialization.NoEncryption()
        else:
            raise ValueError(f"Unsupported encryption algorithm: {encryption_algorithm}")

        output = private_key.private_bytes(encoding=encode, format=format_, encryption_algorithm=enc_alg)
        return (output,)


class XPublicKeyFormat(InitNode):
    CATEGORY = "Cryptography/Modern/Asymmetric"

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
                "encoding_format": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the public key.",
                    },
                ),
                "formatting": (
                    ["SubjectPublicKeyInfo", "Raw", "OpenSSH"],
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

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("public_key",)

    def xpublickeyformat(self, key_source, key_type, encoding_format, formatting, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)
        public_key = private_key_obj.public_key()
        encode = getattr(serialization.Encoding, encoding_format)

        # Due to the nature of `cryptography` and its formatting handler, any incompatible schemes are immediately rejected. Therefore, there is no real need to handle it on the node side.

        if formatting == "SubjectPublicKeyInfo":
            format_ = serialization.PublicFormat.SubjectPublicKeyInfo
        elif formatting == "Raw":
            format_ = serialization.PublicFormat.Raw
        elif formatting == "OpenSSH":
            format_ = serialization.PublicFormat.OpenSSH
        else:
            raise ValueError(f"Unsupported formatting: {formatting}")

        output = public_key.public_bytes(encoding=encode, format=format_)
        return (output,)


class XExchange(InitNode):
    CATEGORY = "Cryptography/Modern/Asymmetric"

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

    def xexchange(self, key_source, key_type, public_key, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)

        if key_type == "x25519":
            public_key_obj = asymmetric.x25519.X25519PublicKey.from_public_bytes(public_key)
        elif key_type == "x448":
            public_key_obj = asymmetric.x448.X448PublicKey.from_public_bytes(public_key)
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
