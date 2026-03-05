# Foursquare Cipher

Encrypts or decrypts a message using the Foursquare cipher.

Source library: `secretpy`

## Historical Context

The Foursquare cipher is a polygraphic substitution cipher, meaning it encrypts pairs of letters (digraphs) at a time. It is considered an improvement on the related Playfair cipher, as it is slightly more complex and resistant to frequency analysis. While sometimes attributed to Lyon Playfair, it was actually introduced by the Swiss cryptographer Felix Delastelle.

## How it Works

The cipher uses four 5x5 Polybius squares arranged in a larger 2x2 grid.

1.  **The Squares**:
    - The top-left and bottom-right squares contain the standard alphabet (with I/J combined).
    - The top-right and bottom-left squares contain mixed alphabets generated from two secret keywords.

2.  **Encryption**: To encrypt a pair of letters (a digraph), say 'ab':
    - Find the first letter 'a' in the top-left (plain) square.
    - Find the second letter 'b' in the bottom-right (plain) square.
    - These two letters define a rectangle. The encrypted pair is formed by the letters at the other two corners of this rectangle, taking the letter from the top-right square first, followed by the letter from the bottom-left square.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key_1**: The keyword for the top-right mixed alphabet square.
- **key_2**: The keyword for the bottom-left mixed alphabet square.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
