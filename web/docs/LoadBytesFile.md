# Load File as Bytes

Loads a file from the ComfyUI key files directory and returns its contents as a `BYTESLIKE` object.

Source: Native Python

## Overview

This node loads a previously uploaded key file from a private temporary directory managed by the ARG Toolkit. Files must first be uploaded via the **Save Bytes as File** node or through the `/keyfiles/upload` HTTP endpoint. The loaded bytes can then be passed directly to key loader nodes (e.g., PEM, DER, SSH) that expect `BYTESLIKE` input.

## Parameters

- **file**: The filename to load, selected from the list of available key files in the private directory.

## Outputs

- **BYTESLIKE**: The raw file contents as a `BYTESLIKE` object.

## Additional Considerations

- Files are stored in a private temporary directory with mode `0700` on POSIX systems, accessible only within this ComfyUI session.
- The file list is dynamically updated as files are uploaded or saved.
- If a file is not found, an error message will be displayed. Re-upload the file if necessary.
- This node is designed for securely passing key material between nodes without exposing it as a text input.
