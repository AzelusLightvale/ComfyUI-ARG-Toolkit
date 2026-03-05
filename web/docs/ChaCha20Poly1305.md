# ChaCha20-Poly1305 Encryption

Encrypts or decrypts a message using the ChaCha20-Poly1305 authenticated encryption scheme. This node is a wrapper around the `cryptography` library.

Source library: `cryptography`

## Overview

ChaCha20-Poly1305 is an Authenticated Encryption with Associated Data (AEAD) scheme that is fast, secure, and widely adopted in protocols like TLS 1.3 and SSH. It combines the ChaCha20 stream cipher with the Poly1305 message authentication code.

## Parameters

- **text**: The message to encrypt or decrypt. For decryption, this should be a Base64 encoded string.
- **key**: The 32-byte (256-bit) encryption key, as a `BYTESLIKE` object.
- **nonce**: A 12-byte (96-bit) "number used once". It is critical that the nonce is never reused with the same key for different messages.
- **associated_data**: Additional data that is authenticated but not encrypted.
- **mode**: Whether to encrypt or decrypt the message.

## Security Considerations

- **Key Size**: ChaCha20-Poly1305 uses a fixed 256-bit key.
- **Nonce**: The security of ChaCha20-Poly1305 relies heavily on the uniqueness of the nonce for each encryption operation with a given key. Reusing a nonce completely compromises confidentiality and authenticity. A 12-byte nonce is standard.
