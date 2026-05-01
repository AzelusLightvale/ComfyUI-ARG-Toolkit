# String to Binary Converter

Converts a string into its binary representation.

## Overview

This node takes a text string and converts each character into its binary form based on the selected character encoding. The output is a string of binary digits (0s and 1s), with each byte represented by 8 bits, separated by spaces.

## Parameters

- **text**: The input string to convert.
- **encoding_format**: The character encoding to use for the conversion (e.g., `utf-8`, `ascii`). This determines how characters are mapped to bytes before being converted to binary.
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format supported by Python.

## Outputs

- **converted_txt**: The binary representation of the input string.
