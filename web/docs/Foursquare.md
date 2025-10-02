
# Foursquare Cipher

Encrypts or decrypts a message using the Foursquare cipher.

Source library: `secretpy`

## Historical Context

The Foursquare cipher is a polygraphic substitution cipher invented by the British cryptographer Lyon Playfair. It is a more secure version of the Playfair cipher.

## How it Works

The Foursquare cipher uses four 5x5 Polybius squares to encrypt pairs of letters. Two of the squares contain the standard alphabet, and the other two contain mixed alphabets based on keywords.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key_1**: The first key for the cipher.
- **key_2**: The second key for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
