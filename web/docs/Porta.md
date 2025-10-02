
# Porta Cipher

Encrypts or decrypts a message using the Porta cipher.

Source library: `secretpy`

## Historical Context

The Porta cipher is a polyalphabetic substitution cipher invented by Giovanni Battista della Porta.

## How it Works

The Porta cipher is a reciprocal cipher, meaning that the encryption and decryption processes are the same. It uses a keyword and a set of rotating alphabets to encrypt the message.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
