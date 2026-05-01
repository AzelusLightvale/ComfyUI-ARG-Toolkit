# ConcatKDF (HMAC) Key Derivation

Derives a key using the Concatenation Key Derivation Function with HMAC.

Source library: `cryptography`

## Overview

This node implements the Concatenation Key Derivation Function using HMAC, as specified in NIST SP 800-56A. It is similar to the hash-based version but uses HMAC for potentially stronger security properties, especially when a salt is used.

This KDF is suitable for deriving keys from a shared secret, but it is **not** intended for hashing passwords.

## Parameters

- **message**: The input keying material (e.g., a shared secret) as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **algorithm**: The hash function to use for the underlying HMAC operation (e.g., `SHA256`).
- **salt**: (Optional) A `BYTESLIKE` salt. While optional, using a salt is highly recommended to randomize the KDF's output.
- **other_info**: (Optional) Application-specific context information as a `BYTESLIKE` object. This can be used to bind the derived key to a specific purpose or context.

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
