# RSA asymmetric encryption
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import serialization, hashes

# Simple init node to deduplicate some bits
class InitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Asymmetric"
    FUNCTION = "execute"

# Actual RSA functions
class RSAPrivateKeyFormat(InitNode):
    RETURN_TYPES = ("KEYOBJ", "BYTESLIKE", "NUMOBJ")
    RETURN_NAMES = ("key_object", "private_key", "private_numbers")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_exponent": ("INT", {
                    "min": 1,
                    "max": 4294967296,
                    "default": 65537,
                    }
                ),
                "key_size": ("INT", {"min": 512, "max": 8192, "step": 128, "default": 2048,}),
                "encoding": (
                    ["PEM", "DER"],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the private key.",
                    },
                ),
                "formatting": (
                    ["PKCS8", "OpenSSH", "TraditionalOpenSSL",],
                    {
                        "default": "PKCS8",
                        "description": "What format to serialize the key in. OpenSSH requires PEM encoding.",
                    },
                ),
                "encryption": (["Best Available", "None"], {"default": "Best Available"}),
            },
            "optional": {
                "encryption_password": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The password to use to encrypt the private key. Required if encryption is used.",
                    },
                ),
            },
        }

    def execute(self, public_exponent, key_size, encoding, formatting, encryption, encryption_password):
        private_key = rsa.generate_private_key(public_exponent=public_exponent, key_size=key_size)

        encoding = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PrivateFormat, formatting)

        match encryption:
            case "Best Available":
                enc_alg = serialization.BestAvailableEncryption(encryption_password.encode("utf-8"))
            case "None":
                enc_alg = serialization.NoEncryption()

        private_bytes = private_key.private_bytes(encoding=encoding, format=formatting, encryption_algorithm=enc_alg)
        return (private_key, private_bytes, private_key.private_numbers())

class RSAPublicKeyFormat(InitNode):
    RETURN_TYPES = ("KEYOBJ", "BYTESLIKE", "NUMOBJ")
    RETURN_NAMES = ("key_object", "public_key", "public_numbers")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_source": (
                    ["Fresh Key", "From Loaded Key"],
                    {
                        "tooltip": "The source of the private key to be used to sign the message",
                        "default": "Fresh Key",
                    },
                ),
                "encoding": (
                    [
                        "PEM",
                        "DER",
                    ],
                    {
                        "default": "PEM",
                        "description": "Encoding type for the public key.",
                    },
                ),
                "formatting": (
                    ["SubjectPublicKeyInfo", "PKCS1"],
                    {
                        "default": "SubjectPublicKeyInfo",
                        "description": "What format to serialize the key in.",
                    },
                ),
            },
            "optional": {
                "serialized_key": ("KEYOBJ",
                    {
                        "forceInput": True,
                        "tooltip": "Only applicable if key_source is `From Loaded Key`."
                    }
                ),
                "fresh_key_size": ("INT",
                    {
                        "min": 512,
                        "max": 8192,
                        "step": 128,
                        "default": 2048,
                        "tooltip": "Only applicable if key_source is `From Fresh Key`."
                    }
                ),
                "public_exponent": ("INT",
                    {
                        "min": 1,
                        "max": 4294967296,
                        "default": 65537,
                        "tooltip": "Only applicable if key_sourcce if `From Fresh Key`."
                    }
                ),
            },
        }

    def execute(self, key_source, encoding, formatting, serialized_key:rsa.RSAPrivateKey | None, fresh_key_size, public_exponent):
        match key_source:
            case "Fresh Key":
                p_key = rsa.generate_private_key(public_exponent, fresh_key_size)
            case "From Loaded Key":
                if isinstance(serialized_key, rsa.RSAPrivateKey):
                    p_key = serialized_key
                else:
                    raise ValueError("Missing private keys for RSA public key generation.")
        public_key = p_key.public_key()

        encoding = getattr(serialization.Encoding, encoding)
        formatting = getattr(serialization.PublicFormat, formatting)

        public_bytes = public_key.public_bytes(encoding=encoding, format=formatting)
        return (public_key, public_bytes, public_key.public_numbers())

