# MyszkowskiTransposition Cipher

Encrypts or decrypts a message using the Myszkowski Transposition cipher.

Source library: `secretpy`

## Historical Context

The Myszkowski transposition cipher is a variant of the columnar transposition cipher. It was invented by Émile Victor Théodore Myszkowski.

## How it Works

The Myszkowski transposition cipher is similar to the columnar transposition cipher, but with a modification in how repeated letters in the key are handled. This creates a more irregular transposition.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
