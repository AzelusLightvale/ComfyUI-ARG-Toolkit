# HKDF Key Derivation

Derives a key using the HMAC-based Extract-and-Expand Key Derivation Function (HKDF).

Source library: `cryptography`

## Overview

This node implements the full two-step HKDF process from RFC 5869.

1.  **Extract**: Takes the input keying material (`IKM`) and a salt to produce a fixed-length pseudorandom key (`PRK`).
2.  **Expand**: Takes the `PRK` and expands it to the desired key length.

HKDF is a standard and secure way to derive one or more keys from a master secret. It is **not** intended for hashing passwords.

## Parameters

- **message**: The input keying material (`IKM`) as a `BYTESLIKE` object. This can be a low-entropy secret.
- **length**: The desired length of the output key in bytes.
- **algorithm**: The hash function to use for the underlying HMAC operation (e.g., `SHA256`).
- **salt**: (Optional) A `BYTESLIKE` salt. While optional, using a salt is highly recommended to mix in additional entropy and ensure uniqueness.
- **info**: (Optional) Application-specific context information as a `BYTESLIKE` object. This helps bind the derived key to a specific context.

## Outputs

- **derived_key**: The resulting output keying material (`OKM`) as a `BYTESLIKE` object.
