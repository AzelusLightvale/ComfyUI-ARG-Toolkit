
# Playfair Cipher

Encrypts or decrypts a message using the Playfair cipher.

Source library: `secretpy`

## Historical Context

The Playfair cipher was the first practical digraph substitution cipher. It was invented in 1854 by Charles Wheatstone, but was named after Lord Playfair who promoted its use.

## How it Works

The Playfair cipher uses a 5x5 grid of letters, based on a keyword, to encrypt pairs of letters (digraphs). The encryption rules are based on the relative positions of the two letters in the grid.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
