from cryptography.hazmat.primitives import keywrap

# As of 2.0.0, all byte-like objects now have their own types. To actually input new data, new Byte-to-Format and Format-to-Byte nodes have been created to deal with that demand.


class WrapKeyNodes:
    def __init__(self):
        pass

    CATEGORY = "Cryptography/Modern/Key Wrap"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wrapping_key": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The wrapping key.",
                    },
                ),
                "secondary_key": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "For wrapping, this is the key to wrap. For unwrapping, this is the wrapped key.",
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

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("wrapped_key",)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


class AESKeyWrap(WrapKeyNodes):
    def aeskeywrap(self, wrapping_key: bytes, secondary_key: bytes, mode):
        if mode:  # Wrap
            wrapped_key = keywrap.aes_key_wrap(wrapping_key, secondary_key)
            return (wrapped_key,)
        else:  # Unwrap
            unwrapped_key = keywrap.aes_key_unwrap(wrapping_key, secondary_key)
            return (unwrapped_key,)


class AESKeyWrapWithPadding(WrapKeyNodes):
    def aeskeywrapwithpadding(self, wrapping_key: bytes, secondary_key: bytes, mode):
        if mode:  # Wrap
            wrapped_key = keywrap.aes_key_wrap_with_padding(wrapping_key, secondary_key)
            return (wrapped_key,)
        else:  # Unwrap
            unwrapped_key = keywrap.aes_key_unwrap_with_padding(wrapping_key, secondary_key)
            return (unwrapped_key,)


NODE_CLASS_MAPPINGS = {
    "AESKeyWrap": AESKeyWrap,
    "AESKeyWrapWithPadding": AESKeyWrapWithPadding,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AESKeyWrap": "AES Key Wrap",
    "AESKeyWrapWithPadding": "AES Key Wrap With Padding",
}
