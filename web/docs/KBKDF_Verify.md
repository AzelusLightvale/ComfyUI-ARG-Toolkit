# KBKDF Key Verification

Verifies a key derived with the KBKDF algorithm.

Source library: `cryptography`

## Overview

This node re-derives a key using the same input parameters as the `KBKDF Key Derivation` node and compares it in constant time to an expected key.

## Parameters

- **message**: The original master key (`Ki`) as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **algorithm**: The original hash function used for the PRF.
- **operation_mode**: The original PRF used (`KBKDFHMAC` or `KBKDFCMAC`).
- **location**: The original counter position.
- **rlen**: The original counter length.
- **llen**: The original key length field length.
- **label**: (Optional) The original label.
- **context**: (Optional) The original context.
- **fixed**: (Optional) The original fixed data.
- **break_location**: (Optional) The original break location for `MiddleFixed` mode.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the re-derived key matches the expected key, and `False` otherwise.
