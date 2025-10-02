
# Nihilist Cipher

Encrypts or decrypts a message using the Nihilist cipher.

Source library: `secretpy`

## Historical Context

The Nihilist cipher was a manually operated symmetric encryption cipher used by Russian Nihilists in the 1880s to organize terrorism against the tsarist regime.

## How it Works

The Nihilist cipher is a polyalphabetic substitution cipher that uses a keyword to create a mixed alphabet. The plaintext is then encrypted using a series of shifts based on the key.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
