# HKDF (Expand Only) Key Derivation

Derives a key using the "expand" step of the HKDF algorithm.

Source library: `cryptography`

## Overview

This node implements only the "expand" step of the HMAC-based Extract-and-Expand Key Derivation Function (HKDF) from RFC 5869. This is useful if you have already performed the "extract" step separately to get a pseudorandom key (PRK). The expand step takes the PRK and generates a key of the desired length.

It is not intended for password hashing.

## Parameters

- **message**: The pseudorandom key (`PRK`) to expand, as a `BYTESLIKE` object. This should be the output of an HKDF extract step and should have a length of at least `hash.digest_size`.
- **length**: The desired length of the output key in bytes.
- **algorithm**: The hash function to use for the underlying HMAC operation (e.g., `SHA256`).
- **info**: (Optional) Application-specific context information as a `BYTESLIKE` object.

## Outputs

- **derived_key**: The resulting output keying material (`OKM`) as a `BYTESLIKE` object.
