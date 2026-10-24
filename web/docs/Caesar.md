# Caesar (ROT) Cipher

Encrypts or decrypts a message using the Caesar cipher.

Source library: `secretpy`

## Historical Context

The Caesar cipher is one of the earliest and most well-known ciphers. It is named after Julius Caesar, who used it to communicate with his generals. It is a simple substitution cipher where each letter in the plaintext is shifted a fixed number of positions down the alphabet.

## How it Works

The Caesar cipher works by shifting each letter in the plaintext by a fixed number of positions. For example, with a shift of 3, 'A' becomes 'D', 'B' becomes 'E', and so on. Decryption is simply shifting back by the same amount.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The shift value for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
