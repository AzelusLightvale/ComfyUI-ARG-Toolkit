# PBKDF2HMAC Key Derivation

Derives a key from a password using the PBKDF2HMAC algorithm.

Source library: `cryptography`

## Overview

PBKDF2 (Password-Based Key Derivation Function 2) is a widely used standard for hashing passwords, defined in RFC 2898 and NIST SP 800-132. It applies a pseudorandom function, such as HMAC, to the input password along with a salt value and repeats the process many times. This "stretching" makes brute-force attacks much more computationally expensive.

This node is highly suitable for password storage and verification.

## Parameters

- **message**: The input password or message to derive the key from, as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **salt**: A random `BYTESLIKE` value. A salt is crucial for password hashing as it ensures that two identical passwords will hash to different values.
- **iterations**: The number of iterations to perform. Higher numbers are more secure but slower. The default of 1,200,000 is a strong modern value.
- **algorithm**: The hash function to use for the underlying HMAC operation (e.g., `SHA256`).

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
