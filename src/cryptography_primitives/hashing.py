from cryptography.hazmat.primitives import hashes


class DynamicInputContainer(dict):
    def __contains__(self, item):
        return item.startswith("key") and item != "key1"

    def __getitem__(self, key):
        return ("BYTESLIKE", {})

    def keys(self):
        return []

    def __iter__(self):
        return iter(self.keys())


class Hash:
    CATEGORY = "Cryptography/Modern/Hashing"

    @classmethod
    def INPUT_TYPES(cls):
        mandatory_inputs = {
            "key1": (
                "BYTESLIKE",
                {"forceInput": True, "default": "", "tooltip": "First key (mandatory)"},
            )
        }

        optional_inputs = DynamicInputContainer()

        return {
            "required": mandatory_inputs,
            "optional": optional_inputs,
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def main_method(self, algorithm, digest_size=None, **kwargs):
        if algorithm == "BLAKE2b" or algorithm == "BLAKE2s":
            digest = hashes.Hash(getattr(hashes, algorithm)(int(digest_size)))
        else:
            digest = hashes.Hash(getattr(hashes, algorithm)())

        # Process dynamic optional keys
        for key, value in sorted(kwargs.items()):
            if key.startswith("key") and value is not None:
                if isinstance(value, (list, tuple)):
                    for v in value:
                        digest.update(v)
                else:
                    digest.update(value)

        return (digest.finalize(),)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("hash_bytes",)


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

    def sha2(self, algorithm, **kwargs):
        return self.main_method(algorithm, **kwargs)


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

    def blake2(self, algorithm, **kwargs):
        if algorithm == "BLAKE2b":
            digest_size = 32
        elif algorithm == "BLAKE2s":
            digest_size = 64
        return self.main_method(algorithm, digest_size, **kwargs)


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

    def sha3(self, algorithm, **kwargs):
        return self.main_method(algorithm, **kwargs)


class SHA1(Hash):
    def sha1(self, algorithm=None, **kwargs):
        algorithm = "SHA1"
        return self.main_method(algorithm, **kwargs)


class MD5(Hash):
    def md5(self, algorithm=None, **kwargs):
        algorithm = "MD5"
        return self.main_method(algorithm, **kwargs)


class SM3(Hash):
    def sm3(self, algorithm=None, **kwargs):
        algorithm = "SM3"
        return self.main_method(algorithm, **kwargs)


class XOFHash(Hash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["squeeze_bytes"] = (
            "INT",
            {"default": 16, "tooltip": "The amount of bytes to squeeze."},
        )
        class_input["required"]["squeeze_times"] = (
            "INT",
            {"default": 1, "tooltip": "The amount of times to squeeze."},
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

    def main_method_xof(self, algorithm, squeeze_bytes, squeeze_times, digest_size, **kwargs):
        # Initialize hash object
        digest = hashes.XOFHash(getattr(hashes, algorithm)(digest_size))
        x = 0

        # Sort kwargs keys to ensure deterministic order (optional)
        for key, value in sorted(kwargs.items()):
            if key.startswith("key") and key != "key1" and value is not None:
                if isinstance(value, (list, tuple)):
                    for v in value:
                        digest.update(v)
                else:
                    digest.update(value)

        # Squeeze loop to define how many keys to output
        while x != squeeze_times:
            digest.squeeze(squeeze_bytes)
            x = x + 1

        # Finalize
        outputs = hashes.Hash(getattr(hashes, algorithm)(digest_size)).finalize()
        return (outputs,)


class SHAKE(XOFHash):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["algorithm"] = (
            [
                "SHAKE_128",
                "SHAKE_256",
            ],
            {},
        )
        return class_input

    def shake(self, algorithm, squeeze_bytes, squeeze_times, digest_size, **kwargs):
        return (self.main_method_xof(algorithm, squeeze_bytes, squeeze_times, digest_size, **kwargs),)


NODE_CLASS_MAPPINGS = {
    "SHA2": SHA2,
    "BLAKE2": BLAKE2,
    "SHA3": SHA3,
    "SHA1": SHA1,
    "MD5": MD5,
    "SM3": SM3,
    "SHAKE": SHAKE,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SHA2": "SHA-2 Hashing",
    "BLAKE2": "BLAKE2 Hashing",
    "SHA3": "SHA-3 Hashing",
    "SHA1": "SHA-1 Hashing",
    "MD5": "MD5 Hashing",
    "SM3": "SM3 Hashing",
    "SHAKE": "SHAKE Hashing",
}
