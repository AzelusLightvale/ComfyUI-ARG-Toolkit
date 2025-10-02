
# Bazeries Cipher

Encrypts or decrypts a message using the Bazeries cipher.

Source library: `secretpy`

## Historical Context

The Bazeries cipher was developed by Étienne Bazeries, a French military cryptanalyst. It is a polyalphabetic substitution cipher that is similar to the Vigenère cipher.

## How it Works

The Bazeries cipher uses a keyword to create a set of mixed alphabets. The plaintext is then encrypted using these alphabets in a periodic manner.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
