
# Trifid Cipher

Encrypts or decrypts a message using the Trifid cipher.

Source library: `secretpy`

## Historical Context

The Trifid cipher is a fractionating transposition cipher invented by Félix Delastelle, the inventor of the Bifid cipher.

## How it Works

The Trifid cipher is similar to the Bifid cipher, but it fractionates each letter into three parts instead of two. It uses a 27-character alphabet and a 3x3x3 cube to represent the letters.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
