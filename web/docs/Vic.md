
# Vic Cipher

Encrypts or decrypts a message using the Vic cipher.

Source library: `secretpy`

## Historical Context

The VIC cipher was a pencil and paper cipher used by the Soviet spy Reino Häyhänen, codenamed "VICTOR".

## How it Works

The VIC cipher is a complex transposition and substitution cipher. It involves a straddling checkerboard, a disrupted columnar transposition, and a final substitution.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
