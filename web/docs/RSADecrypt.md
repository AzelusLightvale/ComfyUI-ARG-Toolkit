# RSA Decrypt Data

Decrypts data using an RSA private key.

Source library: `cryptography`

## Overview

This node decrypts data that was encrypted using an RSA public key. It takes the encrypted data and the corresponding private key and returns the original plaintext.

## Parameters

- **private_key**: The RSA private key object (`KEYOBJ`), obtained from another node.
- **data**: The encrypted data to decrypt, as a `BYTESLIKE` object.
- **signature_algorithm**: The hash algorithm that was used during encryption. Must match the algorithm used by the encryptor. Options include:
    - **SHA224**, **SHA256**, **SHA384**, **SHA512**, **SHA512_224**, **SHA512_256**
    - **BLAKE2b**, **BLAKE2s**
    - **SHA3_224**, **SHA3_256**, **SHA3_384**, **SHA3_512**
    - **SHA1**, **MD5**, **SM3**
- **padding_alg**: The padding algorithm that was used during encryption (**OAEP** or **PKCS1v15**).
- **label**: (Optional) A `BYTESLIKE` label for OAEP padding. Must match the label used during encryption.

## Outputs

- **decrypted_data**: The decrypted data as a `BYTESLIKE` object.

## Additional Considerations

- The hash algorithm and padding algorithm must match what was used during encryption. Using a mismatched algorithm will result in decryption failure.
- [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used.
- Always keep the private key secure. A leaked private key allows anyone to decrypt data intended for you.
