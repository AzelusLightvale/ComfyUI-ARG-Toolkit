from cryptography.hazmat.primitives import hashes  # For the algorithm functions

# Import hell
import cryptography
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash, ConcatKDFHMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from cryptography.hazmat.primitives.kdf.kbkdf import Mode, CounterLocation
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF

from cryptography.exceptions import InvalidKey
from cryptography.exceptions import AlreadyFinalized

# Why does the entire Key Derivation Function section of cryptography work like this? Just...why?
# TODO: Write NIST a strongly worded letter complaining about this categorization system, regret writing the thing in the first place, then burn it.


class KeyDerivationNodes:
    CATEGORY = "Cryptography/Modern/Key Derivation"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "length": (
                    "INT",
                    {
                        "default": 32,
                        "min": 16,
                        "max": 256,
                        "step": 16,
                        "tooltip": "The desired length of the derived key in bytes.",
                    },
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
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("derived_key",)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


# The special child with pre-bundled PHC-encoded strings available.
# TODO: Implement a PHC-encoded version for every other algorithm


class Argon2id_Derive(KeyDerivationNodes):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["salt"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "forceInput": True,
                "tooltip": "The nonce used to generate the key. Use SystemRandom (Random Nonce Generator) to generate this.",
            },
        )
        class_input["required"]["mode"] = (
            "BOOLEAN",
            {"label_on": "string", "label_off": "phc", "default": True},
        )
        class_input["required"]["iterations"] = (
            "INT",
            {
                "default": 1,
                "min": 1,
                "tooltip": "Also known as passes, this is used to tune the running time independently of the memory size.",
            },
        )
        class_input["required"]["parallel_lanes"] = (
            "INT",
            {
                "default": 4,
                "tooltip": "The number of lanes (parallel threads) to use. Also known as parallelism.",
            },
        )
        class_input["required"]["memory_cost"] = (
            "INT",
            {
                "default": 65536,
                "min": 1,
                "step": 1,
                "tooltip": "The amount of memory to use in kibibytes. 1 kibibyte (KiB) is 1024 bytes. This must be at minimum `8 * parallel_lanes`. However, due to ComfyUI limitations, the memory cost will be purposefully limited to 8*2048 KiB, or 16 MiB (Mebibytes)",
            },
        )
        class_input["optional"]["ad"] = (
            "STRING",
            {"default": "", "multiline": False, "tooltip": "Optional associated data."},
        )
        class_input["optional"]["secret"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Optional secret data, to be used for keyed hashing.",
            },
        )
        return class_input

    def argon2id_derive(
        self,
        message,
        length,
        salt,
        iterations,
        parallel_lanes,
        memory_cost,
        ad,
        secret,
        mode,
    ):
        if 8 * memory_cost < 8 * parallel_lanes:
            print(
                f"[WARNING]: Because defined memory cost ({8 * memory_cost} KiB) is lower than the minimum required ({8 * parallel_lanes} KiB), the value will be silently clamped to the minimum."
            )
            memory_cost = 8 * parallel_lanes
        else:
            memory_cost = 8 * memory_cost  # To actually convert this to a proper amount of defined kibibytes.
        ad = ad.encode("utf-8")
        secret = secret.encode("utf-8")
        salt = bytes.fromhex(salt)
        message = message.encode("utf-8")
        argon2_key = Argon2id(
            salt=salt,
            length=length,
            iterations=iterations,
            parallel_lanes=parallel_lanes,
            memory_cost=memory_cost,
            ad=ad,
            secret=secret,
        )
        if mode:
            output = argon2_key.derive(message)
            output = output.hex()
        else:
            output = argon2_key.derive_phc_encoded(message)
        return (output,)


