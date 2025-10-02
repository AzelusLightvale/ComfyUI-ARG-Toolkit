# PBKDF2HMAC Key Verification

Verifies a key derived from a message using the PBKDF2HMAC algorithm.

Source library: `cryptography`

## Parameters

- **length**: The desired length of the derived key.
- **message**: The message to derive the key from.
- **salt**: The salt to use for key derivation. Must be a hexadecimal string.
- **algorithm**: The HMAC algorithm to use.
- **iterations**: The number of iterations to use.
- **expected_key**: The expected derived key.