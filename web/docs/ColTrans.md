
# ColTrans Cipher

Encrypts or decrypts a message using the ColTrans cipher.

Source library: `secretpy`

## How it Works

The ColTrans (Columnar Transposition) cipher is a transposition cipher that involves writing the plaintext in a grid and then reading the ciphertext out column by column. The order of the columns is determined by a keyword.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
