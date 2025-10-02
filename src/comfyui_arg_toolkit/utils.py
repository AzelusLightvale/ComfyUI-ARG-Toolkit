import os
import base64
import re

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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("rand_value",)
    FUNCTION = "SystemRandom"

    def SystemRandom(self, byte_num):
        return ((os.urandom(byte_num)).hex(),)


# THe converter category of Utilities


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
        return (
            " ".join(
                format(c, "b")
                for c in bytearray(
                    text, self.encoding_selector(encoding_format, other_encoding_format)
                )
            ),
        )


class Binary2String(ConverterNodes):
    def binary2string(self, text, encoding_format, other_encoding_format):
        return (
            bytes(int(b, 2) for b in text.split(" ")).decode(
                self.encoding_selector(encoding_format, other_encoding_format)
            ),
        )


class String2Hex(ConverterNodes):
    def string2hex(self, text, encoding_format, other_encoding_format):
        return (
            text.encode(
                self.encoding_selector(encoding_format, other_encoding_format)
            ).hex(),
        )


class Hex2String(ConverterNodes):
    def hex2string(self, text, encoding_format, other_encoding_format):
        return (
            bytes.fromhex(text.replace("0x", "").replace(" ", "")).decode(
                self.encoding_selector(encoding_format, other_encoding_format)
            ),
        )


class String2Base64(ConverterNodes):
    def string2base64(self, text, encoding_format, other_encoding_format):
        return (
            base64.b64encode(
                text.encode(
                    self.encoding_selector(encoding_format, other_encoding_format)
                )
            ).decode("ascii"),
        )


class Base642String(ConverterNodes):
    def base642string(self, text, encoding_format, other_encoding_format):
        return (
            base64.b64decode(text.encode("ascii")).decode(
                self.encoding_selector(encoding_format, other_encoding_format)
            ),
        )


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
                        "tooltip": "The main string to compare against. Accepts encoded string, binary string (starting with 0b and number strings starting from 0 with only 1s and 0s), hexadecimal string (starting with 0x or only containing alphanumerics from A-F), integer strings, and Base64 string. Note that this will return the same type of text you give it. Example: give this base64, and the output returns base64 as well.",
                    },
                ),
                "text_2": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Type your message here...",
                        "tooltip": "The secondary string to compare against. Accepts encoded string, binary string (starting with 0b and number strings starting from 0 with only 1s and 0s), hexadecimal string (starting with 0x or only containing alphanumerics from A-F), integer strings, and Base64 string.",
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
    RETURN_NAMES = ("bitwise_txt",)

    def encoding_selector(self, encoding_format, other_encoding_format):
        if encoding_format == "Other":
            encoding_format = other_encoding_format
        return encoding_format

    def detect_and_parse(self, text, encoding_format, other_encoding_format=None):
        text = text.strip()
        b64_pattern = re.compile(r"^[A-Za-z0-9+/]*={0,2}$")
        hex_pattern = re.compile(r"^(0x)?[0-9a-fA-F]+$")

        # Binary string detection
        if text.startswith("0b") and all(c in "01" for c in text[2:]):
            cleaned = text[2:]
            if len(cleaned) % 8 != 0:
                # pad to nearest byte
                cleaned = cleaned.zfill(((len(cleaned) + 7) // 8) * 8)
            return bytes(
                int(cleaned[i : i + 8], 2) for i in range(0, len(cleaned), 8)
            ), "Binary"

        # Leading 0 + digits 0/1 → implicit binary
        elif text.startswith("0") and all(c in "01" for c in text):
            # pad to nearest byte
            cleaned = text.zfill(((len(text) + 7) // 8) * 8)
            return bytes(
                int(cleaned[i : i + 8], 2) for i in range(0, len(cleaned), 8)
            ), "Binary"

        # Integer detection
        elif text.isdigit():  # simple positive integer
            val = int(text)
            # Convert to minimal number of bytes to hold it
            length = max(1, (val.bit_length() + 7) // 8)
            return val.to_bytes(length, "big"), "Int"

        # Hex detection
        elif hex_pattern.match(text):
            cleaned = text.replace("0x", "").replace(" ", "")
            if len(cleaned) % 2 != 0:
                # Pad with a leading zero if odd length
                cleaned = "0" + cleaned
            return bytes.fromhex(cleaned), "Hex"

        # Base64 detection
        elif len(text) > 1 and b64_pattern.match(text) and len(text) % 4 == 0:
            try:
                return base64.b64decode(text), "Base64"
            except Exception:
                pass  # Not valid Base64, fall through

        # Default to chosen formatted string
        else:
            return text.encode(
                self.encoding_selector(encoding_format, other_encoding_format)
            ), "String"

    def operate(
        self, text_1, text_2, encoding_format, other_encoding_format=None, func=None
    ):
        """
        func: a callable that takes one or two byte objects and returns bytes
        Returns: (result_bytes, detected_format_of_input1)
        """
        b1, return_fmt = self.detect_and_parse(
            text_1, encoding_format, other_encoding_format
        )

        if text_2 is not None:
            b2, _ = self.detect_and_parse(
                text_2, encoding_format, other_encoding_format
            )
            # Ensure same length for operations that need it
            if len(b1) != len(b2):
                raise ValueError("Inputs must be same length for bitwise operations")
            result = func(b1, b2)
        else:
            result = func(b1)

        return result, return_fmt

    def format_output(
        self, data, output_format, encoding_format, other_encoding_format=None
    ):
        if output_format == "Binary":
            return " ".join(format(b, "08b") for b in data)
        elif output_format == "Hex":
            return data.hex()
        elif output_format == "Base64":
            return base64.b64encode(data).decode()
        elif output_format == "Int":
            return str(int.from_bytes(data, "big"))
        elif output_format == "String":
            return data.decode(
                self.encoding_selector(encoding_format, other_encoding_format)
            )
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
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


class BitwiseOR(BitwiseNodes):
    def bitwiseor(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x | y for x, y in zip(b1, b2)),
        )
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


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
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


class BitwiseXOR(BitwiseNodes):
    def bitwisexor(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2)),
        )
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


class BitwiseLS(BitwiseNodes):
    def bitwisels(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x << y for x, y in zip(b1, b2)),
        )
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


class BitwiseRS(BitwiseNodes):
    def bitwisers(self, text_1, text_2, encoding_format, other_encoding_format):
        result_bytes, input_format = self.operate(
            text_1,
            text_2,
            encoding_format,
            other_encoding_format,
            func=lambda b1, b2: bytes(x >> y for x, y in zip(b1, b2)),
        )
        return (
            self.format_output(
                result_bytes, input_format, encoding_format, other_encoding_format
            ),
        )


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
}
