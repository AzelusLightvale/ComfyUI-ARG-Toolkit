from src import utils

# Test suite for utils.py


class TestUtils:
    # Converters

    def test_string_to_binary(self):
        string_to_binary = utils.String2Binary()
        text = "Hello World"
        binary_text = string_to_binary.execute(text, "utf-8", "")
        expected = " ".join(format(b, "08b") for b in bytearray(text, "utf-8"))
        assert binary_text[0] == expected

    def test_binary_to_string(self):
        binary_to_string = utils.Binary2String()
        binary_text = " ".join(format(b, "08b") for b in bytearray("Hello World", "utf-8"))
        text = binary_to_string.execute(binary_text, "utf-8", "")
        assert text[0] == "Hello World"

    def test_string_to_hex(self):
        string_to_hex = utils.String2Hex()
        text = "Hello World"
        hex_text = string_to_hex.execute(text, "utf-8", "")
        assert hex_text[0] == "48656c6c6f20576f726c64"

    def test_hex_to_string(self):
        hex_to_string = utils.Hex2String()
        hex_text = "48656c6c6f20576f726c64"
        text = hex_to_string.execute(hex_text, "utf-8", "")
        assert text[0] == "Hello World"

    def test_string_to_base64(self):
        string_to_base64 = utils.String2Base64()
        text = "Hello World"
        base64_text = string_to_base64.execute(text, "utf-8", "")
        assert base64_text[0] == "SGVsbG8gV29ybGQ="

    def test_base64_to_string(self):
        base64_to_string = utils.Base642String()
        base64_text = "SGVsbG8gV29ybGQ="
        text = base64_to_string.execute(base64_text, "utf-8", "")
        assert text[0] == "Hello World"

    def test_string_looper(self):
        looper = utils.StringLooper()
        result = looper.Looper("Hello ", 3)
        assert result[0] == "Hello Hello Hello "

    def test_bits_counter(self):
        counter = utils.BitsCounter()
        text = b"Hello"
        result = counter.execute(text)
        assert result[0] == len(text) * 8

    # Bitwise operators use a four-argument execute() signature; the source uses the
    # `encoding_format` parameter position for datatype detection, so tests below pass
    # an explicit supported datatype and compare against independently computed values.

    def test_bitwise_and(self):
        bitwise_and = utils.BitwiseAND()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        result = bitwise_and.execute(text1, text2, "Hexadecimal", "")
        expected = bytes(a & b for a, b in zip(bytes.fromhex(text1), bytes.fromhex(text2), strict=True)).hex()
        assert result[0] == expected

    def test_bitwise_or(self):
        bitwise_or = utils.BitwiseOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        result = bitwise_or.execute(text1, text2, "Hexadecimal", "")
        expected = bytes(a | b for a, b in zip(bytes.fromhex(text1), bytes.fromhex(text2), strict=True)).hex()
        assert result[0] == expected

    def test_bitwise_xor(self):
        bitwise_xor = utils.BitwiseXOR()
        text1 = "68656c6c6f"
        text2 = "776f726c64"
        result = bitwise_xor.execute(text1, text2, "Hexadecimal", "")
        expected = bytes(a ^ b for a, b in zip(bytes.fromhex(text1), bytes.fromhex(text2), strict=True)).hex()
        assert result[0] == expected

    def test_bitwise_not(self):
        bitwise_not = utils.BitwiseNOT()
        text = "68656c6c6f"
        result = bitwise_not.execute(text, "Hexadecimal", "")
        expected = bytes((~x & 0xFF) for x in bytes.fromhex(text)).hex()
        assert result[0] == expected
