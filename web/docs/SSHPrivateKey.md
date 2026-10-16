# OpenSSH Serialized Private Key Loader

Loads a private key from an OpenSSH-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a private key in the OpenSSH private key format, as stored in `~/.ssh/id_ed25519`, `~/.ssh/id_rsa`, etc. The loaded key can be used for signing and decryption operations.

## Parameters

- **keyfile**: The OpenSSH-encoded private key data, as a `BYTESLIKE` object.
- **password**: (Optional) The password used to decrypt the key, as a `BYTESLIKE` object. Required if the key is passphrase-protected.
- **skip_rsa_key_validation**: (Optional) A `BOOLEAN` that, when `True`, skips RSA key validation. **Warning**: Disabling this validation is **unsafe** and may cause OpenSSL to misbehave or crash, potentially dragging ComfyUI down with it. Only enable this if you know exactly what you are doing.

## Outputs

- **loaded_key**: The loaded private key object (`KEYOBJ`), ready for use with signing and decryption nodes.

## Additional Considerations

- RSA key validation is a security check that ensures the key components are mathematically valid. Skipping it is **unsafe** and should only be done in exceptional circumstances.
- OpenSSH private keys may be passphrase-protected. If the key is encrypted, the correct password must be provided.
