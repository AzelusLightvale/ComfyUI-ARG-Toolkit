
# Symmetrical Encrypt/Decrypt

Encrypts or decrypts a message using a symmetrical cipher. This node is a wrapper around the `cryptography` library.

Source library: `cryptography`

## Parameters

- **text**: The message to encrypt or decrypt.
- **key**: The encryption key. Must be a hexadecimal string of the correct length for the chosen algorithm.
- **iv**: The initialization vector. Must be a hexadecimal string. For XTS mode, this is the `tweak`.
- **algorithm**: The symmetrical algorithm to use.
- **modes**: The mode of operation for the cipher.
- **mode**: Whether to encrypt or decrypt the message.
- **tag**: The tag bytes to verify during decryption. Exclusively for GCM mode.
- **min_tag_length**: The minimum length of the tag. Exclusively for GCM mode.
- **nonce**: A random nonce to instantiate from. Currently only for ChaCha20.

## Algorithm and Mode Compatibility Matrix

The following table shows the compatibility between the available algorithms and modes.

| Algorithm | CBC | CTR | OFB | CFB | CFB8 | GCM | XTS | ECB | None |
| :-------- | :-: | :-: | :-: | :-: | :--: | :-: | :-: | :-: | :--: |
| AES       |  ✔  |  ✔  |  ✔  |  ✔  |  ✔   |  ✔  |  ✔  |  ✔  |  ❌  |
| AES128    |  ✔  |  ✔  |  ✔  |  ✔  |  ✔   |  ✔  |  ✔  |  ✔  |  ❌  |
| AES256    |  ✔  |  ✔  |  ✔  |  ✔  |  ✔   |  ✔  |  ✔  |  ✔  |  ❌  |
| Camellia  |  ✔  |  ✔  |  ✔  |  ✔  |  ✔   | ❌  | ❌  |  ✔  |  ❌  |
| ChaCha20  | ❌  | ❌  | ❌  | ❌  |  ❌  | ❌  | ❌  | ❌  |  ✔   |
| TripleDES |  ✔  |  ✔  |  ✔  |  ✔  |  ✔   | ❌  | ❌  |  ✔  |  ❌  |
| SM4       |  ✔  |  ✔  |  ✔  |  ✔  |  ❌  | ❌  | ❌  |  ✔  |  ❌  |
| ARC4      | ❌  | ❌  | ❌  | ❌  |  ❌  | ❌  | ❌  | ❌  |  ✔   |
| Blowfish  |  ✔  |  ✔  |  ✔  |  ✔  |  ❌  | ❌  | ❌  |  ✔  |  ❌  |
| CAST5     |  ✔  |  ✔  |  ✔  |  ✔  |  ❌  | ❌  | ❌  |  ✔  |  ❌  |
| SEED      |  ✔  |  ✔  |  ✔  |  ✔  |  ❌  | ❌  | ❌  |  ✔  |  ❌  |
| IDEA      |  ✔  |  ✔  |  ✔  |  ✔  |  ❌  | ❌  | ❌  |  ✔  |  ❌  |

**Notes:**

- The compatibility is based on the `cryptography` library. Please refer to the official documentation for the most accurate information.

- AES-XTS requires a double-length key (e.g., 256-bit key for XTS-AES-128 and 512-bit key for XTS-AES-256).

- Stream ciphers (ChaCha20, ARC4) do not use modes, so None is the only valid choice.

- GCM only works with AES.

- CBC/ECB block modes require padding.

- ECB is insecure but technically valid.

## Key and IV sizes

The required key and IV sizes depend on the selected algorithm and mode. Please refer to the `cryptography` library documentation for the specific requirements.
