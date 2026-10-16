# OpenSSH Public Key Fingerprint

Computes a fingerprint for an OpenSSH-encoded public key.

Source library: `cryptography`

## Overview

This node loads an OpenSSH public key and computes a cryptographic fingerprint (hash) of it. Fingerprints are a compact, human-verifiable way to confirm the identity of a public key, commonly displayed when connecting to an SSH server for the first time.

## Parameters

- **keyfile**: The OpenSSH-encoded public key data, as a `BYTESLIKE` object.
- **hash_algorithm**: The hash algorithm to use for the fingerprint.
    - **MD5**: The traditional, legacy SSH fingerprint format (not recommended for new use).
    - **SHA-1**: An older standard, considered weak.
    - **SHA-256**: The modern, recommended standard for SSH key fingerprints.

## Outputs

- **fingerprint**: The computed fingerprint as a `BYTESLIKE` object.

## Additional Considerations

-   - [**MD5**](https://en.wikipedia.org/wiki/MD5#Overview_of_security_issues) and [**SHA1**](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) are broken and should not be used for new fingerprints that requires security.
- Always compare fingerprints out-of-band (e.g., by phone or in person) when verifying a remote host's key.
