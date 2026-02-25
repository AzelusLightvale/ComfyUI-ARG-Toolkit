# Elliptic curve (X/EC) Diffie-Hellman (DH) key exchange
from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization
import base64


class InitNode:
    CATEGORY = "Cryptography/Modern/Asymmetric"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


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

    def xprivatekeyformat(self, key_type, encoding_format, formatting, encryption_algorithm, conversion_format, encryption_password):
        if key_type == "x25519":
            ed = asymmetric.x25519.X25519PrivateKey
        elif key_type == "x448":
            ed = asymmetric.x448.X448PrivateKey
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
                    },
                ),
                "key_type": (
                    ["x25519", "x448"],
                    {"default": "x25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
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

    def public_key_init(self, key_source, key_type, private_bytes, byte_format):
        if key_type == "x25519":
            ed = asymmetric.x25519.X25519PrivateKey
        elif key_type == "x448":
            ed = asymmetric.x448.X448PrivateKey
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

    def xpublickeyformat(self, key_source, key_type, encoding_format, conversion_format, formatting, private_bytes, byte_format):
        ed_private_key = self.public_key_init(key_source, key_type, private_bytes, byte_format)
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
                    },
                ),
                "key_type": (
                    ["x25519", "x448"],
                    {"default": "x25519", "description": "The key type to use for EdDSA-based asymmetric signing algorithms."},
                ),
                "public_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The public key (assumed in Raw formatting) to derive the shared key from. Uses the format from byte_format",
                    },
                ),
            },
            "optional": {
                "private_bytes": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Only applicable if key_source is set to From Private Bytes. Uses the format from byte_format.",
                    },
                ),
                "byte_format": (["Base64", "Hexadecimal", "String", "Binary"], {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("signature",)

    def byte_formatter(self, byte_format, message: str):
        if byte_format == "Base64":
            message = base64.b64decode(message)
        elif byte_format == "Hexadecimal":
            message = bytes.fromhex(message)
        elif byte_format == "String":
            message = message.encode("utf-8")
        elif byte_format == "Binary":
            message = bytes(int(b, 2) for b in message.split(" "))
        else:
            raise ValueError
        return message

    def xexchange(self, key_source, key_type, public_key, private_bytes, byte_format):
        if key_type == "x25519":
            ed = asymmetric.x25519.X25519PrivateKey
        elif key_type == "x448":
            ed = asymmetric.x448.X448PrivateKey
        else:
            raise ValueError
        if key_source:
            private_key = ed.generate()
        elif not key_source:
            private_bytes = self.byte_formatter(byte_format, private_bytes)
            private_key = ed.from_private_bytes(private_bytes)
        public_keyform = self.byte_formatter(byte_format, public_key)
        if key_type == "x25519":
            ed = asymmetric.x25519.X25519PublicKey.from_public_bytes(public_keyform)
        elif key_type == "x448":
            ed = asymmetric.x448.X448PublicKey.from_public_bytes(public_keyform)
        else:
            raise ValueError
        shared_key = private_key.exchange(public_key)
        output_key = self.byte_formatter(byte_format, shared_key)
        return (output_key,)


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
