# RSA Public Numbers Values

Extracts the modulus and public exponent from an RSA public key.

Source library: `cryptography`

## Overview

This node extracts the raw mathematical components of an RSA public key: the modulus (`n`) and the public exponent (`e`). This is useful for debugging, logging, or when keys need to be transmitted in component form.

## Parameters

- **public_numbers**: (Optional) A `NUMOBJ` object containing the public key numbers.
- **public_key**: (Optional) A loaded public key object (`KEYOBJ`).

## Outputs

- **public_numbers**: The public key numbers as a `NUMOBJ` object.
- **var_n**: The modulus (`n`) as an integer.
- **var_e**: The public exponent (`e`) as an integer.

## Additional Considerations

- This node is primarily for debugging or inspection purposes.
- The modulus can be very large (e.g., 2048 bits or more).
