# RSA Public Key Bytes

Serializes an RSA public key.

Source library: `cryptography`

## Overview

This node extracts the public key from an RSA private key and serializes it into bytes. Public keys are not secret and can be freely shared. They are used to verify signatures made by the corresponding private key or to encrypt data.

## Parameters

- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new random private key.
    - **From Loaded Key**: Uses a private key object passed from another node.
- **encoding**: The encoding format for the public key (**PEM** or **DER**).
- **formatting**: The key format.
    - **SubjectPublicKeyInfo**: The standard X.509 format.
    - **PKCS1**: The older PKCS#1 format.
- **serialized_key**: (Optional) A loaded private key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".
- **fresh_key_size**: (Optional) The key size in bits. Required when `key_source` is "Fresh Key".
- **public_exponent**: (Optional) The public exponent. Required when `key_source` is "Fresh Key".

## Outputs

- **key_object**: The public key object (`KEYOBJ`), which can be passed to verification and encryption nodes.
- **public_key**: The serialized public key as a `BYTESLIKE` object.
- **public_numbers**: The public key numbers as a `NUMOBJ` object.

## Additional Considerations

- Public keys are safe to distribute. They cannot be used to derive the private key (assuming the implementation is secure).
