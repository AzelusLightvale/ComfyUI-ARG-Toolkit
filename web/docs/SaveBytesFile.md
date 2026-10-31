# Save Bytes as File

Saves a `BYTESLIKE` object as a key file in the ComfyUI key files directory.

Source: Native Python

## Overview

This node saves raw byte data (such as a serialized cryptographic key) to a private temporary directory managed by the ARG Toolkit. The saved file can then be loaded later using the **Load File as Bytes** node, or downloaded via the `/keyfiles/upload` HTTP endpoint. This provides a secure way to pass key material between ComfyUI workflow runs.

## Parameters

- **data**: The `BYTESLIKE` data to save to the file.
- **filename**: The base name of the file to save (no path separators). Default is `keyfile`.
- **extension**: The file extension to append to the filename. Default is `pem`. Make sure to change this to the correct format (e.g., `pem`, `der`, `key`, `pub`).
- **mode**: The file permissions in octal format, similar to `chmod` in POSIX. Default is `400` (read-only for owner). Use `600` for read-write owner access.
- **overwrite**: When `True`, overwrites an existing file with the same name. Default is `False`.

## Outputs

This node has no outputs. It is an output-only node that writes a file to the key files directory.

## Additional Considerations

- The file is written to a private temporary directory with mode `0700` on POSIX systems.
- The `mode` parameter controls file permissions. For sensitive key material, use `400` (owner read-only) or `600` (owner read-write).
- If `overwrite` is `False` and a file with the same name exists, a `FileExistsError` will be raised.
- The filename must be a bare name without path separators.
- In modern versions of Python, `0700` on Windows uses ACL under OWNER RIGHTS, which can cause issues in certain situations if the owner is elevated into administrator instead of the standard user. See [this GitHub issue](https://github.com/python/cpython/issues/157876) for more information.
