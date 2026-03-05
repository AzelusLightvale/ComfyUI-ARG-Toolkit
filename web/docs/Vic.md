# Vic Cipher

Encrypts or decrypts a message using the Vic cipher.

Source library: `secretpy`

## Historical Context

The VIC cipher was a pencil and paper cipher used by the Soviet spy Reino Häyhänen, codenamed "VICTOR".

## How it Works

The VIC cipher is notoriously complex for a pencil-and-paper cipher, making it very secure for its time. It is a "bifid" cipher, meaning it splits each plaintext character into two parts, shuffles them, and then reassembles them. The main steps are:

1.  **Key Generation**: A complex series of steps using a passphrase, a date, and a personal number generates the keys for the subsequent steps.
2.  **Straddling Checkerboard**: A modified Polybius square is used to convert letters into single or double-digit numbers.
3.  **Double Transposition**: The sequence of numbers is then put through two successive columnar transpositions, which are "disrupted" or made irregular by the key generation process.
4.  **Chain Addition**: The final step involves a form of substitution where each number in the transposed sequence is added (without carrying) to the previous number in the sequence, creating the final ciphertext digits.

Decryption involves reversing these steps, which is just as complex.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
