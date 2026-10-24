# RSA Restore Private Exponent

Recovers the RSA private exponent (`d`) from the public exponent and the two prime factors.

Source library: `cryptography`

## Overview

This node computes the RSA private exponent (`d`) given the public exponent (`e`) and the two prime factors (`p` and `q`). This is a mathematical recovery operation that is useful when reconstructing keys from partial information.

## Parameters

- **public_exponent**: The public exponent (`e`) as an integer.
- **var_p**: One of the two primes composing the private modulus `n`.
- **var_q**: One of the two primes composing the private modulus `n`.

## Outputs

- **d**: The recovered private exponent (`d`) as an integer.

## Additional Considerations

- This node is useful for debugging or when working with key components from external sources.
- The private exponent is sensitive and should be protected.
