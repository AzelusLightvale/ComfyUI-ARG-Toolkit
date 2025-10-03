from cryptography.hazmat.primitives import padding


class PaddingNode:
    CATEGORY = "Cryptography/Modern/Padding"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "padding_data": ("STRING", {"default": "Hello World", "multiline": False, "tooltip": "The data to pad."}),
                "block_size": (
                    "INT",
                    {
                        "default": 128,
                        "step": 8,
                        "min": 0,
                        "max": 2040,
                        "tooltip": "The size of the block (in bits) that is padded onto the data.",
                    },
                ),
                "algorithm": (["PKCS7", "ANSIX923"], {"tooltip": "The padding algorithm used."}),
                "mode": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "Pad",
                        "label_off": "Unpad",
                        "tooltip": "Toggle between padding and unpadding.",
                    },
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("padded_data",)
    FUNCTION = "padding"

    def padding(self, padding_data, block_size, algorithm, mode):
        padder = getattr(padding, algorithm)(block_size)

        def to_bytes(data):
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                # Try hex first
                try:
                    if all(c in "0123456789abcdefABCDEF" for c in data) and len(data) % 2 == 0:
                        return bytes.fromhex(data)
                except:
                    pass
                # Try base64
                try:
                    import base64

                    if all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in data):
                        return base64.b64decode(data)
                except:
                    pass
                # Otherwise treat as string
                return data.encode("utf-8")
            else:
                raise ValueError(f"Unsupported data type: {type(data)}")

        # Always return hex for crypto operations
        def to_hex(data_bytes):
            return (data_bytes.hex(),)

        if mode:
            data_bytes = to_bytes(padding_data)
            padder = padder.padder()
            padded_data = padder.update(data_bytes)
            padded_data += padder.finalize()
            return to_hex(padded_data)
        else:
            data_bytes = to_bytes(padding_data)
            padder = padder.unpadder()
            unpadded_data = padder.update(data_bytes)
            unpadded_data += padder.finalize()

            # For unpadding, try to return string if it's valid text, otherwise hex
            try:
                decoded = unpadded_data.decode("utf-8")
                return (decoded,)
            except UnicodeDecodeError:
                return to_hex(unpadded_data)


NODE_CLASS_MAPPINGS = {
    "Padding": PaddingNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Padding": "Symmetrical Padding",
}
