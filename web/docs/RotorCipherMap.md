# Rotor Machine Rotor Mapper

Creates a mapping stage that converts between different alphabet sizes.

Source: Native Python

## Overview

This node creates a mapping stage that relabels symbols from one alphabet to another. This is useful when different parts of a rotor machine use different alphabets (e.g., converting between a 26-letter alphabet and a different symbol set).

## Parameters

- **src_alphabet**: The source alphabet. Default is `ABCEDEFGHIJKLMNOPQRSTUVWXYZ`.
- **dst_alphabet**: The destination alphabet. Default is `ABCEDEFGHIJKLMNOPQRSTUVWXYZ`.
- **mapping**: A string specifying the mapping from destination alphabet symbols to source alphabet positions. Each symbol in the destination alphabet must appear exactly once.

## Outputs

- **perm_obj**: A `PERMUTATION` object representing the mapping stage.

## Additional Considerations

- The source and destination alphabets must each contain unique symbols.
- The mapping must have exactly one symbol per source alphabet symbol.
- This node is useful for adapting rotor machines to non-standard alphabets.
