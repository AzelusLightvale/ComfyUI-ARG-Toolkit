# EdDSA Private Key Bytes

Generates a new EdDSA private key and serializes it into bytes.

Source library: `cryptography`

## Overview

EdDSA (Edwards-curve Digital Signature Algorithm) is a modern, high-performance digital signature scheme. This node generates a new private key for either the Ed25519 or Ed448 curve and serializes it into a byte string in the chosen encoding and format. The key can optionally be encrypted with a password.

## Parameters

- **key_type**: The EdDSA curve to use.
    - **Ed25519**: A highly efficient, widely adopted curve.
    - **Ed448**: A newer curve offering different security/performance characteristics.
- **encoding**: The encoding format for the serialized key.
    - **PEM**: Privacy-Enhanced Mail format (human-readable, with headers).
    - **DER**: Distinguished Encoding Rules (binary format).
    - **Raw**: The raw key bytes without any wrapping.
- **formatting**: The key format to serialize in.
    - **PKCS8**: Standard format for private keys.
    - **OpenSSH**: OpenSSH private key format. Only available for Ed25519 and requires PEM encoding.
    - **Raw**: The raw key material.
- **encryption**: How to encrypt the private key.
    - **Best Available**: Encrypts the key using the best available algorithm (requires `encryption_password`).
    - **None**: Stores the key unencrypted.
- **encryption_password**: (Optional) The password to use for encrypting the private key. Required when `encryption` is set to "Best Available".

## Outputs

- **private_bytes**: The serialized private key as a `BYTESLIKE` object.
- **private_key**: The loaded private key object (`KEYOBJ`), which can be passed directly to signing nodes.

## Additional Considerations

- If using "Best Available" encryption, always use a strong password. The encryption protects the private key, but it is only as strong as the password chosen.
- The `Raw` format with `NoEncryption` stores the key in its most vulnerable state. Use this only when the key will be immediately consumed or stored in a secure environment.
