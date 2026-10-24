# ML-DSA Signature Generator

Generates a digital signature for a message using an ML-DSA private key.

Source library: `cryptography`

## Overview

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) is a post-quantum digital signature scheme. This node signs a message using an ML-DSA private key, producing a signature that can be verified later with the corresponding public key.

## Parameters

- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new, random private key.
    - **From Private Bytes**: Uses a previously serialized private key.
    - **From Loaded Key**: Uses a private key object passed from another node.
- **sig_alg**: The ML-DSA parameter set (**ML-DSA-44**, **ML-DSA-65**, or **ML-DSA-87**).
- **message**: The message to sign, as a `BYTESLIKE` object.
- **encoding**: The encoding format for the private key (when `key_source` is "From Private Bytes"). Options: **PEM**, **DER**, **Raw**.
- **formatting**: The key format (when `key_source` is "From Private Bytes"). Options: **PKCS8**, **Raw**.
- **encryption**: How the private key is encrypted (when `key_source` is "From Private Bytes"). Options: **Best Available**, **None**.
- **encryption_password**: (Optional) The password to decrypt the private key, if it was encrypted.
- **private_bytes**: (Optional) The serialized private key bytes (`BYTESLIKE`). Required when `key_source` is "From Private Bytes".
- **private_key**: (Optional) A loaded private key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".
- **context**: (Optional) A `BYTESLIKE` context string, up to 255 bytes. This is additional data that is bound to the signature.

## Outputs

- **signature**: The generated signature as a `BYTESLIKE` object.

## Additional Considerations

- **Fresh Key** generates a cryptographically secure random key each time. For production use cases, this is the safest option.
- When using **From Private Bytes**, ensure the key bytes are transmitted over a secure channel.
- ML-DSA signatures are deterministic for a given key and message, which is a desirable property.
