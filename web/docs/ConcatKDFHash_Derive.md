# ConcatKDF (Hash) Key Derivation

Derives a key using the Concatenation Key Derivation Function with a standard hash.

Source library: `cryptography`

## Overview

This node implements the Concatenation Key Derivation Function from NIST SP 800-56A. The function works by hashing the concatenation of a counter, the input keying material, and optional context-specific information.

This KDF is suitable for deriving keys from a shared secret, but it is **not** intended for hashing passwords.

## Parameters

- **message**: The input keying material (e.g., a shared secret) as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **algorithm**: The hash function to use (e.g., `SHA256`).
- **other_info**: (Optional) Application-specific context information as a `BYTESLIKE` object. This can be used to bind the derived key to a specific purpose or context.

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
