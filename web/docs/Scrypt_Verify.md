# Scrypt Key Verification

Verifies a password against a previously derived Scrypt key.

Source library: `cryptography`

## Overview

This node is the counterpart to `Scrypt Key Derivation`. It takes a password and the original derivation parameters (`salt`, `n`, `r`, `p`) and checks if they produce the expected key. This is the standard way to verify user passwords hashed with Scrypt.

## Parameters

- **message**: The input password or message to verify, as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **salt**: The original `BYTESLIKE` salt used for derivation.
- **n**: The original CPU/Memory cost parameter (as a power-of-2 exponent).
- **r**: The original block size parameter.
- **p**: The original parallelization parameter.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the password hashes to the expected key, and `False` otherwise.
