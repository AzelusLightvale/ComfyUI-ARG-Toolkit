from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization
import base64

from cryptography.exceptions import InvalidSignature


class InitNode:
    CATEGORY = "Cryptography/Modern/Asymmetric"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


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
                    ["PEM", "DER (Converted)", "OpenSSH", "Raw (Converted)", "X962 (Converted)", "SMIME"],
                    {
                        "default": "PEM",
                        "description": 'Encoding type for the private key. Some formats (ones with "(Converted)" next to them) are binary formats, which cannot be outputted normally in ComfyUI. To better serve the purpose of the node, these formats will be converted to a chosen format below in `conversion_format`.',
                    },
                ),
                "conversion_format": (
                    ["Base64", "Hexadecimal", "UTF-8 String", "Binary"],
                    {
                        "default": "Base64",
                        "description": "The conversion format to be used with the converted encoding format that cannot be outputted raw.",
                    },
                ),
                "formatting": (
                    ["Traditional OpenSSL", "PKCS8", "Raw (Converted)", "OpenSSH (Requires PEM)"],
                    {
                        "default": "OpenSSH (Requires PEM)",
                        "description": "What format to serialize the key in",
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
                        "tooltip": "The password to use to encrypt the private key.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("private_bytes",)

    def from_private_key_formatting(self, encoding_format, formatting, encryption_algorithm, encryption_password):
        if encoding_format in ["PEM", "OpenSSH", "SMIME"]:
            encode = getattr(serialization.Encoding, encoding_format)
        elif encoding_format == "DER (Converted)":
            encode = serialization.Encoding.DER
        elif encoding_format == "Raw (Converted)":
            encode = serialization.Encoding.Raw
        elif encoding_format == "X962 (Converted)":
            encode = serialization.Encoding.X962
        else:
            raise ValueError

        if formatting == "Traditional OpenSSL":
            format = serialization.PrivateFormat.TraditionalOpenSSL
        elif formatting == "PKCS8":
            format = serialization.PrivateFormat.PKCS8
        elif formatting == "Raw (Converted)":
            format = serialization.PrivateFormat.Raw
        elif formatting == "OpenSSH (Requires PEM)":
            format = serialization.PrivateFormat.OpenSSH
        else:
            raise ValueError

        if encryption_algorithm == "Best Available":
            encryption_algorithm = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
        elif encryption_algorithm == "None":
            encryption_algorithm = serialization.NoEncryption()
        else:
            raise ValueError
        return (encode, format, encryption_algorithm)

    def eddsaprivatekeyformat(self, key_type, encoding_format, formatting, encryption_algorithm, conversion_format, encryption_password):
        if key_type == "Ed25519":
            ed = asymmetric.ed25519.Ed25519PrivateKey
        elif key_type == "Ed448":
            ed = asymmetric.ed448.Ed448PrivateKey
        else:
            raise ValueError
        ed_private_key = ed.generate()
        output = ed_private_key.private_bytes(
            self.from_private_key_formatting(encoding_format, formatting, encryption_algorithm, encryption_password)
        )
        if encoding_format in ["DER (Converted)", "Raw (Converted)", "X962 (Converted)"]:
            output = output.decode("utf-8")
            if conversion_format == "Base64":
                output = base64.b64encode(output).decode("utf-8")
            elif conversion_format == "Hexadecimal":
                output = output.hex()
            elif conversion_format == "UTF-8 String":
                output = output.decode("utf-8")
            elif conversion_format == "Binary":
                output = bytes(int(b, 2) for b in output.split(" ")).decode("utf-8")
            else:
                raise ValueError
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
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Only applicable if key_source is set to From Private Bytes. Uses the format defined below.",
                    },
                ),
                "byte_format": (["Base64", "Hexadecimal", "String", "Binary"], {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("signature",)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    def EdDSAInit(self, key_source, key_type, private_bytes, byte_format):
        if key_type == "Ed25519":
            ed = asymmetric.ed25519.Ed25519PrivateKey
        elif key_type == "Ed448":
            ed = asymmetric.ed448.Ed448PrivateKey
        else:
            raise ValueError
        if key_source:
            ed_private_key = ed.generate()
        else:
            if byte_format == "Base64":
                ed_private_bytes = base64.b64decode(private_bytes).encode("utf-8")
            elif byte_format == "Hexadecimal":
                ed_private_bytes = bytes.fromhex(private_bytes)
            elif byte_format == "String":
                ed_private_bytes = private_bytes.encode("utf-8")
            elif byte_format == "Binary":
                ed_private_bytes = bytes(int(b, 2) for b in private_bytes.split(" "))
            else:
                raise ValueError
            ed_private_key = ed.from_private_bytes(ed_private_bytes)
            return ed_private_key

    def edssasignature(self, key_source, key_type, message, private_bytes, byte_format):
        signature = self.EdDSAInit(key_source, key_type, private_bytes, byte_format).sign(message.encode("utf-8"))
        return (signature.hex(),)


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
                    },
                ),
                "key_type": (
                    ["Ed25519", "Ed448"],
                    {"default": "Ed25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "encoding_format": (
                    ["PEM", "DER (Converted)", "OpenSSH", "Raw (Converted)", "X962 (Converted)", "SMIME"],
                    {
                        "default": "PEM",
                        "description": 'Encoding type for the private key. Some formats (ones with "(Converted)" next to them) are binary formats, which cannot be outputted normally in ComfyUI. To better serve the purpose of the node, these formats will be converted to a chosen format below in `conversion_format`.',
                    },
                ),
                "conversion_format": (
                    ["Base64", "Hexadecimal", "UTF-8 String", "Binary"],
                    {
                        "default": "Base64",
                        "description": "The conversion format to be used with the converted encoding format that cannot be outputted raw.",
                    },
                ),
                "formatting": (
                    ["SubjectPublicKeyInfo", "PKCS8", "Raw (Converted)", "OpenSSH (Requires PEM)"],
                    {
                        "default": "OpenSSH (Requires PEM)",
                        "description": "What format to serialize the key in",
                    },
                ),
            },
            "optional": {
                "private_bytes": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Only applicable if key_source is set to From Private Bytes. Uses the format defined below.",
                    },
                ),
                "byte_format": (["Base64", "Hexadecimal", "String", "Binary"], {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("public_bytes",)

    def from_public_key_formatting(self, encoding_format, formatting):
        if encoding_format in ["PEM", "OpenSSH", "SMIME"]:
            encode = getattr(serialization.Encoding, encoding_format)
        elif encoding_format == "DER (Converted)":
            encode = serialization.Encoding.DER
        elif encoding_format == "Raw (Converted)":
            encode = serialization.Encoding.Raw
        elif encoding_format == "X962 (Converted)":
            encode = serialization.Encoding.X962
        else:
            raise ValueError

        if formatting == "SubjectPublicKeyInfo":
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        elif formatting == "PKCS8":
            format = serialization.PublicFormat.PKCS8
        elif formatting == "Raw (Converted)":
            format = serialization.PublicFormat.Raw
        elif formatting == "OpenSSH (Requires PEM)":
            format = serialization.PublicFormat.OpenSSH
        else:
            raise ValueError
        return (encode, format)

    def eddsapublickeyformat(self, key_source, key_type, encoding_format, conversion_format, formatting, private_bytes, byte_format):
        ed_private_key = EdDSASignature.EdDSAInit(key_source, key_type, private_bytes, byte_format)
        ed_public_key = ed_private_key.public_key()
        output = ed_public_key.public_bytes(self.from_public_key_formatting(encoding_format, formatting))
        if encoding_format in ["DER (Converted)", "Raw (Converted)", "X962 (Converted)"]:
            output = output.decode("utf-8")
            if conversion_format == "Base64":
                output = base64.b64encode(output).decode("utf-8")
            elif conversion_format == "Hexadecimal":
                output = output.hex()
            elif conversion_format == "UTF-8 String":
                output = output.decode("utf-8")
            elif conversion_format == "Binary":
                output = bytes(int(b, 2) for b in output.split(" ")).decode("utf-8")
            else:
                raise ValueError
        return (output,)


class EdDSAVerify(InitNode):
    CATEGORY = "Cryptography/Modern/Asymmetric"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    "BOOLEAN",
                    {
                        "label_on": "Fresh Key",
                        "label_off": "From Public Bytes",
                        "tooltip": "The source of the public key to be used to verify the message",
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
                "signature": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "placeholder": "Type your signature here... (in hexadecimal)",
                    },
                ),
            },
            "optional": {
                "public_bytes": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Only applicable if key_source is set to From Private Bytes. Uses the format defined below.",
                    },
                ),
                "byte_format": (["Base64", "Hexadecimal", "String", "Binary"], {}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_status",)

    def eddsaverify(self, key_source, key_type, message, signature, public_bytes, byte_format):
        if key_type == "Ed25519":
            ed = asymmetric.ed25519.Ed25519PrivateKey
        elif key_type == "Ed448":
            ed = asymmetric.ed448.Ed448PrivateKey
        else:
            raise ValueError

        if key_source:
            ed_private_key = ed.generate()
            ed_public_key = ed_private_key.public_key()

        elif not key_source:
            if byte_format == "Base64":
                ed_public_bytes = base64.b64decode(public_bytes).encode("utf-8")
            elif byte_format == "Hexadecimal":
                ed_public_bytes = bytes.fromhex(public_bytes)
            elif byte_format == "String":
                ed_public_bytes = public_bytes.encode("utf-8")
            elif byte_format == "Binary":
                ed_public_bytes = bytes(int(b, 2) for b in public_bytes.split(" "))
            else:
                raise ValueError
            ed_public_key = ed.from_public_bytes(ed_public_bytes)
        decoded_signature = bytes.fromhex(signature)
        try:
            ed_public_key.verify(decoded_signature, message)
            output = True
        except InvalidSignature:
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
