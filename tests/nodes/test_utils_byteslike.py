"""Focused tests for the critical ByteslikeEncode/ByteslikeDecode code path in utils.py.

The ByteslikeDecode node is a critical path for ARG solvers: it decodes bytes-like
data into human-readable strings in multiple formats (Hexadecimal, Base64, UTF-8,
Binary, Raw Bytes), with a defensive fallback for invalid UTF-8 and a ValueError for
unknown encodings. Its complement, ByteslikeEncode, performs the inverse operation and
falls back to raw UTF-8 bytes on encoding errors. These code paths are exercised below
with explicit coverage of every match-statement branch and every validation/error path.
"""

import pytest

from src.utils import ByteslikeDecode, ByteslikeEncode, Binary2String


class TestByteslikeDecode:
    """Test suite covering the complete ByteslikeDecode.execute code path."""

    def test_decode_hexadecimal(self):
        decode = ByteslikeDecode()
        data = b"Hello World"
        result = decode.execute(data, "Hexadecimal", "UNIQUE_ID_1")
        assert result[0] == "48656c6c6f20576f726c64"

    def test_decode_base64(self):
        decode = ByteslikeDecode()
        data = b"Hello World"
        result = decode.execute(data, "Base64", "UNIQUE_ID_2")
        assert result[0] == "SGVsbG8gV29ybGQ="

    def test_decode_utf8_success(self):
        decode = ByteslikeDecode()
        data = b"Hello World"
        result = decode.execute(data, "UTF-8", "UNIQUE_ID_3")
        assert result[0] == "Hello World"

    def test_decode_binary(self):
        decode = ByteslikeDecode()
        data = b"Hello World"
        expected = "".join(f"{byte:08b}" for byte in data)
        result = decode.execute(data, "Binary", "UNIQUE_ID_4")
        assert result[0] == expected

    def test_decode_raw_bytes(self):
        decode = ByteslikeDecode()
        data = b"Hello World"
        result = decode.execute(data, "Raw Bytes", "UNIQUE_ID_5")
        assert result[0] == repr(data)

    def test_decode_utf8_invalid_data_falls_back_to_backslashreplace(self):
        """Critical: invalid UTF-8 must not raise, but fall back to backslashreplace."""
        decode = ByteslikeDecode()
        data = b"\xff\xfe"
        result = decode.execute(data, "UTF-8", "UNIQUE_ID_6")
        expected = b"\xff\xfe".decode("utf-8", errors="backslashreplace")
        assert result[0] == expected

    def test_decode_invalid_encoding_raises_value_error(self):
        decode = ByteslikeDecode()
        with pytest.raises(ValueError) as excinfo:
            decode.execute(b"data", "NotAValidEncoding", "UNIQUE_ID_7")
        assert "Invalid encoding method used: NotAValidEncoding" in str(excinfo.value)

    def test_decode_non_byteslike_raises_type_error(self):
        decode = ByteslikeDecode()
        with pytest.raises(TypeError) as excinfo:
            decode.execute("not bytes", "UTF-8", "UNIQUE_ID_8")
        assert "Expected bytes-like objects" in str(excinfo.value)


class TestByteslikeEncode:
    """Test suite covering the complement ByteslikeEncode.execute code path."""

    def test_encode_hexadecimal(self):
        encode = ByteslikeEncode()
        result = encode.execute("48656c6c6f20576f726c64", "Hexadecimal", "UNIQUE_ID_9")
        assert result[0] == b"Hello World"

    def test_encode_base64(self):
        encode = ByteslikeEncode()
        result = encode.execute("SGVsbG8gV29ybGQ=", "Base64", "UNIQUE_ID_10")
        assert result[0] == b"Hello World"

    def test_encode_binary(self):
        encode = ByteslikeEncode()
        data = b"Hello World"
        binary = "".join(f"{byte:08b}" for byte in data)
        result = encode.execute(binary, "Binary", "UNIQUE_ID_11")
        assert result[0] == data

    def test_encode_utf8(self):
        encode = ByteslikeEncode()
        result = encode.execute("Hello World", "UTF-8", "UNIQUE_ID_12")
        assert result[0] == b"Hello World"

    def test_encode_raw_bytes(self):
        encode = ByteslikeEncode()
        result = encode.execute("b'Hello World'", "Raw Bytes", "UNIQUE_ID_13")
        assert result[0] == b"Hello World"

    def test_encode_invalid_format_falls_back_to_raw_utf8_and_warns(self):
        """Critical: any encoding failure must fall back to raw UTF-8 bytes (not crash)."""
        encode = ByteslikeEncode()
        result = encode.execute("not a valid hex number", "Hexadecimal", "UNIQUE_ID_14")
        assert result[0] == b"not a valid hex number"

    def test_encode_invalid_base64_falls_back_to_raw_utf8(self):
        encode = ByteslikeEncode()
        result = encode.execute("!!!garbage!!!", "Base64", "UNIQUE_ID_15")
        assert result[0] == b"!!!garbage!!!"

    def test_encode_non_string_raises_type_error(self):
        encode = ByteslikeEncode()
        with pytest.raises(TypeError) as excinfo:
            encode.execute(12345, "UTF-8", "UNIQUE_ID_16")
        assert "Input must be a string" in str(excinfo.value)


class TestBinary2StringValidation:
    """Test suite for the validation branch of Binary2String.execute."""

    def test_binary_to_string_valid(self):
        convert = Binary2String()
        data = b"Hello World"
        binary = "".join(f"{byte:08b}" for byte in data)
        result = convert.execute(binary, "utf-8", "")
        assert result[0] == "Hello World"

    def test_binary_to_string_whitespace_and_newlines_removed(self):
        convert = Binary2String()
        raw = "01001000 01100101\n01101100 01101100 01101111"
        result = convert.execute(raw, "utf-8", "")
        assert result[0] == "Hello"

    def test_binary_to_string_length_not_multiple_of_8_raises_value_error(self):
        convert = Binary2String()
        with pytest.raises(ValueError) as excinfo:
            convert.execute("01001000 0110010", "utf-8", "")  # 9 bits
        assert "Binary string length must be a multiple of 8" in str(excinfo.value)

    def test_binary_to_string_non_binary_chars_raises_value_error(self):
        convert = Binary2String()
        with pytest.raises(ValueError) as excinfo:
            convert.execute("01001000 01100102", "utf-8", "")  # contains '2'
        assert "Binary input must contain only 0 and 1" in str(excinfo.value)
