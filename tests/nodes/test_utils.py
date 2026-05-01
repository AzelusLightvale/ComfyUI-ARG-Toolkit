from src import utils

# Test suite for utils.py
class TestUtils:
    # Converters
    def test_string_to_binary(self):
        string_to_binary = utils.String2Binary()
        text = "Hello World"
        encoding = "utf-8"
        binary_text = string_to_binary.string2binary(text, encoding, "")
        assert binary_text[0] == "1001000 1100101 1101100 1101100 1101111 100000 1010111 1101111 1110010 1101100 1100100"

    def test_binary_to_string(self):
        binary_to_string = utils.Binary2String()
        binary_text = "1001000 1100101 1101100 1101100 1101111 100000 1010111 1101111 1110010 1101100 1100100"
        encoding = "utf-8"
        text = binary_to_string.binary2string(binary_text, encoding, "")
        assert text[0] == "Hello World"

    def test_string_to_hex(self):
        string_to_hex = utils.String2Hex()
        text = "Hello World"
        encoding = "utf-8"
        hex_text = string_to_hex.string2hex(text, encoding, "")
        assert hex_text[0] == "48656c6c6f20576f726c64"

    def test_hex_to_string(self):
        hex_to_string = utils.Hex2String()
        hex_text = "48656c6c6f20576f726c64"
        encoding = "utf-8"
        text = hex_to_string.hex2string(hex_text, encoding, "")
        assert text[0] == "Hello World"

    def test_string_to_base64(self):
        string_to_base64 = utils.String2Base64()
        text = "Hello World"
        encoding = "utf-8"
        base64_text = string_to_base64.string2base64(text, encoding, "")
        assert base64_text[0] == "SGVsbG8gV29ybGQ="

    def test_base64_to_string(self):
        base64_to_string = utils.Base642String()
        base64_text = "SGVsbG8gV29ybGQ="
        encoding = "utf-8"
        text = base64_to_string.base642string(base64_text, encoding, "")
        assert text[0] == "Hello World"

    # Bitwise Operators
    def test_bitwise_and(self):
        bitwise_and = utils.BitwiseAND()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_and.bitwiseand(text1, text2, encoding, "")
        assert result[0] == "6065606c64"

    def test_bitwise_or(self):
        bitwise_or = utils.BitwiseOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_or.bitwiseor(text1, text2, encoding, "")
        assert result[0] == "7f6f7e6c6f"

    def test_bitwise_xor(self):
        bitwise_xor = utils.BitwiseXOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        encoding = "utf-8"
        result = bitwise_xor.bitwisexor(text1, text2, encoding, "")
        assert result[0] == "1f0a1e000b"

    def test_bitwise_not(self):
        bitwise_not = utils.BitwiseNOT()
        text = "68656c6c6f"
        encoding = "utf-8"
        result = bitwise_not.bitwisenot(text, encoding, "")
        assert result[0] == "979a939390"
