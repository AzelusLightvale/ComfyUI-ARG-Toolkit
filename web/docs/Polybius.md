
# Polybius Cipher

Encrypts or decrypts a message using the Polybius cipher.

Source library: `secretpy`

## Historical Context

The Polybius square, also known as the Polybius checkerboard, is a device invented by the ancient Greeks Cleoxenus and Democleitus, and made famous by the historian and scholar Polybius.

## How it Works

The Polybius cipher is a substitution cipher that uses a grid to represent the letters of the alphabet. Each letter is replaced by its coordinates in the grid.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
