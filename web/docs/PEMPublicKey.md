# PEM Serialized Public Key Loader

Loads a public key from a PEM-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a public key serialized in PEM format. Public keys are not secret and are commonly distributed in PEM format (e.g., in SSL/TLS certificates, SSH authorized_keys files). The loaded key can be used to verify signatures or perform key exchanges.

## Parameters

- **keyfile**: The PEM-encoded public key data, as a `BYTESLIKE` object.

## Outputs

- **loaded_key**: The loaded public key object (`KEYOBJ`), ready for use with verification nodes.

## Additional Considerations

- Public keys are safe to distribute, but always obtain them from a trusted source. In a production setting, a malicious public key could be used in a man-in-the-middle attack if the corresponding private key is also controlled by the attacker.
