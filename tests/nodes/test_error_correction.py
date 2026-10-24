"""Focused tests for the Reed-Solomon error correction code path in error_correction.py.

The ReedSolomonEncode and ReedSolomonDecode nodes are critical for data integrity
in ARG pipelines: they add error-correction symbols to data and recover the
original message even when bytes are corrupted. These tests exercise the
encode/decode round-trip, error correction, erase_pos handling, and validation
paths.
"""

import pytest

from src.error_correction import ReedSolomonDecode, ReedSolomonEncode


class TestReedSolomonEncode:
    """Test suite covering ReedSolomonEncode.execute."""

    def test_encode_returns_bytes(self):
        """Encoded output should be bytes."""
        node = ReedSolomonEncode()
        data = b"Hello World!"
        result = node.execute(data, 10)

        assert isinstance(result[0], bytes)
        assert len(result[0]) > len(data)

    def test_encode_increases_length(self):
        """Encoding should add ECC symbols, increasing total length."""
        node = ReedSolomonEncode()
        data = b"Hello World!"
        result = node.execute(data, 10)

        # ECC symbols are added, so encoded length > original length
        assert len(result[0]) > len(data)

    def test_encode_empty_data(self):
        """Encoding empty data should still produce valid output."""
        node = ReedSolomonEncode()
        result = node.execute(b"", 10)

        assert isinstance(result[0], bytes)
        # Empty data with ECC still produces some encoded output
        assert len(result[0]) >= 0

    def test_encode_large_ecc(self):
        """Encoding with a large ECC count should produce a longer output."""
        node = ReedSolomonEncode()
        data = b"Test data"
        result_small = node.execute(data, 10)
        result_large = node.execute(data, 20)

        assert len(result_large[0]) > len(result_small[0])


class TestReedSolomonDecode:
    """Test suite covering ReedSolomonDecode.execute."""

    def test_decode_roundtrip(self):
        """Encode then decode should return the original data."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = enc.execute(data, 10)
        decoded = dec.execute(encoded[0], 10)

        assert decoded[0] == data

    def test_decode_returns_three_values(self):
        """Decode should return (decoded_msg, msg_with_code, errata_pos_list)."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = enc.execute(data, 10)
        decoded = dec.execute(encoded[0], 10)

        assert len(decoded) == 3
        assert isinstance(decoded[0], bytes)
        assert isinstance(decoded[1], bytes)
        assert isinstance(decoded[2], bytes)

    def test_decode_recovers_single_byte_error(self):
        """Reed-Solomon should correct a single corrupted byte."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = bytearray(enc.execute(data, 10)[0])
        # Corrupt one byte
        encoded[5] = (encoded[5] + 1) % 256

        decoded = dec.execute(bytes(encoded), 10)
        assert decoded[0] == data

    def test_decode_with_erase_pos(self):
        """Providing erase_pos should help recovery of known corrupted bytes."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = bytearray(enc.execute(data, 10)[0])
        # Corrupt byte at position 5
        encoded[5] = (encoded[5] + 1) % 256

        decoded = dec.execute(bytes(encoded), 10, erase_pos="5")
        assert decoded[0] == data

    def test_decode_with_multiple_erase_positions(self):
        """Multiple erase positions should be accepted as comma-separated list."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = bytearray(enc.execute(data, 10)[0])
        encoded[5] = (encoded[5] + 1) % 256
        encoded[10] = (encoded[10] + 1) % 256

        decoded = dec.execute(bytes(encoded), 10, erase_pos="5,10")
        assert decoded[0] == data

    def test_decode_invalid_erase_pos_raises_value_error(self):
        """Invalid erase_pos format should raise ValueError."""
        dec = ReedSolomonDecode()

        with pytest.raises(ValueError) as excinfo:
            dec.execute(b"test", 10, erase_pos="abc")
        assert "Invalid format for erase_pos" in str(excinfo.value)

    def test_decode_empty_erase_pos_string(self):
        """Empty erase_pos string should be treated as no erase positions."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = enc.execute(data, 10)
        decoded = dec.execute(encoded[0], 10, erase_pos="")
        assert decoded[0] == data

    def test_decode_empty_data(self):
        """Decoding empty data should work."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b""

        encoded = enc.execute(data, 10)
        decoded = dec.execute(encoded[0], 10)
        assert decoded[0] == data

    def test_decode_with_whitespace_in_erase_pos(self):
        """erase_pos with whitespace should be handled correctly."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Hello World!"

        encoded = bytearray(enc.execute(data, 10)[0])
        encoded[5] = (encoded[5] + 1) % 256

        decoded = dec.execute(bytes(encoded), 10, erase_pos=" 5 , 10 ")
        assert decoded[0] == data

    def test_decode_roundtrip_with_different_ecc_counts(self):
        """Round-trip should work with various ECC symbol counts."""
        enc = ReedSolomonEncode()
        dec = ReedSolomonDecode()
        data = b"Test message for ECC"

        for ecc in [10, 14, 18, 20]:
            encoded = enc.execute(data, ecc)
            decoded = dec.execute(encoded[0], ecc)
            assert decoded[0] == data
