class BooleanOutputter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": False}),
                "true_text": ("STRING", {"default": "True", "multiline": False, "tooltip": "String returned when input boolean is true."}),
                "false_text": (
                    "STRING",
                    {"default": "False", "multiline": False, "tooltip": "String returned when input boolean is false."},
                ),
            }
        }

    CATEGORY = "Debugging"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "bool_check"

    def bool_check(self, boolean, true_text, false_text):
        if boolean:
            return (true_text,)
        elif not boolean:
            return (false_text,)
        else:
            raise ValueError(
                "How did this even happen? Unless Python or ComfyUI does not handle booleans properly, *this should never happen*. If this does happen, please report this as a bug immediately."
            )


NODE_CLASS_MAPPINGS = {
    "BooleanOutputter": BooleanOutputter,
}
NODE_DISPLAY_NAME_MAPPINGS = {"BooleanOutputter": "Boolean Outputter"}
