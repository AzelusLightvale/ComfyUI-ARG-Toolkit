from cryptography.hazmat.primitives import serialization, hashes


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
                "keyfile": ("BYTESLIKE", {"forceInput": True},),
            },
            "optional": {},
        }

# PEM keys
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

# DER keys
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

# SSH keys and fingerprint 
class SSHPublicKey(KeyInitNode):
    def execute(self, keyfile):
        loaded_key = serialization.load_ssh_public_key(keyfile)
        return (loaded_key,)

class SSHPublicKeyFingerprint(KeyInitNode):
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("fingerprint",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["hash_algorithm"] = (["MD5", "SHA-1", "SHA-256"], {"default": "SHA-256",})
        return class_input

    def execute(self, keyfile, hash_algorithm):
        loaded_key = serialization.load_ssh_public_key(keyfile)
        match hash_algorithm:
            case "MD5":
                algorithm = hashes.MD5()
            case "SHA-1":
                algorithm = hashes.SHA1()
            case "SHA-256":
                algorithm = hashes.SHA256()
        signature = serialization.ssh_key_fingerprint(loaded_key, algorithm)
        return (bytes(signature),)

class SSHPrivateKey(KeyInitNode):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["optional"]["password"] = ("BYTESLIKE", {"forceInput": True, "default": None})
        class_input["optional"]["skip_rsa_key_validation"] = ("BOOLEAN", {"default": False, "tooltip": "Unless you know what you're doing, do not change this. Disabling RSA key validation speeds up key loading, but is **unsafe** and may cause OpenSSL to misbehave or crash, potentially dragging ComfyUI down with it."})
        return class_input

    def execute(self, keyfile, password=None, skip_rsa_key_validation=False):
        loaded_key = serialization.load_ssh_private_key(keyfile, password, unsafe_skip_rsa_key_validation=skip_rsa_key_validation)
        return (loaded_key,)

class SSHPublicIdentity(KeyInitNode):
    RETURN_TYPES = ("BYTESLIKE", "BYTESLIKE",)
    RETURN_NAMES = ("certificate", "key")

    def execute(self, keyfile):
        loaded_key = serialization.load_ssh_public_identity(keyfile)
        if isinstance(loaded_key, serialization.SSHCertificate):
            return (loaded_key, loaded_key.public_key())
        elif isinstance(loaded_key, serialization.SSHCertPublicKeyTypes):
            return (None, loaded_key)
        else:
            raise ValueError("Invalid key. Check your inputs again.")


NODE_CLASS_MAPPINGS = {
    "PEMPrivateKey": PEMPrivateKey,
    "PEMPublicKey": PEMPublicKey,
    "DERPrivateKey": DERPrivateKey,
    "DERPublicKey": DERPublicKey,
    "SSHPublicKey": SSHPublicKey,
    "SSHPublicKeyFingerprint": SSHPublicKeyFingerprint,
    "SSHPrivateKey": SSHPrivateKey,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "PEMPrivateKey": "PEM Serialized Private Key Loader",
    "PEMPublicKey": "PEM Serialized Public Key Loader",
    "DERPrivateKey": "DER Serialized Private Key Loader",
    "DERPublicKey": "DER Serialized Public Key Loader",
    "SSHPublicKey": "OpenSSH Serialized Public Key Loader",
    "SSHPublicKeyFingerprint": "OpenSSH Public Key Fingerprint",
    "SSHPrivateKey": "OpenSSH Serialized Private Key Loader",
}
