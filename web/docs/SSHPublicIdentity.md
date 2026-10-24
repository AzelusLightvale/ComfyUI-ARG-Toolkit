# OpenSSH Public Identity Loader

Loads an OpenSSH public key or certificate and returns both the identity and the underlying public key.

Source library: `cryptography`

## Overview

This node loads an OpenSSH public key or SSH certificate from a byte string. Unlike the standard OpenSSH public key loader, it can distinguish between certificates and plain public keys, returning both the raw identity object and the extractable public key.

## Parameters

- **keyfile**: The OpenSSH-encoded public key or certificate data, as a `BYTESLIKE` object.

## Outputs

- **certificate**: The loaded identity object. If the input is an SSH certificate, this is the full certificate object. If the input is a plain public key, this is `None`.
- **key**: The underlying public key object (`KEYOBJ`), ready for use with verification nodes.

## Additional Considerations

- SSH certificates provide additional authentication and are commonly used in enterprise SSH deployments.
- Always obtain SSH certificates and public keys from trusted sources.
