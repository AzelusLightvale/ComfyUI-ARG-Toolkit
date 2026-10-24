# RSA Private Numbers Values

Extracts the private key components from an RSA private key.

Source library: `cryptography`

## Overview

This node extracts the raw mathematical components of an RSA private key: the two primes (`p`, `q`), the private exponent (`d`), and the CRT parameters (`dmp1`, `dmq1`, `iqmp`). This is useful for debugging, logging, or when keys need to be transmitted in component form.

## Parameters

- **private_numbers**: (Optional) A `NUMOBJ` object containing the private key numbers.
- **private_key**: (Optional) A loaded private key object (`KEYOBJ`).

## Outputs

- **public_numbers**: The public key numbers as a `NUMOBJ` object.
- **var_p**: The first prime (`p`) as an integer.
- **var_q**: The second prime (`q`) as an integer.
- **private_exponent**: The private exponent (`d`) as an integer.
- **dmp1**: The CRT parameter `dmp1` as an integer.
- **dmq1**: The CRT parameter `dmq1` as an integer.
- **iqmp**: The CRT parameter `iqmp` as an integer.

## Additional Considerations

- This node is primarily for debugging or inspection purposes.
- The private key components are sensitive and should be protected.