# RSA signing and verifying of signatures
class RSASign(InitNode):
    RETURN_TYPES = ("SIGNATURE",)
    RETURN_NAMES = ("signature",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "private_key": ("KEYOBJ", {"forceInput": True,}),
                "data": ("BYTESLIKE", {"forceInput": True}),
                "salt_length": (
                    ["Max Length", "Digest Length", "Manual"], {"default": "Max Length", "tooltip": "The length of the salt."}
                ),
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
                "padding_alg": (["PSS", "PKCS1v15"], {"default": "PSS"})
            },
            "optional": {
                "prehashed": ("BOOLEAN", {"tooltip": "Whether the data is prehashed or not."}),
                "salt_length_manual": ("INT", {"min": 1, "max": 65536, "step": 1, "tooltip": "For only when salt_length is `Manual`."})
            },
        }

    def execute(self, private_key, data, salt_length, salt_length_manual, signature_algorithm, padding_alg, prehashed):
        algorithm = getattr(hashes, signature_algorithm)()
        if padding_alg == "PSS":
            match salt_length:
                case "Max Length":
                    salt_length = padding.PSS.MAX_LENGTH
                case "Digest Length":
                    salt_length = padding.PSS.DIGEST_LENGTH
                case "Manual":
                    salt_length = salt_length_manual
            padder = padding.PSS(mgf=padding.MGF1(algorithm),salt_length=salt_length)
        if padding_alg == "PSS" and not prehashed:
            signature = private_key.sign(data, padder, algorithm)
        elif padding_alg == "PSS" and prehashed:
            signature = private_key.sign(data, padder, utils.Prehashed(algorithm))
        elif padding_alg == "PKCS1v15" and not prehashed:
            signature = private_key.sign(data, padding.PKCS1v15(), algorithm)
        elif padding_alg == "PKCS1v15" and prehashed:
            signature = private_key.sign(data, padding.PKCS1v15(), utils.Prehashed(algorithm))
        return (signature,)

class RSAVerify(InitNode):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("verify_result",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_key": ("KEYOBJ", {"forceInput": True,}),
                "data": ("BYTESLIKE", {"forceInput": True,}),
                "signature": ("SIGNATURE", {"forceInput": True,}),
                "salt_length": (
                    ["Max Length", "Digest Length", "Manual"], {"default": "Max Length", "tooltip": "The length of the salt."}
                ),
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
                "padding_alg": (["PSS", "PKCS1v15"], {"default": "PSS"})
            },
            "optional": {
                "prehashed": ("BOOLEAN", {"tooltip": "Whether the data is prehashed or not."}),
                "salt_length_manual": ("INT", {"min": 1, "max": 65536, "step": 1, "tooltip": "For only when salt_length is `Manual`."})
            },
        }

    def execute(self, public_key, data, signature, salt_length, salt_length_manual, signature_algorithm, padding_alg, prehashed):
        algorithm = getattr(hashes, signature_algorithm)()
        from cryptography.exceptions import InvalidSignature
        if padding_alg == "PSS":
            match salt_length:
                case "Max Length":
                    salt_length = padding.PSS.MAX_LENGTH
                case "Digest Length":
                    salt_length = padding.PSS.DIGEST_LENGTH
                case "Manual":
                    salt_length = salt_length_manual
            padder = padding.PSS(mgf=padding.MGF1(algorithm),salt_length=salt_length)
        if padding_alg == "PSS" and not prehashed:
            try:
                public_key.verify(signature, data, padder, algorithm)
                verify_result = True
            except InvalidSignature:
                verify_result = False
        elif padding_alg == "PSS" and prehashed:
            try:
                public_key.verify(signature, data, padder, utils.Prehashed(algorithm))
                verify_result = True
            except InvalidSignature:
                verify_result = False
        elif padding_alg == "PKCS1v15" and not prehashed:
            try:
                public_key.verify(signature, data, padding.PKCS1v15(), algorithm)
                verify_result = True
            except InvalidSignature:
                verify_result = False
        elif padding_alg == "PKCS1v15" and prehashed:
            try:
                public_key.verify(signature, data, padding.PKCS1v15(), utils.Prehashed(algorithm))
                verify_result = True
            except InvalidSignature:
                verify_result = False
        return (verify_result,)

