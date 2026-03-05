# Reed-Solomon Decode

Decodes data that was encoded with Reed-Solomon error correction codes and attempts to correct any errors.

Source library: `reedsolo`

## Overview

This node takes data that includes Reed-Solomon error correction symbols and attempts to recover the original message. It can correct a certain number of errors (erasures and corruptions) in the data.

## Parameters

- **data**: The `BYTESLIKE` data to be decoded (this should be the output of the Reed-Solomon Encode node).
- **ecc_symbols**: The number of error correction symbols that were added during encoding. This must match the value used for encoding.
- **erase_pos**: (Optional) A comma-separated list of integer positions where known errors (erasures) have occurred. Providing this information can significantly improve the decoder's ability to correct errors.

## Outputs

- **decoded_msg**: The corrected, original message as a `BYTESLIKE` object.
- **msg_with_code**: The full message with corrected data and ECC symbols.
- **errata_pos_list**: A list of positions where errors were found and corrected.
