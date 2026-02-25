from cryptography import fernet


class FernetSimple:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern"

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
                        "tooltip": "Input encryption key here. Has to be 32 bytes in size.",
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
    FUNCTION = "FernetSimple"

    def FernetSimple(self, text, key, mode):
        cipher = fernet.Fernet(key)
        bytetext = text.encode("utf-8")
        if mode:
            token = cipher.encrypt(bytetext)
        else:
            token = cipher.decrypt(bytetext)
        encrypted_message = token.decode("utf-8")
        return (encrypted_message,)


class FernetKeygenSimple:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("key",)
    FUNCTION = "FernetKeygenSimple"

    def FernetKeygenSimple(self):
        key = fernet.Fernet.generate_key()
        return (key.decode,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "FernetSimple": FernetSimple,
    "FernetKeygenSimple": FernetKeygenSimple,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FernetSimple": "Fernet Symmetric Key Encryption",
    "FernetKeygenSimple": "Fernet Key Generator",
}
