# PEM Serialized Private Key Loader

Loads a private key from a PEM-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a private key that has been serialized in PEM (Privacy-Enhanced Mail) format. PEM is a widely used, text-based format for storing cryptographic keys, recognizable by its `-----BEGIN` and `-----END` headers. The loaded key can then be used by signing or encryption nodes.

## Parameters

- **keyfile**: The PEM-encoded private key data, as a `BYTESLIKE` object.
- **password**: (Optional) The password used to decrypt the key, as a `BYTESLIKE` object. Required if the key was encrypted during serialization.

## Outputs

- **loaded_key**: The loaded private key object (`KEYOBJ`), ready for use with signing and decryption nodes.

## Additional Considerations

- If the key is encrypted, the password must be provided. The password itself should be transmitted securely.
- This node supports all key types that the `cryptography` library can load via `load_pem_private_key`, including RSA, EC, EdDSA, and X25519/X448 keys.
- PEM keys are human-readable and widely interoperable, but they are not encrypted by default. Always encrypt private keys before storing them long-term.
