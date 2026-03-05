# AES Authenticated Encryption Key Generator

Generates a random key suitable for use with the AES-based authenticated encryption node.

## Overview

This is a convenience node that calls the appropriate `generate_key()` method from the `cryptography` library based on the selected AES type and bit length.

## Parameters

- **bit_length**: The desired key size in bits (128, 192, or 256). Note that for AES-SIV, the effective AES key size is half the selected bit length.
- **aes_type**: The AES authenticated encryption mode for which to generate a key.

## Outputs

- **key**: A `BYTESLIKE` object containing a new key of the appropriate length for the selected algorithm.
