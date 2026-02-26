from reedsolo import RSCodec


class InitNode:
    def __init__(self):
        pass

    CATEGORY = "Utilities/Error Correction"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("BYTESLIKE", {"tooltip": "The data to run through the error-correction algorithm."}),
                "ecc_symbols": (
                    "INT",
                    {"min": 10, "step": 2, "tooltip": "The amount of error-correction symbols to insert into the data."},
                ),
            },
            "optional": {},
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()


class ReedSolomonEncode(InitNode):
    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("encoded_data",)

    def reedsolomonencode(self, data, ecc_symbols):
        rsc = RSCodec(ecc_symbols)
        output = rsc.encode(data)
        return (output,)


class ReedSolomonDecode(InitNode):
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "decoded_msg",
        "msg_with_code",
        "errata_pos_list",
    )

    @classmethod
    def INPUT_TYPES(cls):
        class_method = super().INPUT_TYPES()
        class_method["optional"]["erase_pos"] = (
            "STRING",
            {
                "default": "",
                "multiline": False,
                "tooltip": "If you know the exact positions of the errors, type them here in a comma-separated list.",
            },
        )

    def reedsolomondecode(self, data, ecc_symbols, erase_pos=None):
        rsc = RSCodec(ecc_symbols)
        if erase_pos != "":
            msg, coded_msg, pos_list = rsc.decode(data, erase_pos=erase_pos)
        else:
            msg, coded_msg, pos_list = rsc.decode(data)
        return (
            msg,
            coded_msg,
            pos_list,
        )


NODE_CLASS_MAPPINGS = {
    "ReedSolomonEncode": ReedSolomonEncode,
    "ReedSolomonDecode": ReedSolomonDecode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ReedSolomonEncode": "Reed-Solomon Encode",
    "ReedSolomonDecode": "Reed-Solomon Decode",
}
