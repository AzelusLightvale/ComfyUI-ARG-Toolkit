# Argon2id Key Verification

Verifies a password or message against a previously derived Argon2id key or hash.

Source library: `cryptography`

## Overview

This node is the counterpart to `Argon2id Key Derivation`. It takes a password and the original derivation parameters and checks if they match a given key or PHC-formatted hash string. This is the standard way to verify user passwords without storing them in plaintext.

## Parameters

- **message**: The input password or message to verify, as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key or PHC-formatted string to verify against.
- **length**: The desired length of the derived key in bytes. Must match the original derivation.
- **salt**: The original `BYTESLIKE` salt used for derivation.
- **mode**:
    - `string`: Verifies against a raw derived key.
    - `phc`: Verifies against a PHC-formatted string. The salt and parameters are taken from the string itself, so the `salt`, `iterations`, `parallel_lanes`, and `memory_cost` inputs are ignored.
- **iterations**: The original time cost.
- **parallel_lanes**: The original degree of parallelism.
- **memory_cost**: The original memory cost in KiB.
- **ad**: (Optional) The original `BYTESLIKE` associated data.
- **secret**: (Optional) The original `BYTESLIKE` secret data.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the password matches the expected key/hash, and `False` otherwise.
