# X963KDF Key Derivation

Derives a key using the ANSI X9.63 Key Derivation Function.

Source library: `cryptography`

## Overview

This node implements the Key Derivation Function specified in ANSI X9.63, which is commonly used in elliptic curve cryptography standards for deriving keys from a shared secret. Its structure is similar to `ConcatKDFHash`.

This KDF is suitable for deriving keys from a shared secret, but it is **not** intended for hashing passwords.

## Parameters

- **message**: The shared secret (`Z`) to derive the key from, as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **algorithm**: The hash function to use (e.g., `SHA256`).
- **info**: (Optional) Shared information as a `BYTESLIKE` object, used to bind the key to a specific context.

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
