
# Gronsfeld Cipher

Encrypts or decrypts a message using the Gronsfeld cipher.

Source library: `secretpy`

## Historical Context

The Gronsfeld cipher is a polyalphabetic substitution cipher that is a variation of the Vigenère cipher. It was created by Count Gronsfeld, a German diplomat.

## How it Works

The Gronsfeld cipher uses a numeric key instead of a keyword. Each digit of the key determines the shift for the corresponding letter of the plaintext.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
