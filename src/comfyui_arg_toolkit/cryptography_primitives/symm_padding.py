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
        if mode:
            padder = padder.padder()
            padded_data = padder.update(padding_data.encode("utf-8"))
            padded_data += padder.finalize()
            return (padded_data.hex(),)
        else:
            padder = padder.unpadder()
            unpadded_data = padder.update(bytes.fromhex(padding_data))
            unpadded_data += padder.finalize()
            return (unpadded_data.decode("utf-8"),)


NODE_CLASS_MAPPINGS = {
    "Padding": PaddingNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Padding": "Symmetrical Padding",
}
