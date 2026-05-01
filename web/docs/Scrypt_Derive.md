# Scrypt Key Derivation

Derives a key from a password using the Scrypt algorithm.

Source library: `cryptography`

## Overview

Scrypt is a password-based key derivation function defined in RFC 7914. It was designed to be significantly more secure against large-scale custom hardware attacks than alternatives like PBKDF2. It achieves this by having a high memory cost, making it a "memory-hard" function.

This node is an excellent choice for high-security password hashing.

## Parameters

- **message**: The input password or message to derive the key from, as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **salt**: A random `BYTESLIKE` value. A salt is crucial for password hashing.
- **n**: The CPU/Memory cost parameter. The node takes this as an exponent for a power of 2 (e.g., an input of `14` means the cost `N` is `2**14`). This must be larger than 1 and a power of 2.
- **r**: The block size parameter, which affects memory usage and access patterns.
- **p**: The parallelization parameter, which affects the number of parallel computations.

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
