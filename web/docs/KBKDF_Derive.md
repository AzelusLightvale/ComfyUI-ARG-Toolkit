# KBKDF Key Derivation

Derives a key using the Key-Based Key Derivation Function (KBKDF) in Counter Mode.

Source library: `cryptography`

## Overview

This node implements the KDF specified in NIST SP 800-108. It is designed to derive additional cryptographic keys from a single master key (`Ki`). The function uses a pseudorandom function (PRF), such as HMAC or CMAC, in a counter mode construction.

## Parameters

- **message**: The master key (`Ki`) to derive from, as a `BYTESLIKE` object.
- **length**: The desired length of the derived key in bytes.
- **algorithm**: The hash function to use for the underlying PRF (e.g., `SHA256`).
- **operation_mode**: The PRF to use.
    - `KBKDFHMAC`: Uses HMAC as the PRF.
    - `KBKDFCMAC`: Uses CMAC as the PRF. (Note: CMAC requires an underlying block cipher like AES, which is not exposed as an option in this node and may lead to errors if not configured correctly in the backend).
- **location**: The position of the counter within the data fed to the PRF (`BeforeFixed`, `AfterFixed`, `MiddleFixed`).
- **rlen**: The length of the counter field in bytes.
- **llen**: The length of the output key length field in bytes.
- **label**: (Optional) A `BYTESLIKE` string identifying the purpose of the derived key.
- **context**: (Optional) `BYTESLIKE` information related to the context of the derived key.
- **fixed**: (Optional) Instead of `label` and `context`, you can supply fixed data in this field. If specified, `label` and `context` are ignored.
- **break_location**: (Optional) When `location` is `MiddleFixed`, this specifies the byte offset where the counter is inserted.

## Outputs

- **derived_key**: The resulting derived key as a `BYTESLIKE` object.
