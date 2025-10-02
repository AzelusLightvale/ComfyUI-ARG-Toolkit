
# ADFGVX Cipher

Encrypts or decrypts a message using the ADFGVX cipher.

Source library: `secretpy`

## Historical Context

The ADFGVX cipher was a field cipher used by the German Army during World War I. It was a further development of the ADFGX cipher, adding the letter V to the set of possible ciphertext letters. This allowed for the inclusion of digits in the plaintext.

## How it Works

The ADFGVX cipher is a fractionating transposition cipher, similar to the ADFGX cipher. It uses a 6x6 Polybius square to accommodate the 26 letters of the alphabet and the 10 digits. The plaintext is first converted to its coordinates in the Polybius square, and then the resulting string of letters is written out in a grid and transposed by columns.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
