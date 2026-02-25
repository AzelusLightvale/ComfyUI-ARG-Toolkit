from cryptography.hazmat.primitives.ciphers import aead
import base64

# As of 2.0.0, all byte-like objects now have their own types. To actually input new data, new Byte-to-Format and Format-to-Byte nodes have been created to deal with that demand.


class ChaCha20Poly1305:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Authenticated"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here... (if message is a bytes-like object, convert to base64 first)",
                    },
                ),
                "key": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "Input encryption key here. Has to be in bytes format for this node.",
                    },
                ),
                "nonce": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "A random value to use. Should be 12 bytes in size.",
                    },
                ),
                "associated_data": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "Additional data that should be authenticated with the key, but does not need to be encrypted. Can be None",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "encrypt",
                        "label_off": "decrypt",
                        "tooltip": "Toggle between encrypting or decrypting a message.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("encrypted_txt",)
    FUNCTION = "cc20"

    def cc20(self, text, key: bytes, nonce: bytes, associated_data: bytes, mode):
        cipher = aead.ChaCha20Poly1305(key)
        if mode:
            bytetext = text.encode("utf-8")
            token = cipher.encrypt(nonce, bytetext, associated_data)
            encrypted_message = token.hex()
        else:
            bytetext = base64.b64decode(text, "utf-8")
            token = cipher.decrypt(nonce, bytetext, associated_data)
            encrypted_message = token.decode("utf-8")
        return (encrypted_message,)


class ChaCha20Poly1305Keygen:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Authenticated"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("key",)
    FUNCTION = "cc20_key"

    def cc20_key(self):
        key = aead.ChaCha20Poly1305.generate_key()
        return (key.base64.b64encode(),)


class AESAuth:  # Since all AES-based authenticated encryption techniques are the same, this one node concatenates all of them together into the same node to save on processing.
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Authenticated"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                    },
                ),
                "key": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "Input encryption key here. Has to be in a bytes-like format.",
                    },
                ),
                "nonce": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "A random value to use. Should be 12 bytes in size.",
                    },
                ),
                "associated_data": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "Additional data that should be authenticated with the key, but does not need to be encrypted. Can be None",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "encrypt",
                        "label_off": "decrypt",
                        "tooltip": "Toggle between encrypting or decrypting a message.",
                    },
                ),
                "aes_type": (
                    ["AES-GCM", "AES-GCM-SIV", "AES-OCB3", "AES-SIV", "AES-CCM"],
                    {
                        "tooltip": "Switches between different authenticated encryption form.",
                    },
                ),
            },
            "optional": {
                "ccm_tag_length": (
                    "INT",
                    {
                        "default": 16,
                        "min": 4,
                        "max": 16,
                        "step": 2,
                        "tooltip": "For AES-CCM specifically, it allows a tag length to be specified. Normally, this defaults to 16, but can be lowered to 4. Unless you know what you're doing, DO NOT CHANGE FROM THE DEFAULTS.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("encrypted_txt",)
    FUNCTION = "aesauth"

    def aesauth(self, text, key: bytes, nonce, associated_data, mode, aes_type, ccm_tag_length):
        cipher_engines = {
            "AES-GCM": aead.AESGCM,
            "AES-GCM-SIV": aead.AESGCMSIV,
            "AES-OCB3": aead.AESOCB3,
        }
        if aes_type == "AES-SIV":
            cipher = aead.AESSIV(key)
            associated_data = [associated_data, nonce]
        elif aes_type == "AES-CCM":
            cipher = aead.AESCCM(key, ccm_tag_length)
        elif aes_type in cipher_engines:
            cipher = cipher_engines[aes_type](key)
        else:
            raise ValueError("Invalid AES type chosen. Perhaps the node is broken? Try making a new one, as this is normally impossible.")
        if mode:
            bytetext = text.encode("utf-8")
            if aes_type == "AES-SIV":
                token = cipher.encrypt(bytetext, associated_data)
            else:
                token = cipher.encrypt(nonce, bytetext, associated_data)
            encrypted_message = base64.b64encode(token).decode("utf-8")
        else:
            bytetext = base64.b64decode(text, "utf-8")
            if aes_type == "AES-SIV":
                token = cipher.decrypt(bytetext, associated_data)
            else:
                token = cipher.decrypt(nonce, bytetext, associated_data)
            encrypted_message = token.decode("utf-8")
        return (encrypted_message,)


class AESAuthKeygen:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Authenticated"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bit_length": (
                    ["128", "192", "256"],
                    {
                        "tooltip": "The amount of bits needed to generate a key. For AES-SIV specifically, the bit_length is the equivalent to its standard AES key, as AES-SIV generates both an encryption and MAC key in its process.",
                    },
                ),
                "aes_type": (
                    ["AES-GCM", "AES-GCM-SIV", "AES-OCB3", "AES-SIV", "AES-CCM"],
                    {
                        "tooltip": "Switches between different authenticated encryption form.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("key",)
    FUNCTION = "aes_keygen"

    def aes_keygen(self, bit_length, aes_type):
        bit_length = int(bit_length)
        generators = {
            "AES-GCM": aead.AESGCM,
            "AES-GCM-SIV": aead.AESGCMSIV,
            "AES-OCB3": aead.AESOCB3,
            "AES-CCM": aead.AESCCM,
        }
        if aes_type == "AES-SIV":
            key = aead.AESGCMSIV.generate_key(bit_length * 2)
        elif aes_type in generators:
            key = generators[aes_type].generate_key(bit_length)
        else:
            raise ValueError(
                f"Invalid AES type chosen. Perhaps the node is broken? Try making a new one, as this is normally impossible. Currently, it's {aes_type}, which is wrong."
            )
        return (base64.b64encode(key),)


NODE_CLASS_MAPPINGS = {
    "ChaCha20Poly1305": ChaCha20Poly1305,
    "ChaCha20Poly1305Keygen": ChaCha20Poly1305Keygen,
    "AESAuthenticated": AESAuth,
    "AESAuthenticatedKeygen": AESAuthKeygen,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChaCha20Poly1305": "ChaCha20Poly1305 Encryption",
    "ChaCha20Poly1305Keygen": "ChaCha20Poly1305 Key Generator",
    "AESAuthenticated": "AES-based Authenticated Encryption",
    "AESAuthenticatedKeygen": "AES-based Authenticated Key Generator",
}
