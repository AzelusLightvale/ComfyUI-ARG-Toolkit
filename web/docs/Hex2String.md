# Hexadecimal to String Converter

Converts a hexadecimal string into a text string.

## Overview

This node takes a hexadecimal string, converts it into bytes, and then decodes those bytes back into a text string using the specified character encoding. It can handle common hex prefixes like "0x" and spaces within the input string.

## Parameters

- **text**: The input hexadecimal string to convert.
- **encoding_format**: The character encoding to use for decoding the bytes (e.g., `utf-8`, `ascii`).
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **converted_txt**: The decoded text string.
