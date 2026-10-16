# OpenSSH Serialized Public Key Loader

Loads a public key from an OpenSSH-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a public key in the OpenSSH wire format, as used in `~/.ssh/authorized_keys` files and SSH certificate files. The format begins with a prefix like `ssh-ed25519 AAAA...` or `ecdsa-sha2-nistp256 AAAA...`.

## Parameters

- **keyfile**: The OpenSSH-encoded public key data, as a `BYTESLIKE` object.

## Outputs

- **loaded_key**: The loaded public key object (`KEYOBJ`), ready for use with verification nodes.

## Additional Considerations

- OpenSSH public keys are commonly used in SSH deployments. Always obtain them from trusted sources (e.g., your own `authorized_keys` file).
- This node does not validate the key against a known hosts file. Manually verify key fingerprints when connecting to new hosts.
