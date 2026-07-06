# Elliptic curve encryption
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class EllipticCurve:
    def __init__(self):
        pass

    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "curve_name": ([oid for oid in ec.EllipticCurveOID.__dict__.keys() if not oid.startswith("_")], {}),
            },
            "optional": {},
        }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

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
            [
                "Traditional OpenSSL",
                "PKCS8",
            ],
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
                "tooltip": "If `private_value` is defined, this will be the scalar value used to derive the private key. This will not work if `key_source` is From PEM Key",
            },
        )
        class_input["optional"]["pem_key"] = ("BYTESLIKE", {"force_input": True})
        return class_input

    def ecprivatekey(self, curve_name, formatting, encoding, encryption: str, encryption_password, private_value):
        e_curve = self.e_curve(curve_name)
        if private_value == "":
            pkey = ec.generate_private_key(e_curve())
        else:
            private_number = int(private_value, base=10)
            pkey = ec.derive_private_key(private_number, e_curve)

        encoding = getattr(serialization.Encoding, encoding)

        if formatting == "Traditional OpenSSL":
            formatting = serialization.PrivateFormat.TraditionalOpenSSL
        elif formatting == "PKCS8":
            formatting = serialization.PrivateFormat.PKCS8

        if encryption == "Best Available":
            if encryption_password:
                enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        else:
            enc_alg = serialization.NoEncryption()
        p_bytes = pkey.private_bytes(encoding=encoding, format=formatting, encryption_algorithm=enc_alg)
        return (p_bytes, pkey)


# Stub for now
class ECPublicKey(EllipticCurve):
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("public_key",)

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
        class_input["required"]
        return class_input


NODE_CLASS_MAPPINGS = {
    "ECPrivateKey": ECPrivateKey,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ECPrivateKey": "Elliptic Curve Private Key Bytes",
}
