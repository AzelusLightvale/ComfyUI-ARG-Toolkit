# ChaCha20-Poly1305 Key Generator

Generates a random 256-bit (32-byte) key suitable for use with the ChaCha20-Poly1305 encryption node.

## Overview

This is a simple convenience node that calls `cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305.generate_key()` to create a cryptographically secure random key.

## Parameters

This node has no input parameters.

## Outputs

- **key**: A `BYTESLIKE` object containing a new 32-byte key.
