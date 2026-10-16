# Elliptic Curve Signature Sign

Generates a digital signature using an EC private key.

Source library: `cryptography`

## Overview

This node signs a message using an ECDSA private key. ECDSA (Elliptic Curve Digital Signature Algorithm) is a widely used standard for digital signatures. The resulting signature can be verified by anyone holding the corresponding public key.

## Parameters

- **private_key**: The EC private key object (`KEYOBJ`), obtained from another node.
- **data**: The message to sign, as a `BYTESLIKE` object.
- **signature_algorithm**: The hash algorithm to use for signing. Options include:
    - **SHA224**, **SHA256**, **SHA384**, **SHA512**, **SHA512_224**, **SHA512_256**
    - **BLAKE2b**, **BLAKE2s**
    - **SHA3_224**, **SHA3_256**, **SHA3_384**, **SHA3_512**
    - **SHA1**, **MD5**, **SM3**
- **prehashed**: (Optional) A `BOOLEAN` that, when `True`, indicates the data has already been hashed. Use this when the input is a pre-computed hash rather than raw data.

## Outputs

- **signature**: The generated signature as a `BYTESLIKE` object.

## Security Considerations

- [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used for new signings that requires security.
- ECDSA signatures are probabilistic — the same key and message produce different signatures each time due to a random nonce. This randomness is essential for security; a deterministic nonce (as in RFC 6979) is not used here, but can be provided later on.
- Ensure the private key is kept secure. A leaked private key allows anyone to forge signatures.
