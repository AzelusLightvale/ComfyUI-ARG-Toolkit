
# Affine Cipher

Encrypts or decrypts a message using the Affine cipher.

Source library: `secretpy`

## Historical Context

The Affine cipher is a type of monoalphabetic substitution cipher. It is a simple mathematical cipher that has been known for centuries.

## How it Works

The Affine cipher uses a pair of keys, (a, b), to encrypt a message. The encryption function is `E(x) = (ax + b) mod m`, where `m` is the size of the alphabet. The decryption function is `D(y) = a^-1(y - b) mod m`, where `a^-1` is the modular multiplicative inverse of `a` modulo `m`.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key_1**: The first key (a) for the cipher. Must be an integer that is relatively prime to the length of the alphabet.
- **key_2**: The second key (b) for the cipher. Must be an integer.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
