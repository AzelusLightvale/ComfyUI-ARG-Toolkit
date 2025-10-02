# AES-based Authenticated Encryption

Encrypts or decrypts a message using an AES-based authenticated encryption.

Source library: `cryptography`

## Parameters

- **text**: The message to encrypt or decrypt.
- **key**: The encryption key. Must be a hexadecimal string of the correct length for the chosen AES type.
- **nonce**: The nonce to use for encryption. Must be a hexadecimal string.
- **associated_data**: Additional data to authenticate.
- **mode**: Whether to encrypt or decrypt the message.
- **aes_type**: The type of AES to use.
- **ccm_tag_length**: The tag length for AES-CCM.