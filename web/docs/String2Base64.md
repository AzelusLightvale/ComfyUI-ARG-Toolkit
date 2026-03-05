# String to Base64 Converter

Converts a string into its Base64 encoded representation.

Source: Python `base64` module

## Overview

This node takes a text string, encodes it into bytes using the specified character encoding, and then encodes those bytes into a Base64 string. Base64 is commonly used to transmit binary data over text-based channels.

## Parameters

- **text**: The input string to convert.
- **encoding_format**: The character encoding to use for the initial conversion from string to bytes (e.g., `utf-8`, `ascii`).
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **converted_txt**: The Base64 encoded string.
