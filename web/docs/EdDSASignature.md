# EdDSA Signature Generator

Generates a digital signature for a message using an EdDSA private key.

Source library: `cryptography`

## Overview

EdDSA (Edwards-curve Digital Signature Algorithm) provides efficient and secure digital signatures. This node signs a message using an EdDSA private key (Ed25519 or Ed448), producing a signature that can be verified later with the corresponding public key.

## Parameters

- **key_type**: The EdDSA curve to use (**Ed25519** or **Ed448**).
- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new, random private key.
    - **From Private Bytes**: Uses a previously serialized private key.
    - **From Loaded Key**: Uses a private key object passed from another node.
- **encoding**: The encoding format for the private key (when `key_source` is "From Private Bytes"). Options: **PEM**, **DER**, **Raw**.
- **formatting**: The key format (when `key_source` is "From Private Bytes"). Options: **PKCS8**, **OpenSSH**, **Raw**.
- **encryption**: How the private key is encrypted (when `key_source` is "From Private Bytes"). Options: **Best Available**, **None**.
- **encryption_password**: (Optional) The password to decrypt the private key, if it was encrypted.
- **private_key**: (Optional) The serialized private key bytes (`BYTESLIKE`). Required when `key_source` is "From Private Bytes".
- **serialized_key**: (Optional) A loaded private key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".
- **data**: The message to sign, as a `BYTESLIKE` object.

## Outputs

- **signature**: The generated signature as a `BYTESLIKE` object.
- **public_key**: The public key corresponding to the private key, as a `KEYOBJ` object. This can be passed to verification nodes.

## Additional Considerations

- **Fresh Key** generates a cryptographically secure random key each time. For production use cases, this is the safest option. However, if you need reproducible signatures for some reason, use either of the existing loading options instead.
- When using **From Private Bytes**, ensure the key bytes are transmitted over a secure channel.
- EdDSA signatures are deterministic for a given key and message, which is a desirable property.
