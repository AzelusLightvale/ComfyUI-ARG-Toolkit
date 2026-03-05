# HKDF (Expand Only) Key Verification

Verifies a key derived with the HKDF "expand" step.

Source library: `cryptography`

## Overview

This node re-derives a key using the same input parameters as the `HKDF (Expand Only) Key Derivation` node and compares it in constant time to an expected key.

## Parameters

- **message**: The original pseudorandom key (`PRK`) as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **algorithm**: The original hash function used for the HMAC operation.
- **info**: (Optional) The original application-specific context information.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the re-derived key matches the expected key, and `False` otherwise.
