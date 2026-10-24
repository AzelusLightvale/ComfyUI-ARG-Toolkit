# Chao Cipher

Encrypts or decrypts a message using the Chao cipher.

Source library: `secretpy`

## Historical Context

The Chao cipher is a cipher method invented by John F. Byrne in 1918. He unsuccessfully tried to interest the US government in it for many years.

## How it Works

The Chao cipher uses two alphabets, which are permuted after each character is encrypted. The encryption process involves finding the plaintext character in one alphabet and the ciphertext character in the other, and then permuting both alphabets.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
