# RSA Signature Signer

Generates a digital signature using an RSA private key.

Source library: `cryptography`

## Overview

This node signs a message using an RSA private key. RSA signatures are a widely used standard for digital signatures. The resulting signature can be verified by anyone holding the corresponding public key.

## Parameters

- **private_key**: The RSA private key object (`KEYOBJ`), obtained from another node.
- **data**: The message to sign, as a `BYTESLIKE` object.
- **salt_length**: The length of the salt for PSS padding.
    - **Max Length**: Maximum possible salt length.
    - **Digest Length**: Salt length equal to the hash digest length.
    - **Manual**: Specify a custom salt length.
- **signature_algorithm**: The hash algorithm to use for signing. Options include:
    - **SHA224**, **SHA256**, **SHA384**, **SHA512**, **SHA512_224**, **SHA512_256**
    - **BLAKE2b**, **BLAKE2s**
    - **SHA3_224**, **SHA3_256**, **SHA3_384**, **SHA3_512**
    - **SHA1**, **MD5**, **SM3**
- **padding_alg**: The padding algorithm to use (**PSS** or **PKCS1v15**).
- **salt_length_manual**: (Optional) For PSS padding with `salt_length` set to "Manual", this specifies the salt length.
- **prehashed**: (Optional) A `BOOLEAN` that, when `True`, indicates the data has already been hashed.

## Outputs

- **signature**: The generated signature as a `SIGNATURE` object.

## Security Considerations

- [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used for new signings that requires security.
- PSS (Probabilistic Signature Scheme) is recommended over PKCS1v15 for new applications, as it is provably secure in the random oracle model.
- Ensure the private key is kept secure. A leaked private key allows anyone to forge signatures.
