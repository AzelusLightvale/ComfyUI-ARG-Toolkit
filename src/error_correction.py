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
        return (bytes(output),)


class ReedSolomonDecode(InitNode):
    RETURN_TYPES = (
        "BYTESLIKE",
        "BYTESLIKE",
        "BYTESLIKE",
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
        return class_method

    def reedsolomondecode(self, data, ecc_symbols, erase_pos=""):
        rsc = RSCodec(ecc_symbols)
        parsed_erase_pos = None
        if erase_pos:
            try:
                parsed_erase_pos = [int(p.strip()) for p in erase_pos.split(",")]
            except ValueError:
                raise ValueError("Invalid format for erase_pos. It should be a comma-separated list of integers.")
        msg, coded_msg, pos_list = rsc.decode(data, erase_pos=parsed_erase_pos)
        return (
            bytes(msg),
            bytes(coded_msg),
            bytes(pos_list),
        )


NODE_CLASS_MAPPINGS = {
    "ReedSolomonEncode": ReedSolomonEncode,
    "ReedSolomonDecode": ReedSolomonDecode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ReedSolomonEncode": "Reed-Solomon Encode",
    "ReedSolomonDecode": "Reed-Solomon Decode",
}
