from cryptography.hazmat.primitives import padding


class PaddingNode:
    CATEGORY = "Cryptography/Modern/Padding"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "padding_data": ("BYTESLIKE", {"forceInput": True, "tooltip": "The data to pad or unpad."}),
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
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("padded_data",)
    FUNCTION = "padding"

    def padding(self, padding_data: bytes, block_size, algorithm, mode):
        padding_algorithm = getattr(padding, algorithm)(block_size)

        if mode:
            padder = padding_algorithm.padder()
            padded_data = padder.update(padding_data)
            padded_data += padder.finalize()
            return (padded_data,)
        else:
            unpadder = padding_algorithm.unpadder()
            unpadded_data = unpadder.update(padding_data)
            unpadded_data += padder.finalize()
            return (unpadded_data,)


NODE_CLASS_MAPPINGS = {
    "Padding": PaddingNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Padding": "Symmetrical Padding",
}
