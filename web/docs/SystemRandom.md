# Random Nonce Generator

Generates a random number of bytes using the operating system's source of entropy.

Source: Python `os` module

## Overview

This node provides a simple way to generate cryptographically secure random bytes, which are essential for many cryptographic operations like creating nonces, salts, or initialization vectors (IVs). It uses `os.urandom()`, which is suitable for cryptographic use.

## Parameters

- **byte_num**: The number of random bytes to generate.

## Outputs

- **rand_value**: The generated random bytes, as a `BYTESLIKE` object.
