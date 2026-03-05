# PBKDF2HMAC Key Verification

Verifies a password against a previously derived PBKDF2HMAC key.

Source library: `cryptography`

## Overview

This node is the counterpart to `PBKDF2HMAC Key Derivation`. It takes a password and the original derivation parameters and checks if they produce the expected key. This is the standard way to verify user passwords without storing them in plaintext.

## Parameters

- **message**: The input password or message to verify, as a `BYTESLIKE` object.
- **expected_key**: The `BYTESLIKE` key to check against.
- **length**: The length of the derived key in bytes. Must match the original derivation.
- **salt**: The original `BYTESLIKE` salt used for derivation.
- **iterations**: The original number of iterations.
- **algorithm**: The original hash function used for the HMAC operation.

## Outputs

- **verified_status**: A `BOOLEAN` that is `True` if the password hashes to the expected key, and `False` otherwise.
