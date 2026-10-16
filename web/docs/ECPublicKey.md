# Elliptic Curve Public Key Bytes

Serializes an EC public key.

Source library: `cryptography`

## Overview

This node extracts the public key from an EC private key and serializes it into bytes. Public keys are not secret and can be freely shared. They are used to verify signatures made by the corresponding private key.

## Parameters

- **key_source**: How to obtain the private key.
    - **Fresh Key**: Generates a new random private key.
    - **From Loaded Key**: Uses a private key object passed from another node.
- **key_type**: The EC curve name (same options as `ECPrivateKey`).
- **encoding**: The encoding format (**PEM** or **DER**).
- **formatting**: The key format.
    - **SubjectPublicKeyInfo** (standard): The standard X.509 format.
    - **Raw**: The raw key point bytes.
- **private_key**: (Optional) The serialized private key bytes. Required when `key_source` is "From Private Bytes".
- **serialized_key**: (Optional) A loaded private key object. Required when `key_source` is "From Loaded Key".

## Outputs

- **public_bytes**: The serialized public key as a `BYTESLIKE` object.
- **public_key**: The public key object (`KEYOBJ`), which can be passed to verification nodes.

## Additional Considerations

- Public keys are safe to distribute. They cannot be used to derive the private key (assuming the curve and implementation are secure).
