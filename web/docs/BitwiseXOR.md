# Bitwise XOR Operator

Performs a bitwise XOR operation on two inputs.

## Overview

This node takes two inputs, interprets them as byte arrays based on the selected `datatype`, and performs a bitwise XOR (exclusive OR) operation between them. The inputs must be of the same length. The result is then formatted back into the same datatype as the input. XOR is a common operation in cryptography.

## Parameters

- **text_1**: The first input string.
- **text_2**: The second input string.
- **datatype**: The format of the input strings. Can be `String`, `Hexadecimal`, `Base64`, `Integer`, or `Binary`. This determines how the strings are parsed into bytes before the operation.
- **encoding_format**: If `datatype` is `String`, this specifies the character encoding to use.
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **bitwise_txt**: The result of the XOR operation, formatted according to the input `datatype`.
