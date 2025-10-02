
# Bifid Cipher

Encrypts or decrypts a message using the Bifid cipher.

Source library: `secretpy`

## Historical Context

The Bifid cipher is a fractionating transposition cipher invented by Félix Delastelle. It combines a Polybius square with transposition.

## How it Works

The Bifid cipher uses a Polybius square to convert each letter of the plaintext into two coordinates. The coordinates are then written out in two rows, and the ciphertext is formed by reading the coordinates row by row.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
