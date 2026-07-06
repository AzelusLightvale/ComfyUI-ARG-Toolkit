from cryptography.hazmat.primitives.asymmetric import ed25519, ed448
from cryptography.hazmat.primitives import serialization

from cryptography.exceptions import InvalidSignature


class InitNode:
    def __init__(self):
        pass

    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

    @staticmethod
    def get_private_key(key_source, key_type, private_key_bytes=None):
        if key_type == "Ed25519":
            pk_cls = ed25519.Ed25519PrivateKey
        elif key_type == "Ed448":
            pk_cls = ed448.Ed448PrivateKey
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        if key_source == "Fresh Key":
            return pk_cls.generate()
        elif key_source == "From Private Bytes":
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
                "encoding": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the private key.",
                    },
                ),
                "formatting": (
                    ["PKCS8", "OpenSSH", "Raw"],
                    {
                        "default": "PKCS8",
                        "description": "What format to serialize the key in. OpenSSH requires PEM encoding and is only applicable for Ed25519.",
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
        return (output,)


class EdDSASignature(InitNode):
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    ["Fresh Key", "From Private Bytes", "From Loaded Key"],
                    {
                        "tooltip": "The source of the private key to be used to sign the message",
                        "default": "Fresh Key",
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
                "private_bytes": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is 'From Private Bytes'.",
                    },
                ),
                "serialized_key": ("KEYOBJ", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("signature",)

    def execute(self, key_source, key_type, message, serialized_key, private_bytes=None):
        if key_source == "From Loaded Key":
            private_key_obj = serialized_key
        else:
            private_key_obj = self.get_private_key(key_source, key_type, private_bytes)
        signature = private_key_obj.sign(message.encode("utf-8"))
        return (signature,)


class EdDSAPublicKeyFormat(InitNode):
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    ["Fresh Key", "From Private Bytes", "From Loaded Key"],
                    {
                        "tooltip": "The source of the private key to be used to sign the message",
                        "default": "Fresh Key",
                    },
                ),
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "encoding": (
                    [
                        "PEM",
                        "DER",
                        "OpenSSH",
                        "Raw",
                    ],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the public key. OpenSSH is only usable with Ed25519.",
                    },
                ),
                "formatting": (
                    ["SubjectPublicKeyInfo", "Raw", "OpenSSH"],
                    {
                        "default": "SubjectPublicKeyInfo",
                        "description": "What format to serialize the key in. OpenSSH is only usable with Ed25519.",
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
                "serialized_key": ("KEYOBJ", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("public_bytes", "public_key")

    def execute(self, key_source, key_type, encoding, formatting, serialized_key, private_key=None):
        if key_source == "From Loaded Key":
            private_key_obj = serialized_key
        else:
            private_key_obj = self.get_private_key(key_source, key_type, private_key)
        public_key = private_key_obj.public_key()
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)

        output = public_key.public_bytes(encoding=encode, format=formatting)
        return (output, public_key)


class EdDSAVerify(InitNode):
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "From Private Bytes",
                        "label_off": "From Loaded Key",
                        "tooltip": "The source of the private key to be used to verify the signature of the message",
                    },
                ),
                "message": (
                    "BYTESLIKE",
                    {"forceInput": True},
                ),
                "signature": ("BYTESLIKE",),
            },
            "optional": {"public_bytes": ("BYTESLIKE", {"forceInput": True}), "public_key": ("KEYOBJ", {"forceInput": True})},
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_status",)

    def execute(self, key_type, public_bytes, public_key, message, signature, key_source):
        if key_source:
            if key_type == "Ed25519":
                pk_loader = ed25519.Ed25519PublicKey.from_public_bytes
                public_key_obj = pk_loader(public_bytes)
            elif key_type == "Ed448":
                pk_loader = ed448.Ed448PublicKey.from_public_bytes
                public_key_obj = pk_loader(public_bytes)
        elif not key_source:
            public_key_obj = public_key
        try:
            public_key_obj.verify(signature, message)
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
