# Rotor Machine Encrypt/Decrypt

Encrypts or decrypts a message using a rotor machine.

Source: Native Python

## Overview

This node runs a message through a configured rotor machine, performing either encryption or decryption. The machine's stepping mechanism is applied after each character, causing the rotors to turn and produce a different substitution for each subsequent letter.

## Parameters

- **machine**: A `MACHINE` object from the Rotor Machine State node. Required.
- **positions**: A `POSITIONS` object from the Rotor Machine Positions node. Required.
- **text**: The message to encrypt or decrypt. Default is `Hello World!`.
- **preserve**: When `True`, attempts to preserve the form of the message, including case and punctuation marks. Default is `False`.
- **mode**: Toggle between `Encrypt` (default) and `Decrypt`.

## Outputs

- **encrypted_msg**: The resulting ciphertext (on encryption) or plaintext (on decryption) as a `STRING`.
- **rotor_pos**: The final rotor positions after the operation, as a `POSITIONS` object. This can be used to resume encryption from where you left off.

## Additional Considerations

- The alphabets must be uppercase/uncased - the node case-folds input.
- When `preserve` is `True`, characters not in the alphabet are passed through unchanged, and case is preserved.
- For decryption, the machine must be configured with the same settings used during encryption, and the rotor positions must be reset to the original starting positions.
