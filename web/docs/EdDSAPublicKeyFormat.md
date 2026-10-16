# EdDSA Public Key Bytes

Serializes an EdDSA public key into bytes.

Source library: `cryptography`

## Overview

This node extracts the public key from an EdDSA private key and serializes it into a byte string. The resulting public key bytes can be shared with others, as public keys are not secret. They are used to verify signatures made by the corresponding private key.

## Parameters

- **key_type**: The EdDSA curve (**Ed25519** or **Ed448**).
- **key_source**: How to obtain the private key.
    - **From Loaded Key**: Uses a private key object passed from another node.
    - **From Private Bytes**: Uses a previously serialized private key.
- **encoding**: The encoding format for the public key. Options: **PEM**, **DER**, **Raw**.
- **formatting**: The key format. Options: **SubjectPublicKeyInfo** (standard), **Raw** (raw key material).
- **private_key**: (Optional) The serialized private key bytes (`BYTESLIKE`). Required when `key_source` is "From Private Bytes".
- **serialized_key**: (Optional) A loaded private key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".

## Outputs

- **public_bytes**: The serialized public key as a `BYTESLIKE` object.
- **public_key**: The public key object (`KEYOBJ`), which can be passed to verification nodes.

## Additional Considerations

- Public keys are not secret and can be freely distributed. They are used only for verification.
- The `Raw` format produces the smallest representation but may be less interoperable with other systems.
