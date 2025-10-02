
# Keyword Cipher

Encrypts or decrypts a message using the Keyword cipher.

Source library: `secretpy`

## How it Works

The Keyword cipher is a type of monoalphabetic substitution cipher. A keyword is used to create a mixed alphabet, which is then used to encrypt the message.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
