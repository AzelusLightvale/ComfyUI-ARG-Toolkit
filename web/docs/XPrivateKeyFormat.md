# ECDH Private Key Bytes

Generates an X25519 or X448 private key and serializes it.

Source library: `cryptography`

## Overview

X25519 and X448 are elliptic curves designed for Diffie-Hellman key exchange (ECDH). This node generates a private key for one of these curves and serializes it into bytes. X25519 is the most widely adopted, used in modern protocols like TLS 1.3 and Noise.

## Parameters

- **key_type**: The curve to use (**x25519** or **x448**).
- **encoding**: The encoding format for the serialized key.
    - **PEM**: Privacy-Enhanced Mail format.
    - **DER**: Distinguished Encoding Rules (binary).
    - **Raw**: The raw key bytes.
- **formatting**: The key format.
    - **PKCS8**: Standard format for private keys.
    - **Raw**: The raw key material.
- **encryption**: How to encrypt the private key (**Best Available** or **None**).
- **encryption_password**: (Optional) The password for encrypting the private key.

## Outputs

- **private_bytes**: The serialized private key as a `BYTESLIKE` object.
- **private_key**: The loaded private key object (`KEYOBJ`), which can be passed to the ECDH Shared Key Exchange node.

## Additional Considerations

- X25519/X448 keys are used exclusively for key exchange, not for signing. Use EdDSA (Ed25519/Ed448) for signatures.
- The `Raw` format with `NoEncryption` stores the key in its most vulnerable state. Use only in secure environments.
