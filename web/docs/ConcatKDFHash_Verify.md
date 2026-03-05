# ConcatKDF (Hash) Key Verification

Verifies a key derived with the ConcatKDF (Hash) algorithm.

Source library: `cryptography`

## Overview

This node re-derives a key using the same input parameters as the `ConcatKDF (Hash) Key Derivation` node and compares it in constant time to an expected key.

## Parameters

- **message**: The original input keying material as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **algorithm**: The original hash function used.
- **other_info**: (Optional) The original application-specific context information.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the re-derived key matches the expected key, and `False` otherwise.
