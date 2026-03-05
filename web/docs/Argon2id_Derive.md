# Argon2id Key Derivation

Derives a key from a password or message using the Argon2id algorithm.

Source library: `cryptography`

## Overview

Argon2 is a key derivation function that was selected as the winner of the Password Hashing Competition in July 2015. Argon2id is a hybrid version of Argon2i and Argon2d, providing resistance against both side-channel and GPU cracking attacks. It is a recommended algorithm for modern password hashing.

This node takes a password (or other message) and derives a cryptographic key of a specified length.

## Parameters

- **message**: The input password or message to derive the key from, as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **salt**: A random `BYTESLIKE` value. A salt is crucial for password hashing as it ensures that two identical passwords will hash to different values.
- **mode**:
    - `string`: Derives a raw key as a `BYTESLIKE` object.
    - `phc`: Derives a key and formats it as a PHC (Password Hashing Competition) string, which includes the algorithm, salt, and parameters. This is useful for storing password hashes.
- **iterations**: The time cost, also known as the number of passes. A higher number increases the time required, making brute-force attacks more difficult.
- **parallel_lanes**: The degree of parallelism (i.e., how many threads to use).
- **memory_cost**: The amount of memory to use in kibibytes (KiB). This is the primary factor in Argon2's resistance to custom hardware attacks.
- **ad**: (Optional) `BYTESLIKE` associated data. This data is included in the hash computation but is not part of the derived key.
- **secret**: (Optional) `BYTESLIKE` secret data. If provided, Argon2id will operate in keyed-hashing mode.

## Outputs

- **derived_key**: The resulting key as a `BYTESLIKE` object. If `mode` is `phc`, this will be a UTF-8 encoded PHC string.
