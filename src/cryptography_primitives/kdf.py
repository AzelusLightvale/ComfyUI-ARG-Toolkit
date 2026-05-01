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


def _get_hash_algorithm(name):
    """Gets a hash algorithm instance from its name."""
    if name == "BLAKE2b":
        return getattr(hashes, name)(64)
    elif name == "BLAKE2s":
        return getattr(hashes, name)(32)
    else:
        return getattr(hashes, name)()


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
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The message to derive key from. Must be bytes.",
                    },
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("BYTESLIKE",)
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
            "BYTESLIKE",
            {
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
                "max": 2147483647,
                "step": 1,
                "tooltip": "The amount of memory to use in kibibytes. 1 kibibyte (KiB) is 1024 bytes. This must be at minimum `8 * parallel_lanes`.",
            },
        )
        class_input["optional"]["ad"] = (
            "BYTESLIKE",
            {"forceInput": True, "tooltip": "Optional associated data."},
        )
        class_input["optional"]["secret"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Optional secret data, to be used for keyed hashing.",
            },
        )
        return class_input

    def _get_kdf(self, salt, length, iterations, parallel_lanes, memory_cost, ad, secret):
        min_memory_cost = 8 * parallel_lanes
        if memory_cost < min_memory_cost:
            print(
                f"[ComfyUI ARG Toolkit][WARNING]: Because defined memory cost ({memory_cost} KiB) is lower than the minimum required ({min_memory_cost} KiB), the value will be silently clamped to the minimum."
            )
            memory_cost = min_memory_cost

        return Argon2id(
            salt=salt,
            length=length,
            iterations=iterations,
            lanes=parallel_lanes,
            memory_cost=memory_cost,
            ad=ad,
            secret=secret,
        )

    def argon2id_derive(self, message, length, salt, iterations, parallel_lanes, memory_cost, ad, secret, mode):
        argon2_key = self._get_kdf(salt, length, iterations, parallel_lanes, memory_cost, ad, secret)
        if mode:
            output = argon2_key.derive(message)
        else:
            output = argon2_key.derive_phc_encoded(message)
            output = output.encode("utf-8")
        return (output,)


class Argon2id_Verify(Argon2id_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def argon2id_verify(self, message, length, salt, iterations, parallel_lanes, memory_cost, ad, secret, mode, expected_key):
        argon2_key = self._get_kdf(salt, length, iterations, parallel_lanes, memory_cost, ad, secret)

        if mode:
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
            # For some stupid reason, PHC-formatted strings have to be done in string form, not hex or base64...
            try:
                argon2_key.verify_phc_encoded(message, expected_key.decode("utf-8"), secret)
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
            "BYTESLIKE",
            {
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
                "max": 2147483647,
            },
        )
        return class_input

    def _get_kdf(self, salt, length, iterations, algorithm):
        digest = _get_hash_algorithm(algorithm)
        return PBKDF2HMAC(salt=salt, length=length, iterations=iterations, algorithm=digest)

    def pbkdf2hmac_derive(self, message, length, salt, iterations, algorithm):
        output = self._get_kdf(salt, length, iterations, algorithm).derive(message)
        return (output,)


class PBKDF2HMAC_Verify(PBKDF2HMAC_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def pbkdf2hmac_verify(self, message, length, salt, iterations, algorithm, expected_key):
        pbkdf2hmac_key = self._get_kdf(salt, length, iterations, algorithm)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The nonce used to generate the key. Use SystemRandom (Random Nonce Generator) to generate this.",
            },
        )
        class_input["required"]["n"] = (
            "INT",
            {
                "default": 14,
                "tooltip": "The CPU/Memory cost parameter. Normally, this must be larger than 1 and a power of 2. This specific implementation uses the direct power to exponentiate 2 (as in 2^n, or, in Python, `2**n`), minimum 1.",
                "min": 1,
            },
        )
        class_input["required"]["r"] = (
            "INT",
            {
                "default": 8,
                "tooltip": "The block size parameter. Affects memory costs and sequential memory-hard properties by controlling memory access patterns and memory block size.",
                "min": 1,
            },
        )
        class_input["required"]["p"] = (
            "INT",
            {
                "default": 1,
                "tooltip": "The parallel factor parameter. Affects the number of mixing functions to run in parallel. Can help in multi-core systems, but also makes it easier for attackers with parallel hardware.",
                "min": 1,
            },
        )
        return class_input

    def _get_kdf(self, salt, length, n, r, p):
        n_cost = 2**n
        return Scrypt(salt, length, n_cost, r, p)

    def scrypt_derive(self, message, length, salt, n, r, p):
        output = self._get_kdf(salt, length, n, r, p).derive(message)
        return (output,)


