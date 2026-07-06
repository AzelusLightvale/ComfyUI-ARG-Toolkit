from cryptography.hazmat.primitives import serialization


# Key loader nodes
class KeyInitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    RETURN_TYPES = ("KEYOBJ",)
    RETURN_NAMES = ("loaded_key",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keyfile": ("BYTESLIKE", {"forceInput": True}),
            },
            "optional": {},
        }


class PEMPrivateKey(KeyInitNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["optional"]["password"] = ("BYTESLIKE", {"forceInput": True, "default": None})
        return class_input

    def execute(self, keyfile, password=None):
        loaded_key = serialization.load_pem_private_key(keyfile, password)
        return (loaded_key,)


class PEMPublicKey(KeyInitNode):
    def execute(self, keyfile):
        loaded_key = serialization.load_pem_public_key(keyfile)
        return (loaded_key,)


class DERPrivateKey(KeyInitNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["optional"]["password"] = ("BYTESLIKE", {"forceInput": True, "default": None})
        return class_input

    def execute(self, keyfile, password=None):
        loaded_key = serialization.load_der_private_key(keyfile, password)
        return (loaded_key,)


class DERPublicKey(KeyInitNode):
    def execute(self, keyfile):
        loaded_key = serialization.load_der_public_key(keyfile)
        return (loaded_key,)


NODE_CLASS_MAPPINGS = {
    "PEMPrivateKey": PEMPrivateKey,
    "PEMPublicKey": PEMPublicKey,
    "DERPrivateKey": DERPrivateKey,
    "DERPublicKey": DERPublicKey,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "PEMPrivateKey": "PEM Serialized Private Key Loader",
    "PEMPublicKey": "PEM Serialized Public Key Loader",
    "DERPrivateKey": "DER Serialized Private Key Loader",
    "DERPublicKey": "DER Serialized Public Key Loader",
}
