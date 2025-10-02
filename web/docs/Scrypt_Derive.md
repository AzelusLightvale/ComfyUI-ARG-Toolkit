# Scrypt Key Derivation

Derives a key from a message using the Scrypt algorithm.

Source library: `cryptography`

## Parameters

- **length**: The desired length of the derived key.
- **message**: The message to derive the key from.
- **salt**: The salt to use for key derivation. Must be a hexadecimal string.
- **n**: The CPU/memory cost parameter.
- **r**: The block size parameter.
- **p**: The parallelization parameter.