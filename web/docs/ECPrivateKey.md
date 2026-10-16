# Elliptic Curve Private Key Bytes

Generates an EC private key and serializes it.

Source library: `cryptography`

## Overview

Elliptic Curve Cryptography (ECC) provides strong security with smaller key sizes compared to RSA. This node generates a private key for a selected named curve and serializes it into bytes. The private key can optionally be derived from a specific scalar value or generated randomly.

## Parameters

- **curve_name**: The named elliptic curve to use. Available curves include:
    - **SECP256R1** (P-256): The most widely used curve.
    - **SECP384R1** (P-384): A higher-security curve.
    - **SECP521R1** (P-521): A very high-security curve.
    - **SECP256K1**: The Bitcoin curve.
    - **BRAINPOOLP256R1**, **BRAINPOOLP384R1**, **BRAINPOOLP512R1**: Brainpool curves.
    - And other curves defined in the `cryptography` library.
- **formatting**: The serialization format.
    - **Traditional OpenSSL**: The traditional SEC1 format.
    - **PKCS8**: The modern PKCS#8 format.
    - **OpenSSH**: OpenSSH private key format (requires PEM encoding).
- **encoding**: The encoding format (**PEM** or **DER**).
- **encryption**: How to encrypt the private key (**Best Available** or **None**).
- **encryption_password**: (Optional) The password for encrypting the private key.
- **private_value**: (Optional) A decimal integer string. If provided, the private key is derived from this scalar value instead of being randomly generated. This is useful for deterministic key generation.
- **pem_key**: (Optional) A `BYTESLIKE` PEM-encoded key. For loading an existing key.

## Outputs

- **keyfile**: The serialized private key as a `BYTESLIKE` object.
- **private_key**: The private key object (`KEYOBJ`), which can be passed to signing nodes.

## Additional Considerations

- The `private_value` parameter allows deterministic key generation, which can be useful for testing but should be used with caution in production. If the value is weak or predictable, the key is compromised.
- Always protect private keys. Use encryption when storing or transmitting them.
