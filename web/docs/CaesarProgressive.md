# CaesarProgressive Cipher

Encrypts or decrypts a message using the Caesar Progressive cipher.

Source library: `secretpy`

## How it Works

The Caesar Progressive cipher is a variation of the Caesar cipher. Instead of a fixed shift, the shift value increases for each letter of the plaintext. The initial shift is determined by the key.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The initial shift for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
