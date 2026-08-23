from cryptography.hazmat.primitives import hashes


class Hash:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Hashing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": (
                    "BYTESLIKE",
                    {"forceInput": True, "default": "", "tooltip": "First key (mandatory)"},
                )
            }
        }

    def main_method(self, algorithm, key, digest_size=None):
        if algorithm in ["BLAKE2b", "BLAKE2s", "SHAKE128", "SHAKE256"]:
            digest = hashes.Hash(getattr(hashes, algorithm)(int(digest_size)))
        else:
            digest = hashes.Hash(getattr(hashes, algorithm)())
        digest.update(key)
        return (digest.finalize(),)

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("hash_bytes",)
    FUNCTION = "execute"


class SHA2(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["algorithm"] = (
            [
                "SHA224",
                "SHA256",
                "SHA384",
                "SHA512",
                "SHA512_224",
                "SHA512_256",
            ],
            {},
        )
        return class_input

    def execute(self, algorithm, key):
        return self.main_method(algorithm, key)


class BLAKE2(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["algorithm"] = (
            [
                "BLAKE2b",
                "BLAKE2s",
            ],
            {},
        )
        return class_input

    def execute(self, algorithm, key):
        if algorithm == "BLAKE2b":
            digest_size = 32
        elif algorithm == "BLAKE2s":
            digest_size = 64
        return self.main_method(algorithm, key, digest_size)


class SHA3(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["algorithm"] = (
            [
                "SHA3_224",
                "SHA3_256",
                "SHA3_384",
                "SHA3_512",
            ],
            {},
        )
        return class_input

    def execute(self, algorithm, key):
        return self.main_method(algorithm, key)


class SHA1(Hash):
    def execute(self, key, algorithm=None):
        algorithm = "SHA1"
        return self.main_method(algorithm, key)


class MD5(Hash):
    def execute(self, key, algorithm=None):
        algorithm = "MD5"
        return self.main_method(algorithm, key)


class SM3(Hash):
    def execute(self, key, algorithm=None):
        algorithm = "SM3"
        return self.main_method(algorithm, key)


class HashSHAKE(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["digest_size"] = (
            "INT",
            {
                "default": 32,
                "min": 1,
                "tooltip": "The length of output desired (in bytes)",
            },
        )
        class_input["required"]["algorithm"] = (
            [
                "SHAKE128",
                "SHAKE256",
            ],
            {"defaull": "SHAKE128", "tooltip": "The algorithm for hashing."},
        )
        return class_input

    def execute(self, key, algorithm, digest_size):
        return self.main_method(algorithm, key, digest_size)


class XOFHash(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["squeeze_bytes"] = (
            "INT",
            {"default": 16, "tooltip": "The amount of bytes to squeeze."},
        )
        class_input["required"]["digest_size"] = (
            "INT",
            {
                "default": 32,
                "min": 1,
                "tooltip": "The length of output desired (in bytes)",
            },
        )
        return class_input

    def main_method_xof(self, squeeze_bytes, algorithm, key, digest_size):
        digest = hashes.XOFHash(getattr(hashes, algorithm)(digest_size))
        digest.update(key)
        outputs = bytes(digest.squeeze(squeeze_bytes))
        return outputs


class XOFSHAKE(XOFHash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["algorithm"] = (
            [
                "SHAKE128",
                "SHAKE256",
            ],
            {"defaull": "SHAKE128", "tooltip": "The algorithm for hashing."},
        )
        return class_input

    def execute(self, algorithm, key, squeeze_bytes, digest_size):
        return (self.main_method_xof(squeeze_bytes, algorithm, key, digest_size),)


NODE_CLASS_MAPPINGS = {
    "SHA2": SHA2,
    "BLAKE2": BLAKE2,
    "SHA3": SHA3,
    "SHA1": SHA1,
    "MD5": MD5,
    "SM3": SM3,
    "XOFSHAKE": XOFSHAKE,
    "HashSHAKE": HashSHAKE,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SHA2": "SHA-2 Hashing",
    "BLAKE2": "BLAKE2 Hashing",
    "SHA3": "SHA-3 Hashing",
    "SHA1": "SHA-1 Hashing",
    "MD5": "MD5 Hashing",
    "SM3": "SM3 Hashing",
    "XOFSHAKE": "SHAKE XOF Hashing",
    "HashSHAKE": "SHAKE Hashing",
}
