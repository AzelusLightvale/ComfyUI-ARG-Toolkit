# ML-DSA Message Verification

Verifies an ML-DSA digital signature against a message.

Source library: `cryptography`

## Overview

This node verifies that a signature was legitimately created by the holder of a specific ML-DSA private key. It takes the message, the signature, and the corresponding public key and returns whether the signature is valid. This is the counterpart to the ML-DSA Signature Generator.

## Parameters

- **sig_alg**: The ML-DSA parameter set (**ML-DSA-44**, **ML-DSA-65**, or **ML-DSA-87**).
- **key_source**: How to obtain the public key.
    - **From Private Bytes**: Loads the public key from serialized bytes.
    - **From Loaded Key**: Uses a public key object passed from another node.
- **message**: The original message that was signed, as a `BYTESLIKE` object.
- **signature**: The signature to verify, as a `BYTESLIKE` object.
- **public_bytes**: (Optional) The serialized public key bytes. Required when `key_source` is "From Private Bytes".
- **public_key**: (Optional) A loaded public key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".
- **context**: (Optional) A `BYTESLIKE` context string, up to 255 bytes. Must match the context used during signing.

## Outputs

- **verify_status**: A `BOOLEAN` that is `True` if the signature is valid for the given message and public key, and `False` otherwise.

## Additional Considerations

- Always verify signatures using a trusted public key. If an attacker can provide the public key, they can forge signatures.
- Verification is the essential step in ensuring that a message has not been tampered with and genuinely came from the claimed sender.
- The context string must match what was used during signing, otherwise verification will fail.
