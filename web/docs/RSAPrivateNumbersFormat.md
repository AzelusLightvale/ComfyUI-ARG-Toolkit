# RSA Private Numbers into Key

Constructs an RSA private key from its component numbers.

Source library: `cryptography`

## Overview

This node reconstructs an RSA private key from its mathematical components: the two primes (`p`, `q`), the private exponent (`d`), and the public key numbers. This is useful when working with raw key material or when keys need to be transmitted in component form.

## Parameters

- **public_numbers**: A `NUMOBJ` object containing the public key numbers, obtained from another node.
- **var_p**: One of the two primes composing the private modulus `n`.
- **var_q**: One of the two primes composing the private modulus `n`.
- **private_exponent**: The private exponent (`d`).
- **skip_rsa_key_validation**: (Optional) A `BOOLEAN` that, when `True`, skips RSA key validation. **Warning**: Disabling this validation is **unsafe** and may cause OpenSSL to misbehave or crash, potentially dragging ComfyUI down with it. Only enable this if you know exactly what you are doing.

## Outputs

- **public_key**: The reconstructed private key object (`KEYOBJ`).
- **private_numbers**: The private key numbers as a `NUMOBJ` object.

## Additional Considerations

- This node is useful for debugging or when working with key components from external sources.
- Always verify the origin of key components before using them in production.
- Skipping RSA key validation is **unsafe** and should only be done in exceptional circumstances.
