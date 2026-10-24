# ML-DSA signature algorithms

# As of `cryptography` v51.0.0, DSA has been deprecated and replaced with ML-DSA (Module-Lattice-Based Digital Signature Algorithm) on the implementation side. Their recommendation is to use EdDSA or ML-DSA instead.

from cryptography.hazmat.primitives.asymmetric import mldsa
from cryptography.hazmat.primitives import serialization

from cryptography.exceptions import InvalidSignature


class InitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

    @staticmethod
    def get_private_format(sig_alg):
        algorithm = {
            "ML-DSA-44": mldsa.MLDSA44PrivateKey,
            "ML-DSA-65": mldsa.MLDSA65PrivateKey,
            "ML-DSA-87": mldsa.MLDSA87PrivateKey,
        }
        return algorithm[sig_alg]

    @staticmethod
    def get_public_format(sig_alg):
        algorithm = {
            "ML-DSA-44": mldsa.MLDSA44PublicKey,
            "ML-DSA-65": mldsa.MLDSA65PublicKey,
            "ML-DSA-87": mldsa.MLDSA87PublicKey,
        }
        return algorithm[sig_alg]


# ML-DSA Private and Public Key loaders
class MLDSAPrivateKeyFormat(InitNode):
    RETURN_TYPES = (
        "BYTESLIKE",
        "KEYOBJ",
    )
    RETURN_NAMES = ("private_bytes", "private_key")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sig_alg": (["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"], {"default": "ML-DSA-65", "tooltip": "The algorithm to use for the private key."}),
                "key_source": ("BOOLEAN", {"default": True, "label_on": "Fresh Key", "label_off": "Seed Bytes", "tooltip": "The source to generate the private key."}),
                "encoding": (
                    ["PEM", "DER", "Raw"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the private key.",
                    },
                ),
                "formatting": (
                    ["PKCS8", "Raw"],
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
                "seed_bytes": (
                    "BYTESLIKE",
                    {"forceInput": True, "tooltip": "The seed bytes to use for generating the private key only when the source is 'Seed Bytes'. Has to be 32 bytes."},
                ),
            },
        }

    def execute(self, sig_alg, key_source, encoding, formatting, encryption, encryption_password, seed_bytes):
        private_key = self.get_private_format(sig_alg=sig_alg).generate() if key_source else self.get_private_format(sig_alg=sig_alg).from_seed_bytes(seed_bytes)
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PrivateFormat, formatting)

        if encryption == "Best Available" and encryption_password:
            enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        else:
            enc_alg = serialization.NoEncryption()

        private_bytes = private_key.private_bytes(encoding=encode, format=formatting, encryption_algorithm=enc_alg)
        return (private_bytes, private_key)


class MLDSAPublicKeyFormat(InitNode):
    RETURN_TYPES = (
        "BYTESLIKE",
        "KEYOBJ",
    )
    RETURN_NAMES = ("public_bytes", "public_key")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sig_alg": (["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"], {"default": "ML-DSA-65", "tooltip": "The algorithm to use for the public key."}),
                "key_source": ("BOOLEAN", {"default": True, "label_on": "From Key Object", "label_off": "From Public Bytes", "tooltip": "The source to load the public key."}),
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
                        "description": "What format to serialize the key in.",
                    },
                ),
            },
            "optional": {
                "public_bytes": (
                    "BYTESLIKE",
                    {
                        "tooltip": "Only applicable if key_source is `From Public Bytes`. Refer to documentation for exact byte size for each algorithm.",
                        "forceInput": True,
                    }
                ),
                "private_key": ("KEYOBJ", {"forceInput": True, "tooltip": "Only applicable is key_source is `From Key Object`."}),
            },
        }

    def execute(self, sig_alg, key_source, encoding, formatting, public_bytes, private_key):
        public_key = InitNode.get_public_format(sig_alg).from_public_bytes(public_bytes) if not key_source else private_key.public_key()
        encode = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)

        output = public_key.public_bytes(encoding=encode, format=formatting)
        return (output, public_key)


## ML-DSA Signing and Verification (with context support)
class MLDSASignature(InitNode):
    RETURN_TYPES = "BYTESLIKE"
    RETURN_NAMES = "signature"

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
                "sig_alg": (["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"], {"default": "ML-DSA-65", "tooltip": "The algorithm to use for the private key."}),
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
                "context": ("BYTESLIKE", {"forceInput": True, "tooltip": "Optional context string, up to 255 bytes."}),
            },
        }

    def execute(self, key_source, sig_alg, message, private_bytes, private_key, context: bytes | None):
        private_key = InitNode.get_private_format(sig_alg).from_private_bytes(private_bytes) if not key_source else private_key
        signature = private_key.sign(message, context)
        return (signature,)


class MLDSAVerify(InitNode):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_status",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sig_alg": (["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"], {"default": "ML-DSA-65", "tooltip": "The algorithm to use for the public key."}),
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
            "optional": {"public_bytes": ("BYTESLIKE", {"forceInput": True}), "public_key": ("KEYOBJ", {"forceInput": True, "tooltip": "Only applicable if key_source is 'From Loaded Key'."}), "context": ("BYTESLIKE", {"forceInput": True, "tooltip": "Optional context string, up to 255 bytes."})},
        }

    def execute(self, sig_alg, public_bytes, public_key, message, signature, key_source, context: bytes | None):
        public_key_obj = InitNode.get_public_format(sig_alg).from_public_bytes(public_bytes) if not key_source else public_key
        try:
            public_key_obj.verify(signature, message, context)
            output = True
        except (InvalidSignature, ValueError):
            output = False
        return (output,)


NODE_CLASS_MAPPINGS = {
    "MLDSAPrivateKeyFormat": MLDSAPrivateKeyFormat,
    "MLDSASignature": MLDSASignature,
    "MLDSAPublicKeyFormat": MLDSAPublicKeyFormat,
    "MLDSAVerify": MLDSAVerify,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "MLDSAPrivateKeyFormat": "ML-DSA Private Key Bytes",
    "MLDSASignature": "ML-DSA Signature Generator",
    "MLDSAPublicKeyFormat": "ML-DSA Public Key Bytes",
    "MLDSAVerify": "ML-DSA Message Verification",
}
