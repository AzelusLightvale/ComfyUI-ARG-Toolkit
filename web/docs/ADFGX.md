# ADFGX Cipher

Encrypts or decrypts a message using the ADFGX cipher.

Source library: `secretpy`

## Historical Context

The ADFGX cipher was a field cipher used by the German Army on the Western Front during World War I. It was an improvement on an earlier cipher, ADFG. The name comes from the five possible letters used in the ciphertext: A, D, F, G, and X. These letters were chosen because their Morse code representations are very different from each other, reducing the risk of transmission errors. The cipher was famously broken by French cryptanalyst Georges Painvin, which provided crucial intelligence to the Allies.

## How it Works

The ADFGX cipher is a fractionating transposition cipher that combines a Polybius square with a columnar transposition.

1.  **Substitution**: A 5x5 Polybius square is created, usually filled with a mixed alphabet based on a keyword. The letters 'I' and 'J' are typically combined to fit the 25-character grid. Each letter of the plaintext is replaced by its two-letter coordinate from the square (one of A, D, F, G, X for the row and one for the column).

    _Example_: If 'p' is at row F, column G, it is replaced by "FG".

2.  **Transposition**: The long string of coordinate letters is written into a grid, with the width of the grid determined by the length of a second keyword. The columns of this grid are then reordered alphabetically based on the letters of the keyword.

3.  **Ciphertext**: The final ciphertext is produced by reading the letters down the reordered columns.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