class Scrypt_Verify(Scrypt_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def scrypt_verify(self, message, length, salt, n, r, p, expected_key):
        scrypt_key = self._get_kdf(salt, length, n, r, p)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )
        return class_input

    def _get_kdf(self, length, algorithm, other_info):
        digest = _get_hash_algorithm(algorithm)
        if other_info is None:
            other_info = b""
        return ConcatKDFHash(length=length, algorithm=digest, otherinfo=other_info)

    def concatkdfhash_derive(self, message, length, algorithm, other_info):
        kdf = self._get_kdf(length, algorithm, other_info)
        return (kdf.derive(message),)


class ConcatKDFHash_Verify(ConcatKDFHash_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def concatkdfhash_verify(self, message, length, algorithm, other_info, expected_key):
        ckdfhash_key = self._get_kdf(length, algorithm, other_info)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "A salt. Optional, but highly recommended, ideally with as many bits of entropy as the security level of the hash function.",
            },
        )
        return class_input

    def _get_kdf(self, length, algorithm, other_info, salt):
        digest = _get_hash_algorithm(algorithm)
        if other_info is None:
            other_info = b""
        return ConcatKDFHMAC(length=length, algorithm=digest, otherinfo=other_info, salt=salt)

    def concatkdfhmac_derive(self, message, length, algorithm, other_info, salt):
        kdf = self._get_kdf(length, algorithm, other_info, salt)
        return (kdf.derive(message),)


class ConcatKDFHMAC_Verify(ConcatKDFHMAC_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def concatkdfhmac_verify(self, message, length, algorithm, other_info, salt, expected_key):
        ckdfhash_key = self._get_kdf(length, algorithm, other_info, salt)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "A salt to randomize the KDF's output. Optional, but highly recommended.",
            },
        )
        class_input["optional"]["info"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def _get_kdf(self, length, algorithm, salt, info):
        digest = _get_hash_algorithm(algorithm)
        if info is None:
            info = b""
        return HKDF(algorithm=digest, length=length, salt=salt, info=info)

    def hkdf_derive(self, message, length, algorithm, salt, info):
        kdf = self._get_kdf(length, algorithm, salt, info)
        return (kdf.derive(message),)


class HKDF_Verify(HKDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def hkdf_verify(self, message, length, algorithm, info, salt, expected_key):
        hkdf_key = self._get_kdf(length, algorithm, salt, info)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def _get_kdf(self, length, algorithm, info):
        digest = _get_hash_algorithm(algorithm)
        if info is None:
            info = b""
        return HKDFExpand(algorithm=digest, length=length, info=info)

    def hkdfexpand_derive(self, message, length, algorithm, info):
        kdf = self._get_kdf(length, algorithm, info)
        return (kdf.derive(message),)


class HKDFExpand_Verify(HKDFExpand_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def hkdfexpand_verify(self, message, length, algorithm, info, expected_key):
        hkdf_key = self._get_kdf(length, algorithm, info)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific context information. If left empty, will pass an empty byte string.",
            },
        )

        return class_input

    def _get_kdf(self, length, algorithm, info):
        digest = _get_hash_algorithm(algorithm)
        if info is None:
            info = b""
        return X963KDF(algorithm=digest, length=length, sharedinfo=info)

    def x963kdf_derive(self, message, length, algorithm, info):
        kdf = self._get_kdf(length, algorithm, info)
        return (kdf.derive(message),)


class X963KDF_Verify(X963KDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "The expected result of key derivation.",
            },
        )
        return class_input

    def x963kdf_verify(self, message, length, algorithm, info, expected_key):
        x963kdf_key = self._get_kdf(length, algorithm, info)
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
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific label information",
            },
        )
        class_input["optional"]["context"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
                "tooltip": "Application-specific context information",
            },
        )
        class_input["optional"]["fixed"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
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

    def _get_kdf(
        self,
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
        digest = _get_hash_algorithm(algorithm)
        location_enum = getattr(CounterLocation, location)
        kdf_class = getattr(cryptography.hazmat.primitives.kdf.kbkdf, operation_mode)
        return kdf_class(
            length=length,
            algorithm=digest,
            mode=Mode.CounterMode,
            rlen=rlen,
            llen=llen,
            location=location_enum,
            label=label or b"",
            context=context or b"",
            fixed=fixed,
            break_location=break_location,
        )

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
        kdf = self._get_kdf(length, algorithm, rlen, llen, location, label, context, operation_mode, break_location, fixed)
        return (kdf.derive(message),)


class KBKDF_Verify(KBKDF_Derive):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verified_status",)

    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        class_input["required"]["expected_key"] = (
            "BYTESLIKE",
            {
                "forceInput": True,
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
        kbkdf_key = self._get_kdf(length, algorithm, rlen, llen, location, label, context, operation_mode, break_location, fixed)
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
