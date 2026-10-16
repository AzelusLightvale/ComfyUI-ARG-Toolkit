# Bits Counter

Counts the number of bits in a `BYTESLIKE` object.

Source: Native Python

## Overview

This is a simple utility node that calculates the total number of bits in a given `BYTESLIKE` (bytes-like) object. Each byte contains 8 bits, so the output is simply `len(data) * 8`. This can be useful for quickly assessing the size of cryptographic material or for workflow planning.

## Parameters

- **text**: The input `BYTESLIKE` object to count the bits of.

## Outputs

- **bit_count**: The total number of bits, as an integer string.

## Security Considerations

- This is a read-only utility and has no security implications. It is purely informational.
