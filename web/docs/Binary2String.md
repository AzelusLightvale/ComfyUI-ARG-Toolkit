# Binary to String Converter

Converts a string of binary digits into a text string.

## Overview

This node takes a string of binary digits (0s and 1s), groups them into 8-bit bytes, and then decodes them back into a text string using the specified character encoding. It automatically handles spaces and newlines in the input binary string.

## Parameters

- **text**: The input binary string to convert. It should consist of '0' and '1' characters. The total number of digits must be a multiple of 8.
- **encoding_format**: The character encoding to use for decoding the bytes (e.g., `utf-8`, `ascii`). This must match the encoding used to create the binary string.
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **converted_txt**: The decoded text string.