class Argon2id_Verify(Argon2id_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def argon2id_verify(
        self,
        message,
        length,
        salt,
        iterations,
        parallel_lanes,
        memory_cost,
        ad,
        secret,
        mode,
        expected_key,
    ):
        if 8 * memory_cost < 8 * parallel_lanes:
            print(
                f"[WARNING]: Because defined memory cost ({8 * memory_cost} KiB) is lower than the minimum required ({8 * parallel_lanes} KiB), the value will be silently clamped to the minimum."
            )
            memory_cost = 8 * parallel_lanes
        else:
            memory_cost = 8 * memory_cost  # To actually convert this to a proper amount of defined kibibytes.
        salt = bytes.fromhex(salt)
        ad = ad.encode("utf-8")
        secret = secret.encode("utf-8")
        argon2_key = Argon2id(salt, length, iterations, parallel_lanes, memory_cost, ad, secret)

        if mode:
            expected_key = bytes.fromhex(expected_key)
            message = message.encode("utf-8")
            try:
                argon2_key.verify(message, expected_key)
                output = True
            except InvalidKey:
                output = False
            except AlreadyFinalized:
                raise RuntimeError(
                    "The verification function is being called more than once on a finalized KDF target. This should not be happening."
                )
        else:
            expected_key = str(expected_key)
            message = str(message)
            # For some stupid reason, PHC-formatted strings have to be done in string form, not hex or base64...
            try:
                argon2_key.verify_phc_encoded(message, expected_key, secret)
                output = True
            except InvalidKey:
                output = False
            except AlreadyFinalized:
                raise RuntimeError(
                    "The verification function is being called more than once on a finalized KDF target. This should not be happening."
                )
        return (output,)


class PBKDF2HMAC_Derive(KeyDerivationNodes):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["salt"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "forceInput": True,
                "tooltip": "The nonce used to generate the key. Use SystemRandom (Random Nonce Generator) to generate this.",
            },
        )
        class_input["required"]["algorithm"] = (
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["required"]["iterations"] = (
            "INT",
            {
                "default": 1200000,
                "tooltip": "The number of iterations to perform of the hash function. This can be used to control the length of time the operation takes. Higher numbers help mitigate brute force attacks against derived keys.",
                "min": 1,
            },
        )
        return class_input

    def pbkdf2hmac_derive(self, message, length, salt, iterations, algorithm):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        salt = bytes.fromhex(salt)
        message = message.encode("utf-8")
        pbkdf2hmac_key = PBKDF2HMAC(salt=salt, length=length, iterations=iterations, algorithm=digest)
        output = pbkdf2hmac_key.derive(message)
        output = output.hex()
        return (output,)


class PBKDF2HMAC_Verify(PBKDF2HMAC_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def pbkdf2hmac_verify(self, message, length, salt, iterations, algorithm, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        salt = bytes.fromhex(salt)
        message = message.encode("utf-8")
        pbkdf2hmac_key = PBKDF2HMAC(salt=salt, length=length, iterations=iterations, algorithm=digest)
        expected_key = bytes.fromhex(expected_key)
        try:
            pbkdf2hmac_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class Scrypt_Derive(KeyDerivationNodes):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["salt"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "forceInput": True,
                "tooltip": "The nonce used to generate the key. Use SystemRandom (Random Nonce Generator) to generate this.",
            },
        )
        class_input["required"]["n"] = (
            "INT",
            {
                "default": 14,
                "tooltip": "The CPU/Memory cost parameter. Normally, this must be larger than one and a power of 2. This specific implementation uses the direct power to exponentiate 2, minimum 1.",
                "min": 1,
            },
        )
        class_input["required"]["r"] = (
            "INT",
            {
                "default": 8,
                "tooltip": "The block size parameter. Affects computation costs.",
                "min": 1,
            },
        )
        class_input["required"]["p"] = (
            "INT",
            {
                "default": 1,
                "tooltip": "The parallel factor parameter. Affects computation costs.",
                "min": 1,
            },
        )
        return class_input

    def scrypt_derive(self, message, length, salt, n, r, p):
        salt = bytes.fromhex(salt)
        message = message.encode("utf-8")
        n = 2**n
        scrypt_key = Scrypt(salt, length, n, r, p)
        output = scrypt_key.derive(message)
        output = output.hex()
        return (output,)


class Scrypt_Verify(Scrypt_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def scrypt_verify(self, message, length, salt, n, r, p, expected_key):
        salt = bytes.fromhex(salt)
        message = message.encode("utf-8")
        n = 2**n
        scrypt_key = Scrypt(salt, length, n, r, p)
        expected_key = bytes.fromhex(expected_key)
        try:
            scrypt_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


# Fixed cost algorithms
class ConcatKDFHash_Derive(KeyDerivationNodes):
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["optional"]["other_info"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )
        return class_input

    def concatkdfhash_derive(self, message, length, algorithm, other_info):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        other_info = other_info.encode("utf-8")
        ckdfhash_key = ConcatKDFHash(length=length, algorithm=digest, otherinfo=other_info)
        output = ckdfhash_key.derive(message)
        output = output.hex()
        return (output,)


class ConcatKDFHash_Verify(ConcatKDFHash_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def concatkdfhash_verify(self, message, length, algorithm, other_info, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        other_info = other_info.encode("utf-8")
        ckdfhash_key = ConcatKDFHash(length=length, algorithm=digest, otherinfo=other_info)
        expected_key = bytes.fromhex(expected_key)
        try:
            ckdfhash_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class ConcatKDFHMAC_Derive(ConcatKDFHash_Derive):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["optional"]["salt"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "A salt. Optional, but highly recommended, ideally with as many bits of entropy as the security level of the hash function.",
            },
        )
        return class_input

    def concatkdfhmac_derive(self, message, length, algorithm, other_info, salt):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        other_info = other_info.encode("utf-8")
        salt = bytes.fromhex(salt)
        ckdfhmac_key = ConcatKDFHMAC(length=length, algorithm=digest, otherinfo=other_info, salt=salt)
        output = ckdfhmac_key.derive(message)
        output = output.hex()
        return (output,)


class ConcatKDFHMAC_Verify(ConcatKDFHMAC_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def concatkdfhmac_verify(self, message, length, algorithm, other_info, salt, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        other_info = other_info.encode("utf-8")
        salt = bytes.fromhex(salt)
        ckdfhash_key = ConcatKDFHMAC(length=length, algorithm=digest, otherinfo=other_info, salt=salt)
        expected_key = bytes.fromhex(expected_key)
        try:
            ckdfhash_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class HKDF_Derive(KeyDerivationNodes):
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["optional"]["salt"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "forceInput": True,
                "tooltip": "A salt to randomize the KDF's output. Optional, but highly recommended.",
            },
        )
        class_input["optional"]["info"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def hkdf_derive(self, message, length, algorithm, salt, info):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        salt = bytes.fromhex(salt)
        info = info.encode("utf-8")
        hkdf_key = HKDF(algorithm=digest, length=length, salt=salt, info=info)
        output = hkdf_key.derive(message)
        output = output.hex()
        return (output,)


class HKDF_Verify(HKDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def hkdf_verify(self, message, length, algorithm, info, salt, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        info = info.encode("utf-8")
        salt = bytes.fromhex(salt)
        hkdf_key = HKDF(length=length, algorithm=digest, info=info, salt=salt)
        expected_key = bytes.fromhex(expected_key)
        try:
            hkdf_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class HKDFExpand_Derive(KeyDerivationNodes):
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["optional"]["info"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def hkdfexpand_derive(self, message, length, algorithm, info):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        info = info.encode("utf-8")
        hkdf_key = HKDFExpand(algorithm=digest, length=length, info=info)
        output = hkdf_key.derive(message)
        output = output.hex()
        return (output,)


class HKDFExpand_Verify(HKDFExpand_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def hkdfexpand_verify(self, message, length, algorithm, info, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        info = info.encode("utf-8")
        hkdf_key = HKDF(length=length, algorithm=digest, info=info)
        expected_key = bytes.fromhex(expected_key)
        try:
            hkdf_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class X963KDF_Derive(KeyDerivationNodes):
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["optional"]["info"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def x963kdf_derive(self, message, length, algorithm, info):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        info = info.encode("utf-8")
        x963kdf_key = X963KDF(algorithm=digest, length=length, info=info)
        output = x963kdf_key.derive(message)
        output = output.hex()
        return (output,)


class X963KDF_Verify(X963KDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def x963kdf_verify(self, message, length, algorithm, info, expected_key):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        info = info.encode("utf-8")
        x963kdf_key = X963KDF(length=length, algorithm=digest, info=info)
        expected_key = bytes.fromhex(expected_key)
        try:
            x963kdf_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


class KBKDF_Derive(KeyDerivationNodes):
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
            {"tooltip": "The algorithm to use for hash generation."},
        )
        class_input["required"]["rlen"] = ("INT", {"default": 4, "min": 1})
        class_input["required"]["llen"] = ("INT", {"default": 4, "min": 1})
        class_input["required"]["location"] = (
            [
                "BeforeFixed",
                "AfterFixed",
                "MiddleFixed",
            ],
            {
                "default": "BeforeFixed",
                "tooltip": "The location to put the counter bytes.",
            },
        )
        class_input["required"]["operation_mode"] = (
            ["KBKDFHMAC", "KBKDFCMAC"],
            {"default": "KBKDFHMAC", "tooltip": "The operation mode to use."},
        )
        class_input["optional"]["label"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific label information",
            },
        )
        class_input["optional"]["context"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Application-specific context information",
            },
        )
        class_input["optional"]["fixed"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "Instead of supplying `label` and `context`, you can supply fixed data in this field instead. Note that if this is specified, `label` and `context` will be ignored.",
            },
        )
        class_input["optional"]["break_location"] = (
            "INT",
            {
                "default": 0,
                "min": 0,
                "tooltip": "When MiddleFixed is chosen as the counter location method, this field will be used to indicate the bytes offset where counter bytes are to be located.",
            },
        )
        return class_input

    def kbkdf_derive(
        self,
        message,
        length,
        algorithm,
        rlen,
        llen,
        location,
        label,
        context,
        operation_mode,
        break_location=None,
        fixed=None,
    ):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        label = label.encode("utf-8")
        context = context.encode("utf-8")
        fixed = fixed.encode("utf-8")
        location = getattr(CounterLocation, location)
        kbkdf_key = getattr(cryptography.hazmat.primitives.kdf.kbkdf, operation_mode)(
            length=length,
            algorithm=digest,
            mode=Mode.CounterMode,
            rlen=rlen,
            llen=llen,
            location=location,
            label=label,
            context=context,
            fixed=fixed,
            break_location=break_location,
        )
        output = kbkdf_key.derive(message)
        output = output.hex()
        return (output,)


class KBKDF_Verify(KBKDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def kbkdf_verify(
        self,
        message,
        length,
        algorithm,
        rlen,
        llen,
        location,
        label,
        context,
        expected_key,
        operation_mode,
        break_location=None,
        fixed=None,
    ):
        if algorithm == "BLAKE2b":
            digest = getattr(hashes, algorithm)(64)
        elif algorithm == "BLAKE2s":
            digest = getattr(hashes, algorithm)(32)
        else:
            digest = getattr(hashes, algorithm)()
        message = message.encode("utf-8")
        label = label.encode("utf-8")
        context = context.encode("utf-8")
        fixed = fixed.encode("utf-8")
        location = getattr(CounterLocation, location)
        kbkdf_key = getattr(cryptography.hazmat.primitives.kdf.kbkdf, operation_mode)(
            length=length,
            algorithm=digest,
            mode=Mode.CounterMode,
            rlen=rlen,
            llen=llen,
            location=location,
            label=label,
            context=context,
            fixed=fixed,
            break_location=break_location,
        )
        expected_key = bytes.fromhex(expected_key)
        try:
            kbkdf_key.verify(message, expected_key)
            output = True
        except InvalidKey:
            output = False
        except AlreadyFinalized:
            raise RuntimeError(
                "The verification function is being called more than once on a finalized KDF target. This should not be happening."
            )
        return (output,)


NODE_CLASS_MAPPINGS = {
    "Argon2id_Derive": Argon2id_Derive,
    "Argon2id_Verify": Argon2id_Verify,
    "PBKDF2HMAC_Derive": PBKDF2HMAC_Derive,
    "PBKDF2HMAC_Verify": PBKDF2HMAC_Verify,
    "Scrypt_Derive": Scrypt_Derive,
    "Scrypt_Verify": Scrypt_Verify,
    "ConcatKDFHash_Derive": ConcatKDFHash_Derive,
    "ConcatKDFHash_Verify": ConcatKDFHash_Verify,
    "ConcatKDFHMAC_Derive": ConcatKDFHMAC_Derive,
    "ConcatKDFHMAC_Verify": ConcatKDFHMAC_Verify,
    "HKDF_Derive": HKDF_Derive,
    "HKDF_Verify": HKDF_Verify,
    "HKDFExpand_Derive": HKDFExpand_Derive,
    "HKDFExpand_Verify": HKDFExpand_Verify,
    "X963KDF_Derive": X963KDF_Derive,
    "X963KDF_Verify": X963KDF_Verify,
    "KBKDF_Derive": KBKDF_Derive,
    "KBKDF_Verify": KBKDF_Verify,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Argon2id_Derive": "Argon2id Key Derivation",
    "Argon2id_Verify": "Argon2id Key Verification",
    "PBKDF2HMAC_Derive": "PBKDF2HMAC Key Derivation",
    "PBKDF2HMAC_Verify": "PBKDF2HMAC Key Verification",
    "Scrypt_Derive": "Scrypt Key Derivation",
    "Scrypt_Verify": "Scrypt Key Verification",
    "ConcatKDFHash_Derive": "ConcatKDF (Hash) Key Derivation",
    "ConcatKDFHash_Verify": "ConcatKDF (Hash) Key Verification",
    "ConcatKDFHMAC_Derive": "ConcatKDF (HMAC) Key Derivation",
    "ConcatKDFHMAC_Verify": "ConcatKDF (HMAC) Key Verification",
    "HKDF_Derive": "HKDF Key Derivation",
    "HKDF_Verify": "HKDF Key Verification",
    "HKDFExpand_Derive": "HKDF (Expand Only) Key Derivation",
    "HKDFExpand_Verify": "HKDF (Expand Only) Key Verification",
    "X963KDF_Derive": "X963KDF Key Derivation",
    "X963KDF_Verify": "X963KDF Key Verification",
    "KBKDF_Derive": "KBKDF Key Derivation",
    "KBKDF_Verify": "KBKDF Key Verification",
}
