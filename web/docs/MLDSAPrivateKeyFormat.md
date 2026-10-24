# ML-DSA Private Key Bytes

Generates a new ML-DSA private key and serializes it into bytes.

Source library: `cryptography`

## Overview

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) is a post-quantum digital signature scheme selected by NIST as a replacement for DSA and ECDSA. This node generates a new private key for one of the ML-DSA parameter sets and serializes it into a byte string. The key can optionally be encrypted with a password.

## Parameters

- **sig_alg**: The ML-DSA parameter set to use.
    - **ML-DSA-44**: Smaller, faster parameter set.
    - **ML-DSA-65**: Balanced security and performance (default).
    - **ML-DSA-87**: Highest security level.
- **key_source**: How to generate the private key.
    - **Fresh Key**: Generates a new random private key.
    - **Seed Bytes**: Derives the key from a provided 32-byte seed.
- **encoding**: The encoding format for the serialized key (**PEM**, **DER**, or **Raw**).
- **formatting**: The key format to serialize in (**PKCS8** or **Raw**).
- **encryption**: How to encrypt the private key (**Best Available** or **None**).
- **encryption_password**: (Optional) The password to use for encrypting the private key. Required when `encryption` is set to "Best Available".
- **seed_bytes**: (Optional) A `BYTESLIKE` 32-byte seed. Required when `key_source` is "Seed Bytes".

## Outputs

- **private_bytes**: The serialized private key as a `BYTESLIKE` object.
- **private_key**: The loaded private key object (`KEYOBJ`), which can be passed directly to signing nodes.

## Additional Considerations

- If using "Best Available" encryption, always use a strong password. The encryption protects the private key, but it is only as strong as the password chosen.
- The `Raw` format with `NoEncryption` stores the key in its most vulnerable state. Use this only when the key will be immediately consumed or stored in a secure environment.
