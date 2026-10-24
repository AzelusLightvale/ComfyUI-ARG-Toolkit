# RSA Public Numbers into Key

Constructs an RSA public key from its component numbers.

Source library: `cryptography`

## Overview

This node reconstructs an RSA public key from its mathematical components: the modulus (`n`) and the public exponent (`e`). This is useful when working with raw key material or when keys need to be transmitted in component form.

## Parameters

- **public_numbers**: A `NUMOBJ` object containing the public key numbers, obtained from another node.
- **public_key**: (Optional) A loaded public key object (`KEYOBJ`). Required when `key_source` is "From Loaded Key".
- **var_n**: The modulus (`n`) as an integer.
- **var_e**: The public exponent (`e`) as an integer.

## Outputs

- **public_key**: The reconstructed public key object (`KEYOBJ`).
- **public_numbers**: The public key numbers as a `NUMOBJ` object.

## Additional Considerations

- This node is useful for debugging or when working with key components from external sources.
- Always verify the origin of key components before using them in production.
