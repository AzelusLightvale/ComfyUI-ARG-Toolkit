# ChaCha20Poly1305 Encryption

Encrypts or decrypts a message using the ChaCha20Poly1305 authenticated encryption.

Source library: `cryptography`

## Parameters

- **text**: The message to encrypt or decrypt.
- **key**: The encryption key. Must be a 32-byte hexadecimal string.
- **nonce**: The nonce to use for encryption. Must be a 12-byte hexadecimal string.
- **associated_data**: Additional data to authenticate.
- **mode**: Whether to encrypt or decrypt the message.