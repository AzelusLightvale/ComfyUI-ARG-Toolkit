# RSA Encrypt Data

Encrypts data using an RSA public key.

Source library: `cryptography`

## Overview

This node encrypts data using an RSA public key. RSA encryption is a widely used public-key cryptosystem for secure data transmission. The encrypted data can only be decrypted by the holder of the corresponding private key.

## Parameters

- **public_key**: The RSA public key object (`KEYOBJ`), obtained from another node.
- **data**: The data to encrypt, as a `BYTESLIKE` object.
- **signature_algorithm**: The hash algorithm to use for OAEP padding. Options include:
    - **SHA224**, **SHA256**, **SHA384**, **SHA512**, **SHA512_224**, **SHA512_256**
    - **BLAKE2b**, **BLAKE2s**
    - **SHA3_224**, **SHA3_256**, **SHA3_384**, **SHA3_512**
    - **SHA1**, **MD5**, **SM3**
- **padding_alg**: The padding algorithm to use (**OAEP** or **PKCS1v15**).
- **label**: (Optional) A `BYTESLIKE` label for OAEP padding. This is used to bind the encryption to a specific context.

## Outputs

- **encrypted_data**: The encrypted data as a `BYTESLIKE` object.

## Security Considerations

- RSA encryption is not suitable for encrypting large amounts of data directly due to key size limitations. It is typically used to encrypt a symmetric key, which is then used to encrypt the actual data (hybrid encryption).
- OAEP (Optimal Asymmetric Encryption Padding) is recommended over PKCS1v15 for new applications, as PKCS1v15 is vulnerable to padding oracle attacks.
- [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used.
