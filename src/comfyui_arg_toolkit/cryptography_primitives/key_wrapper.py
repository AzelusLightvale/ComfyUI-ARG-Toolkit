from cryptography.hazmat.primitives import keywrap

# To save my sanity (and because ComfyUI does not support it as a type), all byte array objects are converted to hexadecimal. Do not expect to directly manipulate byte arrays here. This comment will be on top of every Python file that directly interfaces with byte arrays.


class WrapKeyNodes:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Key Wrap"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wrapping_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The wrapping key, in hexadecimal.",
                    },
                ),
                "secondary_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The secondary key, in hexadecimal. For wrapping, this is the key to wrap. For decoding, this is the wrapped key.",
                    },
                ),
                "mode": (
                    "BOOLEAN",
                    {
                        "label_on": "Wrap",
                        "label_off": "Unwrap",
                        "tooltip": "Toggle between wrapping and unwrapping.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wrapped_key",)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


class AESKeyWrap(WrapKeyNodes):
    def aeskeywrap(self, wrapping_key, secondary_key, mode):
        wrapping_key_bytes = bytes.fromhex(wrapping_key)
        secondary_key_bytes = bytes.fromhex(secondary_key)

        if mode:  # Wrap
            wrapped_key = keywrap.aes_key_wrap(wrapping_key_bytes, secondary_key_bytes)
            return (wrapped_key.hex(),)
        else:  # Unwrap
            unwrapped_key = keywrap.aes_key_unwrap(wrapping_key_bytes, secondary_key_bytes)
            return (unwrapped_key.hex(),)


class AESKeyWrapWithPadding(WrapKeyNodes):
    def aeskeywrapwithpadding(self, wrapping_key, secondary_key, mode):
        wrapping_key_bytes = bytes.fromhex(wrapping_key)
        secondary_key_bytes = bytes.fromhex(secondary_key)

        if mode:  # Wrap
            wrapped_key = keywrap.aes_key_wrap_with_padding(wrapping_key_bytes, secondary_key_bytes)
            return (wrapped_key.hex(),)
        else:  # Unwrap
            unwrapped_key = keywrap.aes_key_unwrap_with_padding(wrapping_key_bytes, secondary_key_bytes)
            return (unwrapped_key.hex(),)


NODE_CLASS_MAPPINGS = {
    "AESKeyWrap": AESKeyWrap,
    "AESKeyWrapWithPadding": AESKeyWrapWithPadding,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AESKeyWrap": "AES Key Wrap",
    "AESKeyWrapWithPadding": "AES Key Wrap With Padding",
}
