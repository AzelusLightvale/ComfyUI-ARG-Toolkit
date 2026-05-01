# Bitwise NOT Operator

Performs a bitwise NOT (inversion) operation on a single input.

## Overview

This node takes a single input, interprets it as a byte array based on the selected `datatype`, and performs a bitwise NOT operation on each byte. The result is then formatted back into the same datatype as the input.

## Parameters

- **text**: The input string to operate on.
- **datatype**: The format of the input string. Can be `String`, `Hexadecimal`, `Base64`, `Integer`, or `Binary`. This determines how the string is parsed into bytes before the operation.
- **encoding_format**: If `datatype` is `String`, this specifies the character encoding to use.
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **bitwise_txt**: The result of the NOT operation, formatted according to the input `datatype`.
