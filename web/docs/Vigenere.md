
# Vigenere Cipher

Encrypts or decrypts a message using the Vigenere cipher.

Source library: `secretpy`

## Historical Context

The Vigenère cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers, based on the letters of a keyword. It is a form of polyalphabetic substitution.

## How it Works

The Vigenère cipher uses a keyword to shift the letters of the plaintext. Each letter of the keyword determines the shift for the corresponding letter of the plaintext. The encryption is performed using a tabula recta, a square table of alphabets.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
