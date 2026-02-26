import os
import base64
import binascii
import ast

# To save my sanity, all byte array objects are converted to hexadecimal. Do not expect to directly manipulate byte arrays here. This comment will be on top of every Python file that directly interfaces with byte arrays.


class SystemRandom:
    def __init__(self):
        pass

    CATEGORY = "Utilities/Random"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "byte_num": (
                    "INT",
                    {
                        "default": 12,
                        "min": 1,
                        "step": 1,
                    },
                ),
            }
        }

    RETURN_TYPES = ("BYTESLIKE",)
    RETURN_NAMES = ("rand_value",)
    FUNCTION = "SystemRandom"

    def SystemRandom(self, byte_num):
        return (os.urandom(byte_num),)


# The converter category of Utilities


class ConverterNodes:
    def __init__(self):
        pass

    CATEGORY = "Utilities/Converter"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                    },
                ),
                "encoding_format": (
                    [
                        "utf-8",
                        "utf-16",
                        "utf-32",
                        "ascii",
                        "latin-1",
                        "cp1252",
                        "utf-8-sig",
                        "Other",
                    ],
                    {
                        "tooltip": "The encoding format available for text, may yield different results when converting.",
                    },
                ),
            },
            "optional": {
                "other_encoding_format": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": 'If, for some reason, your chosen encoding format is not available in the dropdown, select "Other" in encoding_format and type in your encoding format here. Supports all format written in Python\'s `encoding` module.',
                    },
                )
            },
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("converted_txt",)

    def encoding_selector(self, encoding_format, other_encoding_format):
        if encoding_format == "Other":
            encoding_format = other_encoding_format
        return encoding_format


class String2Binary(ConverterNodes):
    def string2binary(self, text, encoding_format, other_encoding_format):
        return (" ".join(format(c, "08b") for c in bytearray(text, self.encoding_selector(encoding_format, other_encoding_format))),)


class Binary2String(ConverterNodes):
    def binary2string(self, text, encoding_format, other_encoding_format):
        cleaned = text.replace(" ", "").replace("\n", "")
        if len(cleaned) % 8 != 0:
            raise ValueError("Binary string length must be a multiple of 8")
        if any(c not in "01" for c in cleaned):
            raise ValueError("Binary input must contain only 0 and 1")
        byte_data = bytes(int(cleaned[i : i + 8], 2) for i in range(0, len(cleaned), 8))
        return (byte_data.decode(self.encoding_selector(encoding_format, other_encoding_format)),)


class String2Hex(ConverterNodes):
    def string2hex(self, text, encoding_format, other_encoding_format):
        return (text.encode(self.encoding_selector(encoding_format, other_encoding_format)).hex(),)


class Hex2String(ConverterNodes):
    def hex2string(self, text, encoding_format, other_encoding_format):
        return (
            bytes.fromhex(text.replace("0x", "").replace(" ", "")).decode(self.encoding_selector(encoding_format, other_encoding_format)),
        )


class String2Base64(ConverterNodes):
    def string2base64(self, text, encoding_format, other_encoding_format):
        return (base64.b64encode(text.encode(self.encoding_selector(encoding_format, other_encoding_format))).decode("ascii"),)


class Base642String(ConverterNodes):
    def base642string(self, text, encoding_format, other_encoding_format):
        return (base64.b64decode(text.encode("ascii")).decode(self.encoding_selector(encoding_format, other_encoding_format)),)


# The Bitwise category of Utilities. Also has auto-detection for the sake of my sanity.