# RSA encryption and decryption
class RSAEncrypt(InitNode):
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("encrypted_data",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_key": ("KEYOBJ", {"forceInput": True,}),
                "data": ("BYTESLIKE", {"forceInput": True,}),
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
                "padding_alg": (["OAEP", "PKCS1v15"], {"default": "OAEP"})
            },
            "optional": {
                "label": ("BYTESLIKE", {"forceInput": True}),
            },
        }

    def execute(self, public_key: rsa.RSAPublicKey, data, signature_algorithm, padding_alg, label = None):
        algorithm = getattr(hashes, signature_algorithm)()
        if padding_alg == "OAEP":
            encrypted_data = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm), algorithm=algorithm, label=label))
        elif padding_alg == "PKCS1v15":
            encrypted_data = public_key.encrypt(data, padding.PKCS1v15())
        return (encrypted_data,)

class RSADecrypt(InitNode):
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("decrypted_data",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "private_key": ("KEYOBJ", {"forceInput": True,}),
                "data": ("BYTESLIKE", {"forceInput": True,}),
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
                "padding_alg": (["OAEP", "PKCS1v15"], {"default": "OAEP"})
            },
            "optional": {
                "label": ("BYTESLIKE", {"forceInput": True}),
            },
        }

    def execute(self, private_key: rsa.RSAPrivateKey, data, signature_algorithm, padding_alg, label = None):
        algorithm = getattr(hashes, signature_algorithm)()
        if padding_alg == "OAEP":
            decrypted_data = private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm), algorithm=algorithm, label=label))
        elif padding_alg == "PKCS1v15":
            decrypted_data = private_key.decrypt(data, padding.PKCS1v15())
        return (decrypted_data,)

# RSA numbers, for when standard serialized key loading fails
class RSAPublicNumbersFormat(InitNode):
    RETURN_TYPES = ("KEYOBJ", "NUMOBJ",)
    RETURN_NAMES = ("public_key", "public_numbers")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_modulus": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 3, "tooltip": "The public modulus (n)."}),
                "public_exponent": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 65537, "tooltip": "The public exponent (e)."}),
            },
        }

    def execute(self, public_modulus, public_exponent):
        pub_num = rsa.RSAPublicNumbers(n=public_modulus, e=public_exponent)
        return (pub_num.public_key(), pub_num)

class RSAPubNumValue(InitNode):
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("public_modulus", "public_exponent")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "public_numbers": ("NUMOBJ", {"forceInput": True}),
                "public_key": ("KEYOBJ", {"forceInput": True}),
            },
        }

    def execute(self, public_numbers: rsa.RSAPublicNumbers | None, public_key: rsa.RSAPublicKey | None):
        if public_numbers == None and public_key != None:
            pnum = public_key.public_numbers()
        elif public_numbers != None and public_key == None:
            pnum = public_numbers
        else:
            raise ValueError("Invalid configuration given. Input either the public numbers object or public key object only.")
        return (pnum.n, pnum.e,)

class RSAPrivateNumbersFormat(InitNode):
    RETURN_TYPES = ("KEYOBJ", "NUMOBJ",)
    RETURN_NAMES = ("public_key", "private_numbers",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_numbers": ("NUMOBJ", {"forceInput": True, "tooltip": "As a requirement to generate one of these keys, you need the public numbers generated from that key as well."}),
                "var_p": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "One of the two primes composing the private modulus `n`"}),
                "var_q": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "One of the two primes composing the private modulus `n`"}),
                "private_exponent": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 65537, "tooltip": "The private exponent (d)."}),
                "skip_rsa_key_validation": ("BOOLEAN", {"default": False, "tooltip": "Unless you know what you're doing, do not change this. Disabling RSA key validation speeds up key loading, but is **unsafe** and may cause OpenSSL to misbehave or crash, potentially dragging ComfyUI down with it."})
            },
        }

    def execute(self, public_numbers, var_p, var_q, private_exponent, skip_rsa_key_validation):
        pvn_iqmp = rsa.rsa_crt_iqmp(var_p, var_q)
        pvn_dmp1 = rsa.rsa_crt_dmp1(private_exponent, var_p)
        pvn_dmq1 = rsa.rsa_crt_dmq1(private_exponent, var_q)
        private_num = rsa.RSAPrivateNumbers(p=var_p, q=var_q, d=private_exponent, dmp1=pvn_dmp1, dmq1=pvn_dmq1, iqmp=pvn_iqmp, public_numbers=public_numbers)
        private_key = private_num.private_key(unsafe_skip_rsa_key_validation=skip_rsa_key_validation)
        return (private_num, private_key,)

