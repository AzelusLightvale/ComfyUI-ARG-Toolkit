
# Zigzag Cipher

Encrypts or decrypts a message using the Zigzag cipher.

Source library: `secretpy`

## How it Works

The Zigzag cipher, also known as the Rail Fence cipher, is a transposition cipher that gets its name from the way the plaintext is written down. The plaintext is written downwards and diagonally on successive "rails" of an imaginary fence, then read off in rows.

## Parameters

- **text**: The message to encrypt or decrypt.
- **key**: The number of rails to use.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
