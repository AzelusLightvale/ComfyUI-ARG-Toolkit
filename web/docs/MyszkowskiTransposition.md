# MyszkowskiTransposition Cipher

Encrypts or decrypts a message using the Myszkowski Transposition cipher.

Source library: `secretpy`

## Historical Context

The Myszkowski transposition cipher is a variant of the columnar transposition cipher. It was invented by Émile Victor Théodore Myszkowski.

## How it Works

The Myszkowski transposition is a variant of the standard columnar transposition cipher.

1.  A keyword is chosen, and its letters are numbered based on their alphabetical order. Unlike a standard columnar transposition, **repeated letters in the key are given the same number**.
2.  The plaintext is written out in rows under the keyword.
3.  The columns are then read off to form the ciphertext.
4.  Columns corresponding to letters that appear only once in the key are read top-to-bottom, in the order of their number.
5.  Columns corresponding to repeated letters in the key are read differently. For a given repeated letter (e.g., the two 'O's in `TOMATO`), the corresponding columns are read from left to right, one row at a time. This is done for each set of repeated letters, in the order of their number.

This handling of repeated letters is the defining characteristic of the Myszkowski cipher and distinguishes it from a simple columnar transposition.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
