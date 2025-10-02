# TwoSquare Cipher

Encrypts or decrypts a message using the Two Square cipher.

Source library: `secretpy`

## How it Works

The Two Square cipher, also known as the Double Playfair cipher, is a polygraphic substitution cipher that is a variation of the Playfair cipher. It uses two 5x5 Polybius squares to encrypt pairs of letters.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key_1**: The first key for the cipher.
- **key_2**: The second key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
