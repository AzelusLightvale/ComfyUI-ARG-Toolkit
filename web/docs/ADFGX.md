
# ADFGX Cipher

Encrypts or decrypts a message using the ADFGX cipher.

Source library: `secretpy`

## Historical Context

The ADFGX cipher was a field cipher used by the German Army during World War I. It was an extension of the earlier ADFG cipher and was designed to be more secure. The name comes from the five possible letters used in the ciphertext: A, D, F, G, and X.

## How it Works

The ADFGX cipher is a fractionating transposition cipher. It combines a Polybius square with a single columnar transposition. The letters of the plaintext are first replaced by their coordinates in the Polybius square, and then the resulting string of letters is written out in a grid and transposed by columns.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
