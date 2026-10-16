# ECDH Shared Key Exchange

Performs an X25519 or X448 Diffie-Hellman key exchange to derive a shared secret.

Source library: `cryptography`

## Overview

This node performs an Elliptic Curve Diffie-Hellman (ECDH) key exchange using the X25519 or X448 curve. Given a private key and the other party's public key, it computes a shared secret that can be used to derive symmetric encryption keys. This is the foundational primitive for modern key exchange protocols.

## Parameters

- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new random private key.
    - **From Private Bytes**: Uses a previously serialized private key.
- **key_type**: The curve (**x25519** or **x448**).
- **public_key**: The other party's public key, as a `BYTESLIKE` object. This is expected in **Raw** format (32 bytes for x25519, 56 bytes for x448).
- **private_key**: (Optional) The serialized private key bytes. Required when `key_source` is "From Private Bytes".

## Outputs

- **shared_key**: The derived shared secret, as a `BYTESLIKE` object. This is a 32-byte (x25519) or 56-byte (x448) value that should be passed through a Key Derivation Function (KDF) before use as an encryption key.

## Additional Considerations

- **Never reuse a private key with multiple parties.** Each key pair should be used for a single exchange.
- The shared secret itself is not a suitable encryption key. Always pass it through a KDF (e.g., HKDF, ConcatKDF) with appropriate context information.
- X25519 does not provide authentication by itself. Combine it with a digital signature scheme (e.g., Ed25519) to prevent man-in-the-middle attacks.
- The public key input expects **Raw** format. If you have a serialized public key in PEM or DER format, use the appropriate loader node first.
