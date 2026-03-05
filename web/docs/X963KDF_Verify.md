# X963KDF Key Verification

Verifies a key derived with the X963KDF algorithm.

Source library: `cryptography`

## Overview

This node re-derives a key using the same input parameters as the `X963KDF Key Derivation` node and compares it in constant time to an expected key.

## Parameters

- **message**: The original shared secret (`Z`) as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **algorithm**: The original hash function used.
- **info**: (Optional) The original shared information.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the re-derived key matches the expected key, and `False` otherwise.
