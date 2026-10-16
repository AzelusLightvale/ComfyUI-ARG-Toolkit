# Elliptic Curve Signature Verify

Verifies an ECDSA digital signature.

Source library: `cryptography`

## Overview

This node verifies that a signature was legitimately created by the holder of a specific EC private key. It takes the message, the signature, the public key, and the hash algorithm used during signing, and returns whether the signature is valid.

## Parameters

- **public_key**: The EC public key object (`KEYOBJ`), obtained from another node.
- **signature**: The signature to verify, as a `BYTESLIKE` object.
- **data**: The original message that was signed, as a `BYTESLIKE` object.
- **signature_algorithm**: The hash algorithm that was used during signing. Must match the algorithm used by the signer. Options include:
    - **SHA224**, **SHA256**, **SHA384**, **SHA512**, **SHA512_224**, **SHA512_256**
    - **BLAKE2b**, **BLAKE2s**
    - **SHA3_224**, **SHA3_256**, **SHA3_384**, **SHA3_512**
    - **SHA1**, **MD5**, **SM3**
- **prehashed**: (Optional) A `BOOLEAN` that, when `True`, indicates the data is a pre-computed hash.

## Outputs

- **verification**: A `BOOLEAN` that is `True` if the signature is valid, and `False` otherwise.

## Additional Considerations

- Always verify signatures using a trusted public key. If an attacker can supply the public key, they can forge signatures.
- The hash algorithm must match what was used during signing. Using a mismatched algorithm will always result in verification failure.
- [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used for new verification that requires security.
