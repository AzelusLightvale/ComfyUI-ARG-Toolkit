
# Scytale Cipher

Encrypts or decrypts a message using the Scytale cipher.

Source library: `secretpy`

## Historical Context

The Scytale cipher is a transposition cipher used by the ancient Greeks. It consisted of a cylinder with a strip of parchment wound around it, on which a message was written.

## How it Works

The Scytale cipher works by writing the plaintext along the length of the cylinder, and then unwrapping the parchment. The ciphertext is the sequence of letters on the unwrapped parchment. To decrypt, the parchment is wrapped around a cylinder of the same diameter.

## Parameters

- **text**: The message to encrypt or decrypt.
- **alphabet**: The alphabet to use for the cipher. Can be a string of characters or a predefined alphabet from `secretpy.alphabets`.
- **key**: The diameter of the Scytale.
- **mode**: Whether to encrypt or decrypt the message.
- **keep_formatting**: Whether to keep the original formatting of the message.
