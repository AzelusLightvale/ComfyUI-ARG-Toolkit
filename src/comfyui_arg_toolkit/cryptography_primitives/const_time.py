from cryptography.hazmat.primitives import constant_time


class ConstantTimeCompare:
    CATEGORY = "Cryptography/Modern/Constant Time"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The first string to compare (in hexadecimal).",
                    },
                ),
                "b": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "The second string to compare (in hexadecimal).",
                    },
                ),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_equal",)
    FUNCTION = "compare"

    def compare(self, a, b):
        a_bytes = bytes.fromhex(a)
        b_bytes = bytes.fromhex(b)
        result = constant_time.bytes_eq(a_bytes, b_bytes)
        return (result,)


NODE_CLASS_MAPPINGS = {
    "ConstantTimeCompare": ConstantTimeCompare,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConstantTimeCompare": "Constant Time Compare",
}
