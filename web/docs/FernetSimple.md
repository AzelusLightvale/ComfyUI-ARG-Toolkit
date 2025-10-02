# Fernet Symmetric Key Encryption

Encrypts or decrypts a message using the Fernet symmetric key encryption.

Source library: `cryptography`

## Parameters

- **text**: The message to encrypt or decrypt.
- **key**: The encryption key. Must be a 32-byte URL-safe base64-encoded string.
- **mode**: Whether to encrypt or decrypt the message.