class RSAPrivNumValue(InitNode):
    RETURN_TYPES = ("NUMOBJ", "INT", "INT", "INT", "INT", "INT", "INT",)
    RETURN_NAMES = ("public_numbers", "var_p", "var_q", "private_exponent", "dmp1", "dmq1", "iqmp",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "private_numbers": ("NUMOBJ", {"forceInput": True}),
                "private_key": ("KEYOBJ", {"forceInput": True}),
            }
        }

    def execute(self, private_numbers: rsa.RSAPrivateNumbers | None, private_key: rsa.RSAPrivateKey | None):
        if private_numbers == None and private_key != None:
            pnum = private_key.private_numbers()
        elif private_numbers != None and private_key == None:
            pnum = private_numbers
        else:
            raise ValueError("Invalid configuration given. Input either the private numbers object or private key object only.")
        return (pnum.public_numbers, pnum.p, pnum.q, pnum.d, pnum.dmp1, pnum.dmq1, pnum.iqmp,)

# Recovery nodes for partial numbers given

class RSARestoreD(InitNode):
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("d",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "public_exponent": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 65537, "tooltip": "The public exponent (e)."}),
                "var_p": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "One of the two primes composing the private modulus `n`"}),
                "var_q": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "One of the two primes composing the private modulus `n`"}),
            }
        }

    def execute(self, public_exponent, var_p, var_q):
        return (rsa.rsa_recover_private_exponent(public_exponent, var_p, var_q),)

class RSARestorePrime(InitNode):
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("p", "q")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "private_modulus": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 65537, "tooltip": "The private modulus (n)."}),
                "public_exponent": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "The public exponent (e)"}),
                "private_exponent": ("INT", {"min": 1, "max": 4294967296, "step": 1, "default": 1, "tooltip": "The private exponent (d)"}),
            }
        }

    def execute(self, private_modulus, public_exponent, private_exponent):
        return rsa.rsa_recover_prime_factors(private_modulus, public_exponent, private_exponent)

NODE_CLASS_MAPPINGS = {
    "RSAPrivateKeyFormat": RSAPrivateKeyFormat,
    "RSAPublicKeyFormat": RSAPublicKeyFormat,
    "RSASign": RSASign,
    "RSAVerify": RSAVerify,
    "RSAEncrypt": RSAEncrypt,
    "RSADecrypt": RSADecrypt,
    "RSAPublicNumbersFormat": RSAPublicNumbersFormat,
    "RSAPubNumValue": RSAPubNumValue,
    "RSAPrivateNumbersFormat": RSAPrivateNumbersFormat,
    "RSAPrivNumValue": RSAPrivNumValue,
    "RSARestoreD": RSARestoreD,
    "RSARestorePrime": RSARestorePrime,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RSAPrivateKeyFormat": "RSA Private Key Bytes",
    "RSAPublicKeyFormat": "RSA Public Key Bytes",
    "RSASign": "RSA Signature Signer",
    "RSAVerify": "RSA Signature Verification",
    "RSAEncrypt": "RSA Encrypt Data",
    "RSADecrypt": "RSA Decrypt Data",
    "RSAPublicNumbersFormat": "RSA Public Numbers into Key",
    "RSAPubNumValue": "RSA Public Numbers Values",
    "RSAPrivateNumbersFormat": "RSA Private Numbers into Key",
    "RSAPrivNumValue": "RSA Private Numbers Values",
    "RSARestoreD": "RSA Restore Private Exponent",
    "RSARestorePrime": "RSA Restore Prime Factors",
}
