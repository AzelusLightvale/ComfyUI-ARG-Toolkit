# Elliptic curve encryption
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class EllipticCurve:
    def __init__(self):
        pass

    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "curve_name": ([oid for oid in ec.EllipticCurveOID.__dict__.keys() if not oid.startswith("_")], {}),
            },
            "optional": {},
        }

    def e_curve(self, curve_name: str):
        if curve_name in ["BRAINPOOLP256R1", "BRAINPOOLP384R1", "BRAINPOOLP512R1"]:
            c_name = "Brainpool" + curve_name[9:]
        else:
            c_name = str(curve_name)
        e_curve_cls = getattr(ec, c_name)
        return e_curve_cls


class ECPrivateKey(EllipticCurve):
    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("keyfile", "private_key")

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["formatting"] = (
            ["Traditional OpenSSL", "PKCS8", "OpenSSH"],
            {
                "default": "PKCS8",
                "description": "What format to serialize the key in. OpenSSH requires PEM encoding.",
            },
        )
        class_input["required"]["encoding"] = (
            [
                "PEM",
                "DER",
            ],
            {"default": "PEM", "description": "Encoding type for the private key."},
        )
        class_input["required"]["encryption"] = (["Best Available", "None"], {"default": "Best Available"})
        class_input["optional"]["encryption_password"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The password to use to encrypt the private key. Required if encryption is used.",
            },
        )
        class_input["optional"]["private_value"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "If `private_value` is defined, this will be the scalar value used to derive the private key.",
            },
        )
        class_input["optional"]["pem_key"] = ("BYTESLIKE", {"force_input": True})
        return class_input

    def execute(self, curve_name, formatting, encoding, encryption: str, encryption_password, private_value):
        e_curve = self.e_curve(curve_name)
        if private_value == "":
            pkey = ec.generate_private_key(e_curve())
        else:
            private_number = int(private_value, base=10)
            pkey = ec.derive_private_key(private_number, e_curve)

        encoding = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PrivateFormat, formatting)

        if encryption == "Best Available":
            if encryption_password:
                enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        else:
            enc_alg = serialization.NoEncryption()
        p_bytes = pkey.private_bytes(encoding=encoding, format=formatting, encryption_algorithm=enc_alg)
        return (p_bytes, pkey)


class ECPublicKey(EllipticCurve):
    RETURN_TYPES = ("BYTESLIKE", "KEYOBJ")
    RETURN_NAMES = ("public_bytes", "public_key")

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["key_source"] = (
            "BOOLEAN",
            {
                "label_on": "Fresh Key",
                "label_off": "From Loaded Key",
                "tooltip": "The source of the private key to be used to sign the message",
                "default": True,
            },
        )
        class_input["required"]["formatting"] = (
            ["SubjectPublicKeyInfo", "OpenSSH", "PKCS1", "CompressedPoint", "UncompressedPoint"],
            {
                "default": "PKCS8",
                "description": "What format to serialize the key in. OpenSSH requires PEM encoding.",
            },
        )
        class_input["required"]["encoding"] = (
            ["PEM", "DER", "OpenSSH", "X962"],
            {"default": "PEM", "description": "Encoding type for the private key."},
        )
        class_input["optional"]["serialized_key"] = ("KEYOBJ", {"forceInput": True})
        return class_input

    def execute(self, curve_name, key_source, serialized_key, encoding, formatting):
        e_curve = self.e_curve(curve_name)
        if key_source:
            private_key = ec.generate_private_key(e_curve())
        elif not key_source:
            private_key = serialized_key
        public_key = private_key.public_key()

        encoding = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)

        p_bytes = public_key.public_bytes(encoding, formatting)
        return (p_bytes, public_key)


class ECSign:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("signature",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "private_key": ("KEYOBJ", {"forceInput": True}),
                "data": ("BYTESLIKE", {"forceInput": True}),
                "signature_algorithm": (
                    [
                        "SHA224",
                        "SHA256",
                        "SHA384",
                        "SHA512",
                        "SHA512_224",
                        "SHA512_256",
                        "BLAKE2b",
                        "BLAKE2s",
                        "SHA3_224",
                        "SHA3_256",
                        "SHA3_384",
                        "SHA3_512",
                        "SHA1",
                        "MD5",
                        "SM3",
                    ],
                    {"tooltip": "The hashing algorithm used for the signature."},
                ),
            },
            "optional": {"prehashed": ("BOOLEAN", {"tooltip": "Whether the data is prehashed or not."})},
        }

    def execute(self, private_key, data, signature_algorithm, prehashed):
        if signature_algorithm == "BLAKE2b":
            algorithm = getattr(hashes, signature_algorithm)(64)
        elif signature_algorithm == "BLAKE2s":
            algorithm = getattr(hashes, signature_algorithm)(32)
        else:
            algorithm = getattr(hashes, signature_algorithm)()
        if prehashed:
            from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

            algorithm = Prehashed(algorithm)
        alg = ec.ECDSA(algorithm)
        return (private_key.sign(data, alg),)


class ECVerify:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verification",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_key": ("KEYOBJ", {"forceInput": True}),
                "signature": ("BYTESLIKE", {"forceInput": True}),
                "data": ("BYTESLIKE", {"forceInput": True}),
                "signature_algorithm": (
                    [
                        "SHA224",
                        "SHA256",
                        "SHA384",
                        "SHA512",
                        "SHA512_224",
                        "SHA512_256",
                        "BLAKE2b",
                        "BLAKE2s",
                        "SHA3_224",
                        "SHA3_256",
                        "SHA3_384",
                        "SHA3_512",
                        "SHA1",
                        "MD5",
                        "SM3",
                    ],
                    {"tooltip": "The hashing algorithm used for the signature."},
                ),
            },
            "optional": {"prehashed": ("BOOLEAN", {"tooltip": "Whether the data is prehashed or not."})},
        }

    def execute(self, public_key, signature, data, signature_algorithm, prehashed):
        if signature_algorithm == "BLAKE2b":
            algorithm = getattr(hashes, signature_algorithm)(64)
        elif signature_algorithm == "BLAKE2s":
            algorithm = getattr(hashes, signature_algorithm)(32)
        else:
            algorithm = getattr(hashes, signature_algorithm)()
        if prehashed:
            from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

            algorithm = Prehashed(algorithm)
        alg = ec.ECDSA(algorithm)
        try:
            public_key.verify(signature, data, alg)
            verification = True
        except (InvalidSignature, ValueError):
            verification = False
        return (verification,)


NODE_CLASS_MAPPINGS = {
    "ECPrivateKey": ECPrivateKey,
    "ECPublicKey": ECPublicKey,
    "ECSign": ECSign,
    "ECVerify": ECVerify,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ECPrivateKey": "Elliptic Curve Private Key Bytes",
    "ECPublicKey": "Elliptic Curve Public Key Bytes",
    "ECSign": "Elliptic Curve Signature Sign",
    "ECVerify": "Elliptic Curve Signature Verify",
}
