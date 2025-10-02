
# Beaufort Cipher

Encrypts or decrypts a message using the Beaufort cipher.

Source library: `secretpy`

## Historical Context

The Beaufort cipher is a polyalphabetic substitution cipher that is similar to the Vigenère cipher. It was created by Sir Francis Beaufort.

## How it Works

The Beaufort cipher uses a keyword and a tabula recta. The encryption and decryption processes are the same. The ciphertext letter is found at the intersection of the plaintext letter's row and the key letter's column.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