class BitwiseNodes:
    def __init__(self):
        pass

    CATEGORY = "Utilities/Bitwise"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_1": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                        "tooltip": "The main string to compare against. Accepts format defined in `datatype`",
                    },
                ),
                "text_2": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                        "tooltip": "The secondary string to compare against. Accepts format defined in `datatype`",
                    },
                ),
                "datatype": (["String", "Hexadecimal", "Base64", "Integer", "Binary"], {}),
                "encoding_format": (
                    [
                        "utf-8",
                        "utf-16",
                        "utf-32",
                        "ascii",
                        "latin-1",
                        "cp1252",
                        "utf-8-sig",
                        "Other",
                    ],
                    {
                        "tooltip": "The encoding format available for text, may yield different results when converting.",
                    },
                ),
            },
            "optional": {
                "other_encoding_format": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": 'If, for some reason, your chosen encoding format is not available in the dropdown, select "Other" in encoding_format and type in your encoding format here. Supports all format written in Python\'s `encoding` module.',
                    },
                )
            },
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-set FUNCTION to lowercase class name
        cls.FUNCTION = cls.__name__.lower()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("bitwise_txt",)

    def encoding_selector(self, encoding_format, other_encoding_format):
        if encoding_format == "Other":
            encoding_format = other_encoding_format
        return encoding_format

    def detect_and_parse(self, text, datatype, encoding_format, other_encoding_format=None):
        text = text.strip()

        if datatype == "Binary":
            cleaned = text[2:] if text.startswith("0b") else text
            cleaned = cleaned.zfill(((len(cleaned) + 7) // 8) * 8)
            return bytes(int(cleaned[i : i + 8], 2) for i in range(0, len(cleaned), 8)), "Binary"

        elif datatype == "Integer":
            val = int(text)
            length = max(1, (val.bit_length() + 7) // 8)
            return val.to_bytes(length, "big"), "Integer"

        elif datatype == "Hexadecimal":
            cleaned = text.replace("0x", "").replace(" ", "")
            if len(cleaned) % 2 != 0:
                cleaned = "0" + cleaned
            return bytes.fromhex(cleaned), "Hexadecimal"

        elif datatype == "Base64":
            return base64.b64decode(text), "Base64"

        elif datatype == "String":
            encoding = self.encoding_selector(encoding_format, other_encoding_format)
            return text.encode(encoding), "String"

        else:
            raise ValueError(f"Unsupported datatype: {datatype}")

    def operate(self, text_1, text_2, datatype, encoding_format, other_encoding_format=None, func=None):
        b1, return_fmt = self.detect_and_parse(
            text=text_1, datatype=datatype, encoding_format=encoding_format, other_encoding_format=other_encoding_format
        )

        if text_2 is not None:
            b2, _ = self.detect_and_parse(
                text=text_2, datatype=datatype, encoding_format=encoding_format, other_encoding_format=other_encoding_format
            )
            # Ensure same length for operations that need it
            if len(b1) != len(b2):
                raise ValueError("Inputs must be same length for bitwise operations")
            result = func(b1, b2)
        else:
            result = func(b1)

        return result, return_fmt

    def format_output(self, data, output_format, encoding_format, other_encoding_format=None):
        if output_format == "Binary":
            return " ".join(format(b, "08b") for b in data)
        elif output_format == "Hex":
            return data.hex()
        elif output_format == "Base64":
            return base64.b64encode(data).decode()
        elif output_format == "Int":
            return str(int.from_bytes(data, "big"))
        elif output_format == "String":
            return data.decode(self.encoding_selector(encoding_format, other_encoding_format))
        else:
            raise ValueError(f"Unknown output format {output_format}")


class BitwiseAND(BitwiseNodes):
    def bitwiseand(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x & y for x, y in zip(b1, b2)),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class BitwiseOR(BitwiseNodes):
    def bitwiseor(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x | y for x, y in zip(b1, b2)),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class BitwiseNOT(BitwiseNodes):
    @classmethod
    def INPUT_TYPES(cls):
        class_input = super().INPUT_TYPES()
        del class_input["required"]["text_2"]
        class_input["required"]["text"] = class_input["required"].pop("text_1")
        return class_input

    def bitwisenot(self, text, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text,
            None,
            encoding_format,
            other_encoding_format,
            func=lambda b1: bytes((~x & 0xFF) for x in b1),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class BitwiseXOR(BitwiseNodes):
    def bitwisexor(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2)),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class BitwiseLS(BitwiseNodes):
    def bitwisels(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x << y for x, y in zip(b1, b2)),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class BitwiseRS(BitwiseNodes):
    def bitwisers(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x >> y for x, y in zip(b1, b2)),
        )
        return (self.format_output(result_bytes, input_format, encoding_format, other_encoding_format),)


class StringLooper:
    CATEGORY = "Utilities/Padding"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                    },
                ),
                "loops": (
                    "INT",
                    {
                        "min": 1,
                        "step": 1,
                        "default": 3,
                        "tooltip": "The number of times to repeat the string given",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("looped_text",)
    FUNCTION = "Looper"

    def Looper(self, text=str, loops=int):
        return (text * (loops + 1),)


class ByteslikeEncode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "Hello World!", "placeholder": "Type your message here..."}),
                "encoding": (["Hexadecimal", "Base64", "UTF-8", "Binary", "Raw Bytes"],),
            }
        }

    RETURN_TYPES = ("BYTESLIKE",)
    FUNCTION = "execute"
    CATEGORY = "Utilities/Converters"

    def execute(self, text, encoding):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        if encoding == "Hexadecimal":
            cleaned = text.strip().replace(" ", "").replace("\n", "")
            if len(cleaned) % 2 != 0:
                raise ValueError("Hex input must have even length.")
            try:
                data = bytes.fromhex(cleaned)
            except ValueError:
                raise ValueError("Invalid hex input.")
        elif encoding == "Base64":
            cleaned = text.strip()
            try:
                data = base64.b64decode(cleaned, validate=True)
            except binascii.Error:
                raise ValueError("Invalid base64 input.")
        elif encoding == "Binary":
            cleaned = text.replace(" ", "").replace("\n", "")
            if len(cleaned) % 8 != 0:
                raise ValueError("Binary length must be multiple of 8.")
            if any(c not in "01" for c in cleaned):
                raise ValueError("Binary input must contain only 0 and 1.")
            data = bytes(int(cleaned[i : i + 8], 2) for i in range(0, len(cleaned), 8))
        elif encoding == "UTF-8":
            try:
                data = text.encode("utf-8")
            except UnicodeEncodeError:
                raise ValueError("UTF-8 encoding failed.")
        elif encoding == "Raw Bytes":
            data = ast.literal_eval(f"b{data!r}" if not data.startswith(("'", '"')) else f"b{data}")
        else:
            raise ValueError("Unsupported mode")
        return (data,)


