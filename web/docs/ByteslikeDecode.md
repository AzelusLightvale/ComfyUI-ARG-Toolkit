# Bytes-like Object Decode

Decodes a raw `BYTESLIKE` object into a human-readable string using various formats.

## Overview

This node is the counterpart to `Bytes-like Object Encode`. It takes a `BYTESLIKE` object (raw bytes) and converts it into a string representation based on the chosen format. This is useful for viewing the output of cryptographic nodes or preparing data for display or further text-based processing.

## Parameters

- **data**: The input `BYTESLIKE` object to be decoded.
- **encoding**: The format to use for converting the bytes into a string.
    - **Hexadecimal**: Converts the bytes into a hexadecimal string (e.g., "deadbeef").
    - **Base64**: Encodes the bytes into a Base64 string.
    - **UTF-8**: Decodes the bytes into a string using the UTF-8 standard. This will fail if the bytes are not valid UTF-8.
    - **Binary**: Converts the bytes into a binary string of 0s and 1s.
    - **Raw Bytes**: Converts the bytes into their Python literal string representation (e.g., `b'\\xde\\xad'`).

## Outputs

- **STRING**: The resulting string representation of the input bytes.
