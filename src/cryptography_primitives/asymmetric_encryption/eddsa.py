from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization

from cryptography.exceptions import InvalidSignature


class InitNode:
    CATEGORY = "Cryptography/Modern/Asymmetric"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    @staticmethod
    def get_private_key(key_source, key_type, private_key_bytes=None):
        if key_type == "Ed25519":
            pk_cls = asymmetric.ed25519.Ed25519PrivateKey
        elif key_type == "Ed448":
            pk_cls = asymmetric.ed448.Ed448PrivateKey
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        if key_source:  # True means "Fresh Key"
            return pk_cls.generate()
        else:  # False means "From Private Bytes"
            if private_key_bytes is None:
                raise ValueError("Private key bytes are required when key_source is 'From Private Bytes'")
            return pk_cls.from_private_bytes(private_key_bytes)


class EdDSAPrivateKeyFormat(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
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

    def eddsaprivatekeyformat(self, key_type, encoding_format, formatting, encryption_algorithm, encryption_password=""):
        if key_type == "Ed25519":
            private_key = asymmetric.ed25519.Ed25519PrivateKey.generate()
        elif key_type == "Ed448":
            private_key = asymmetric.ed448.Ed448PrivateKey.generate()
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        if formatting == "OpenSSH" and encoding_format != "PEM":
            raise ValueError("OpenSSH format requires PEM encoding.")

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


class EdDSASignature(InitNode):
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
                        "tooltip": "The source of the private key to be used to sign the message",
                        "default": True,
                    },
                ),
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "message": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
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
    RETURN_NAMES = ("signature",)

    def edssasignature(self, key_source, key_type, message, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)
        signature = private_key_obj.sign(message.encode("utf-8"))
        return (signature,)


class EdDSAPublicKeyFormat(InitNode):
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
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
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

    def eddsapublickeyformat(self, key_source, key_type, encoding_format, formatting, private_key=None):
        private_key_obj = self.get_private_key(key_source, key_type, private_key)
        public_key = private_key_obj.public_key()

        if formatting == "OpenSSH" and encoding_format != "PEM":
            raise ValueError("OpenSSH format requires PEM encoding.")

        encode = getattr(serialization.Encoding, encoding_format)

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


class EdDSAVerify(InitNode):
    CATEGORY = "Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "public_key": ("BYTESLIKE", {}),
                "message": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                    },
                ),
                "signature": ("BYTESLIKE",),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_status",)

    def eddsaverify(self, key_type, public_key, message, signature):
        if key_type == "Ed25519":
            pk_loader = asymmetric.ed25519.Ed25519PublicKey.from_public_bytes
        elif key_type == "Ed448":
            pk_loader = asymmetric.ed448.Ed448PublicKey.from_public_bytes
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        try:
            public_key_obj = pk_loader(public_key)
            public_key_obj.verify(signature, message.encode("utf-8"))
            output = True
        except (InvalidSignature, ValueError):
            output = False
        return (output,)


NODE_CLASS_MAPPINGS = {
    "EdDSAPrivateKeyFormat": EdDSAPrivateKeyFormat,
    "EdDSASignature": EdDSASignature,
    "EdDSAPublicKeyFormat": EdDSAPublicKeyFormat,
    "EdDSAVerify": EdDSAVerify,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "EdDSAPrivateKeyFormat": "EdDSA Private Key Bytes",
    "EdDSASignature": "EdDSA Signature Generator",
    "EdDSAPublicKeyFormat": "EdDSA Public Key Bytes",
    "EdDSAVerify": "EDDSA Message Verification",
}
