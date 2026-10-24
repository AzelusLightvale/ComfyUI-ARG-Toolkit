# EdDSA signature algorithms

from cryptography.hazmat.primitives.asymmetric import ed25519, ed448
from cryptography.hazmat.primitives import serialization

from cryptography.exceptions import InvalidSignature


class InitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

    @staticmethod
    def get_private_format(sig_alg):
        algorithm = {
            "Ed25519": ed25519.Ed25519PrivateKey,
            "Ed448": ed448.Ed448PrivateKey,
        }
        return algorithm[sig_alg]

    @staticmethod
    def get_public_format(sig_alg):
        algorithm = {
            "Ed25519": ed25519.Ed25519PublicKey,
            "Ed448": ed448.Ed448PublicKey,
        }
        return algorithm[sig_alg]


class EdDSAPrivateKeyFormat(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sig_alg": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The signature algorithm for EdDSA-based asymmetric signing."},
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

    def execute(self, sig_alg, encoding, formatting, encryption: str, encryption_password=""):
        private_key = InitNode.get_private_format(sig_alg=sig_alg).generate()
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PrivateFormat, formatting)

        if encryption == "Best Available" and encryption_password:
            enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        else:
            enc_alg = serialization.NoEncryption()

        output = private_key.private_bytes(encoding=encode, format=formatting, encryption_algorithm=enc_alg)
        return (output, private_key)


class EdDSASignature(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "From Key Object",
                        "label_off": "From Private Bytes",
                        "tooltip": "The source of the private key to be used to verify the signature of the message",
                        "default": True,
                    },
                ),
                "sig_alg": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The signature algorithm for EdDSA-based asymmetric signing."},
                ),
                "message": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The messange to sign.",
                    },
                ),
            },
            "optional": {
                "private_bytes": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is 'From Private Bytes'.",
                        "forceInput": True,
                    },
                ),
                "private_key": ("KEYOBJ", {"forceInput": True, "tooltip": "Only applicable if key_source is `From Key Object`"}),
            },
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("signature",)

    def execute(self, key_source, sig_alg, message, private_key, private_bytes):
        private_key_obj = InitNode.get_private_format(sig_alg).from_private_bytes(private_bytes) if not key_source else private_key
        signature = private_key_obj.sign(message)
        return (signature,)


class EdDSAPublicKeyFormat(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "From Key Object",
                        "label_off": "From Public Bytes",
                        "default": False,
                        "tooltip": "The source of the private key to be used to verify the signature of the message",
                    },
                ),
                "sig_alg": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The signature algorithm for EdDSA-based asymmetric signing."},
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
                "public_bytes": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is 'From Public Bytes'.",
                        "forceInput": True,
                    },
                ),
                "private_key": ("KEYOBJ", {"forceInput": True, "tooltip": "Only applicable is key_source is `From Key Object`."}),
            },
        }

    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("public_bytes", "public_key")

    def execute(self, key_source, sig_alg, encoding, formatting, private_key, public_bytes=None):
        public_key = InitNode.get_public_format(sig_alg).from_public_bytes(public_bytes) if not key_source else private_key.public_key()
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)

        output = public_key.public_bytes(encoding=encode, format=formatting)
        return (output, public_key)


class EdDSAVerify(InitNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sig_alg": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The signature algorithm for EdDSA-based asymmetric signing."},
                ),
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "From Private Bytes",
                        "label_off": "From Loaded Key",
                        "tooltip": "The source of the public key to be used to verify the signature of the message",
                    },
                ),
                "message": (
                    "BYTESLIKE",
                    {"forceInput": True},
                ),
                "signature": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                    },
                ),
            },
            "optional": {
                "public_bytes": ("BYTESLIKE", {"forceInput": True}),
                "public_key": ("KEYOBJ", {"forceInput": True, "tooltip": "Only applicable if key_source is 'From Loaded Key'."}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_status",)

    def execute(self, sig_alg, public_bytes, public_key, message, signature, key_source):
        public_key_obj = InitNode.get_public_format(sig_alg).from_public_bytes(public_bytes) if not key_source else public_key
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
