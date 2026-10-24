# RSA Private Key Bytes

Generates an RSA private key and serializes it.

Source library: `cryptography`

## Overview

RSA is a widely used public-key cryptosystem for secure data transmission. This node generates a new RSA private key with a specified key size and serializes it into bytes. The private key can optionally be encrypted with a password for secure storage.

## Parameters

- **public_exponent**: The public exponent (e) for the key. Commonly 65537.
- **key_size**: The size of the key in bits (512 to 8192, in steps of 128). Default is 2048.
- **encoding**: The encoding format for the serialized key (**PEM** or **DER**).
- **formatting**: The key format to serialize in.
    - **PKCS8**: Modern standard format.
    - **OpenSSH**: OpenSSH private key format (requires PEM encoding).
    - **TraditionalOpenSSL**: Legacy SEC1 format.
- **encryption**: How to encrypt the private key (**Best Available** or **None**).
- **encryption_password**: (Optional) The password to use for encrypting the private key. Required when `encryption` is set to "Best Available".

## Outputs

- **key_object**: The private key object (`KEYOBJ`), which can be passed to signing and decryption nodes.
- **private_key**: The serialized private key as a `BYTESLIKE` object.
- **private_numbers**: The private key numbers as a `NUMOBJ` object.

## Additional Considerations

- Always protect private keys. Use encryption when storing or transmitting them.
- Larger key sizes provide more security but take longer to generate.
