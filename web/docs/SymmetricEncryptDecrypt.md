# Symmetric Encrypt/Decrypt

Encrypts or decrypts data using a variety of standard symmetric ciphers and modes. This node is a wrapper around the `cryptography` library.

Source library: `cryptography`

## Overview

This is a flexible, general-purpose node for performing symmetric encryption. It allows you to choose from a wide range of algorithms (like AES, ChaCha20) and modes of operation (like CBC, GCM, CTR) to fit different cryptographic needs.

## Parameters

- **text**: The `BYTESLIKE` data to be encrypted or decrypted.
- **key**: The encryption key as a `BYTESLIKE` object. The required size depends on the chosen algorithm.
- **iv**: The initialization vector or nonce as a `BYTESLIKE` object. For XTS mode, this is the `tweak`. Not used by all algorithms/modes (e.g., ECB, stream ciphers).
- **algorithm**: The symmetric algorithm to use (e.g., `AES`, `ChaCha20`, `TripleDES`).
- **modes**: The cipher mode of operation (e.g., `CBC`, `GCM`, `CTR`).
- **algorithm**: The symmetric algorithm to use (e.g., `AES`, `ChaCha20`). Several legacy algorithms like `TripleDES` and `Blowfish` are supported but considered deprecated.
- **modes**: The cipher mode of operation (e.g., `CBC`, `GCM`, `CTR`). Legacy modes like `OFB` and `CFB` are supported but considered deprecated.
- **mode**: Toggles between `Encrypt` and `Decrypt`.
- **tag**: (Optional) For GCM decryption, this is the `BYTESLIKE` authentication tag that must be provided to verify the ciphertext's integrity and authenticity.
- **min_tag_length**: (Optional) For GCM, the minimum acceptable tag length during decryption.
- **nonce**: (Optional) A `BYTESLIKE` nonce, used specifically for `ChaCha20` in this implementation.

## Outputs

- **output**: The resulting ciphertext (on encryption) or plaintext (on decryption) as a `BYTESLIKE` object.
- **tag**: When using GCM mode for encryption, this output provides the generated authentication tag as a `BYTESLIKE` object. This tag is required for decryption.

## Algorithm and Mode Compatibility

The `cryptography` library will raise an error if an incompatible algorithm and mode are selected. The following table provides a general guide.
The `cryptography` library will raise an error if an incompatible algorithm and mode are selected. The following table provides a general guide. Items marked with **(D)** are deprecated according to the `cryptography` library and should be avoided for new projects.

| Algorithm      | CBC | CTR |   OFB   |   CFB   |   CFB8   | GCM | XTS | ECB | None |
| :------------- | :-: | :-: | :-----: | :-----: | :------: | :-: | :-: | :-: | :--: |
| AES            |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| AES128         |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| AES256         |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| Camellia       |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     | ❌  | ❌  |  ✔  |  ❌  |
| ChaCha20       | ❌  | ❌  |   ❌    |   ❌    |    ❌    | ❌  | ❌  | ❌  |  ✔   |
| TripleDES      |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     | ❌  | ❌  |  ✔  |  ❌  |
| SM4            |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| ARC4           | ❌  | ❌  |   ❌    |   ❌    |    ❌    | ❌  | ❌  | ❌  |  ✔   |
| Blowfish       |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| CAST5          |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| SEED           |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| IDEA           |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| Algorithm      | CBC | CTR | OFB (D) | CFB (D) | CFB8 (D) | GCM | XTS | ECB | None |
| :------------- | :-: | :-: | :-----: | :-----: | :------: | :-: | :-: | :-: | :--: |
| AES            |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| AES128         |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| AES256         |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     |  ✔  |  ✔  |  ✔  |  ❌  |
| Camellia       |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     | ❌  | ❌  |  ✔  |  ❌  |
| ChaCha20       | ❌  | ❌  |   ❌    |   ❌    |    ❌    | ❌  | ❌  | ❌  |  ✔   |
| TripleDES (D)  |  ✔  |  ✔  |    ✔    |    ✔    |    ✔     | ❌  | ❌  |  ✔  |  ❌  |
| SM4            |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| ARC4 (D)       | ❌  | ❌  |   ❌    |   ❌    |    ❌    | ❌  | ❌  | ❌  |  ✔   |
| Blowfish (D)   |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| CAST5 (D)      |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| SEED (D)       |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |
| IDEA (D)       |  ✔  |  ✔  |    ✔    |    ✔    |    ❌    | ❌  | ❌  |  ✔  |  ❌  |

**Notes:**

- **Key/IV Types**: All key and IV inputs must be `BYTESLIKE` objects of the correct length for the chosen algorithm/mode. Use the `Random Nonce Generator` node to create secure random values.
- **Stream Ciphers**: Stream ciphers like `ChaCha20` and `ARC4` do not use a block mode; select `None`.
- **GCM**: GCM is an authenticated mode and only works with AES in this implementation. It provides both confidentiality and integrity.
- **ECB**: Electronic Codebook mode is insecure for most uses and should be avoided. It does not use an IV.
- **Padding**: Block ciphers in modes like CBC and ECB require padding to handle messages that are not a multiple of the block size. The `cryptography` library handles this automatically.

**Deprecation Warning:**
As of `cryptography` 47.0.0, several legacy primitives were moved to a `decrepit` module. This includes algorithms like `ARC4`, `Blowfish`, `CAST5`, `IDEA`, `SEED`, and `TripleDES`, as well as modes like `OFB`, `CFB`, and `CFB8`. These are considered insecure or sub-optimal and are only provided for compatibility with legacy systems. Users are encouraged to use **AES** (with **GCM** or **CTR** mode) or **ChaCha20** for modern applications. For more information, check the latest documentations over at [https://cryptography.io/en/47.0.0/](https://cryptography.io/en/47.0.0/).
