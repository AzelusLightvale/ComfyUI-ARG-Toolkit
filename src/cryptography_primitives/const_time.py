from cryptography.hazmat.primitives import constant_time


class ConstantTimeCompare:
    CATEGORY = "ARG Toolkit/Cryptography/Modern/Constant Time"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The first byte-object to compare.",
                    },
                ),
                "b": (
                    "BYTESLIKE",
                    {
                        "forceInput": True,
                        "tooltip": "The second byte-object to compare.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_equal",)
    FUNCTION = "compare"

    def compare(self, a, b):
        result = constant_time.bytes_eq(a, b)
        return (result,)


NODE_CLASS_MAPPINGS = {
    "ConstantTimeCompare": ConstantTimeCompare,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConstantTimeCompare": "Constant Time Compare",
}
