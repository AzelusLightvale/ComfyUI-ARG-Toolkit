# RSA Restore Prime Factors

Recovers the RSA prime factors (`p` and `q`) from the modulus, public exponent, and private exponent.

Source library: `cryptography`

## Overview

This node computes the two prime factors (`p` and `q`) of an RSA key given the modulus (`n`), the public exponent (`e`), and the private exponent (`d`). This is a mathematical recovery operation that is useful when reconstructing keys from partial information.

## Parameters

- **private_modulus**: The private modulus (`n`) as an integer.
- **public_exponent**: The public exponent (`e`) as an integer.
- **private_exponent**: The private exponent (`d`) as an integer.

## Outputs

- **p**: The first prime factor (`p`) as an integer.
- **q**: The second prime factor (`q`) as an integer.

## Additional Considerations

- This node is useful for debugging or when working with key components from external sources.
- The prime factors are sensitive and should be protected.
