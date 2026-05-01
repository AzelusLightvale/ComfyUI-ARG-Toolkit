# Base64 to String Converter

Converts a Base64 encoded string back into a text string.

Source: Python `base64` module

## Overview

This node takes a Base64 encoded string, decodes it into bytes, and then decodes those bytes back into a text string using the specified character encoding.

## Parameters

- **text**: The input Base64 string to convert.
- **encoding_format**: The character encoding to use for the final conversion from bytes to string (e.g., `utf-8`, `ascii`).
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **converted_txt**: The decoded text string.
