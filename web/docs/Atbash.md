
# Atbash Cipher

Encrypts or decrypts a message using the Atbash cipher.

Source library: `secretpy`

## Historical Context

The Atbash cipher is a simple substitution cipher originally used for the Hebrew alphabet. It is one of the earliest known ciphers and is mentioned in the Bible.

## How it Works

The Atbash cipher works by reversing the alphabet. The first letter of the alphabet is replaced by the last letter, the second letter by the second-to-last, and so on.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
