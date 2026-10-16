# ECDH Public Key Bytes

Serializes an X25519 or X448 public key.

Source library: `cryptography`

## Overview

This node extracts the public key from an X25519/X448 private key and serializes it into bytes. Public keys are used in Diffie-Hellman key exchange to derive a shared secret between two parties.

## Parameters

- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new random private key.
    - **From Private Bytes**: Uses a previously serialized private key.
- **key_type**: The curve (**x25519** or **x448**).
- **encoding**: The encoding format (**PEM** or **DER**).
- **formatting**: The key format.
    - **SubjectPublicKeyInfo**: The standard X.509 format.
    - **Raw**: The raw key bytes (32 bytes for x25519, 56 bytes for x448).
- **private_key**: (Optional) The serialized private key bytes. Required when `key_source` is "From Private Bytes".

## Outputs

- **public_bytes**: The serialized public key as a `BYTESLIKE` object.
- **public_key**: The public key object (`KEYOBJ`), which can be passed to the ECDH Shared Key Exchange node.

## Additional Considerations

- Public keys are not secret and can be freely shared. They are used only for key exchange.
- The `Raw` format produces the smallest representation (32 bytes for x25519), which is the format expected by the XExchange node.
