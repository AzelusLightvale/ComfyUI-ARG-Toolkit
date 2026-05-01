# Bytes-like Object Encode

Encodes a string from various formats into a raw `BYTESLIKE` object.

## Overview

This node is a versatile encoder that converts a standard string input into a `BYTESLIKE` object. `BYTESLIKE` is the raw byte data type used by many cryptographic and low-level nodes in this toolkit. The node can interpret the input string as Hexadecimal, Base64, UTF-8, Binary, or a Python bytes literal, providing a bridge from human-readable formats to the byte-level data required for complex operations.

## Parameters

- **text**: The input string to be encoded. The interpretation of this string depends on the `encoding` parameter.
- **encoding**: The format to use for interpreting the input `text` and converting it to bytes.
    - **Hexadecimal**: Treats the input string as a hex string (e.g., "DEADBEEF") and converts it to bytes.
    - **Base64**: Treats the input string as a Base64 encoded string and decodes it to bytes.
    - **UTF-8**: Encodes the input string directly into bytes using the UTF-8 standard. This is for converting plain text.
    - **Binary**: Treats the input string as a binary string (e.g., "0110100001101001") and converts it to bytes.
    - **Raw Bytes**: Evaluates the input string as a Python bytes literal (e.g., `b'hello'` or `b'\\xde\\xad'`).

## Outputs

- **BYTESLIKE**: The resulting raw `BYTESLIKE` object.
