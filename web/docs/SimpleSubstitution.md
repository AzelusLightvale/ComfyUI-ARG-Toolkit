
# SimpleSubstitution Cipher

Encrypts or decrypts a message using the SimpleSubstitution cipher.

Source library: `secretpy`

## How it Works

The Simple Substitution cipher is a monoalphabetic substitution cipher where each letter of the plaintext is replaced by a corresponding letter of a mixed alphabet. The mixed alphabet is generated from a keyword.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
