# DER Serialized Public Key Loader

Loads a public key from a DER-encoded byte string.

Source library: `cryptography`

## Overview

This node loads a public key serialized in DER format. DER is a binary format commonly used in X.509 digital certificates and public key infrastructure (PKI) systems.

## Parameters

- **keyfile**: The DER-encoded public key data, as a `BYTESLIKE` object.

## Outputs

- **loaded_key**: The loaded public key object (`KEYOBJ`), ready for use with verification nodes.

## Additional Considerations

- DER public keys are commonly found in X.509 certificates. Always verify the certificate chain when loading public keys from untrusted sources.
