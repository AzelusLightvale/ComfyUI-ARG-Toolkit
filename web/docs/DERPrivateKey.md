# DER Serialized Private Key Loader

Loads a private key from a DER-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a private key that has been serialized in DER (Distinguished Encoding Rules) format. DER is a binary, compact format commonly used in X.509 certificates and hardware security modules. It is less human-readable than PEM but more compact.

## Parameters

- **keyfile**: The DER-encoded private key data, as a `BYTESLIKE` object.
- **password**: (Optional) The password used to decrypt the key, as a `BYTESLIKE` object. Required if the key was encrypted during serialization.

## Outputs

- **loaded_key**: The loaded private key object (`KEYOBJ`), ready for use with signing and decryption nodes.

## Additional Considerations

- DER is a binary format and is not human-readable. It is commonly used in certificate files and hardware tokens.
- This node supports all key types loadable via `load_der_private_key`, including RSA, EC, EdDSA, and X25519/X448 keys.
- DER-encoded private keys should still be encrypted when stored, as they contain sensitive key material.
