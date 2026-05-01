# Bitwise Left Shift Operator

Performs a bitwise left shift operation on two inputs.

## Overview

This node takes two inputs, `text_1` (the value) and `text_2` (the shift amount), interprets them as byte arrays based on the selected `datatype`, and performs a bitwise left shift (`<<`) operation for each corresponding pair of bytes. The inputs must be of the same length. The result is then formatted back into the same datatype as the input.

## Parameters

- **text_1**: The input string containing the values to be shifted.
- **text_2**: The input string containing the number of bits to shift by.
- **datatype**: The format of the input strings. Can be `String`, `Hexadecimal`, `Base64`, `Integer`, or `Binary`.
- **encoding_format**: If `datatype` is `String`, this specifies the character encoding to use.
- **other_encoding_format**: If "Other" is selected for `encoding_format`, this field allows you to specify a custom encoding format.

## Outputs

- **bitwise_txt**: The result of the left shift operation, formatted according to the input `datatype`.
