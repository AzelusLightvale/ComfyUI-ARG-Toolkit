# AES-based Authenticated Encryption

Encrypts or decrypts a message using an AES-based authenticated encryption scheme. This node is a wrapper around the `cryptography` library.

Source library: `cryptography`

## Overview

Authenticated Encryption with Associated Data (AEAD) is a form of encryption which simultaneously provides confidentiality, integrity, and authenticity assurances on the data. This node provides access to several common AEAD schemes based on AES.

## Parameters

- **text**: The message to encrypt or decrypt. For decryption, this should be a Base64 encoded string representing the ciphertext.
- **key**: The encryption key. Must be a `BYTESLIKE` object. The required length depends on the chosen AES type.
- **nonce**: A "number used once". A random value that is required for most modes. Should be 12 bytes for GCM, GCM-SIV, OCB3, and CCM. For AES-SIV, this is part of the associated data.
- **associated_data**: Additional data that is authenticated but not encrypted.
- **mode**: Whether to encrypt or decrypt the message.
- **aes_type**: The AES authenticated encryption mode to use.
    - **AES-GCM**: Galois/Counter Mode. A widely used mode of operation.
    - **AES-GCM-SIV**: A variant of GCM that is resistant to nonce misuse.
    - **AES-OCB3**: Offset Codebook Mode. A high-performance AEAD mode. It is patent-encumbered, so use with caution in commercial applications.
    - **AES-SIV**: Synthetic Initialization Vector. Can be used when it is not possible to generate a unique nonce for each message.
    - **AES-CCM**: Counter with CBC-MAC. An AEAD mode used in standards like Wi-Fi.
- **ccm_tag_length**: (Optional) For AES-CCM only. The length of the authentication tag in bytes.

## Key Sizes

| AES Type    | Supported Key Sizes (bits) |
| :---------- | :------------------------- |
| AES-GCM     | 128, 192, 256              |
| AES-GCM-SIV | 128, 192, 256              |
| AES-OCB3    | 128, 192, 256              |
| AES-SIV     | 256, 384, 512              |
| AES-CCM     | 128, 192, 256              |

**Note:** For AES-SIV, the key is split internally into two keys (one for encryption, one for authentication), so a 256-bit key for AES-SIV corresponds to AES-128, 384-bit to AES-192, and 512-bit to AES-256. The `AESAuthenticatedKeygen` node handles this automatically.

## Nonce Handling

- **AES-GCM, AES-GCM-SIV, AES-OCB3, AES-CCM**: Require a unique nonce for every encryption operation with the same key. Reusing a nonce can lead to catastrophic security failures. A 12-byte (96-bit) nonce is typically used.
- **AES-SIV**: Does not require a unique nonce, making it more robust against nonce misuse. The `nonce` input is treated as part of the associated data for authentication.