class ByteslikeDecode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"data": ("BYTESLIKE",), "encoding": (["Hexadecimal", "Base64", "UTF-8", "Binary", "Raw Bytes"],)}}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "Utilities/Converters"

    def execute(self, data, encoding):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Expected bytes-like objects. Got a different datatype from `BYTESLIKE`")
        if encoding == "Hexadecimal":
            return (data.hex(),)
        elif encoding == "Base64":
            return (base64.b64encode(data).decode("utf-8"),)
        elif encoding == "UTF-8":
            return (data.decode("utf-8"),)
        elif encoding == "Binary":
            return ("".join(f"{byte:08b}" for byte in data),)
        elif encoding == "Raw Bytes":
            return (repr(data),)
        else:
            raise ValueError("Unsupported encoding")


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SystemRandom": SystemRandom,
    "String2Binary": String2Binary,
    "Binary2String": Binary2String,
    "String2Hex": String2Hex,
    "Hex2String": Hex2String,
    "String2Base64": String2Base64,
    "Base642String": Base642String,
    "BitwiseAND": BitwiseAND,
    "BitwiseOR": BitwiseOR,
    "BitwiseNOT": BitwiseNOT,
    "BitwiseXOR": BitwiseXOR,
    "BitwiseLS": BitwiseLS,
    "BitwiseRS": BitwiseRS,
    "StringLooper": StringLooper,
    "ByteslikeEncode": ByteslikeEncode,
    "ByteslikeDecode": ByteslikeDecode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SystemRandom": "Random Nonce Generator",
    "String2Binary": "String to Binary Converter",
    "Binary2String": "Binary to String Converter",
    "String2Hex": "String to Hexadecimal Converter",
    "Hex2String": "Hexadecimal to String Converter",
    "String2Base64": "String to Base64 Converter",
    "Base642String": "Base64 to String Converter",
    "BitwiseAND": "Bitwise AND Operator",
    "BitwiseOR": "Bitwise OR Operator",
    "BitwiseNOT": "Bitwise NOT Operator",
    "BitwiseXOR": "Bitwise XOR Operator",
    "BitwiseLS": "Bitwise Left Shift Operator",
    "BitwiseRS": "Bitwise Right Shift Operator",
    "StringLooper": "String Append Looper",
    "ByteslikeEncode": "Bytes-like Object Encode",
    "ByteslikeDecode": "Bytes-like Object Decode",
}
