# Argon2id Key Derivation

Derives a key from a message using the Argon2id algorithm.

Source library: `cryptography`

## Parameters

- **length**: The desired length of the derived key.
- **message**: The message to derive the key from.
- **salt**: The salt to use for key derivation. Must be a hexadecimal string.
- **mode**: Whether to output the key as a string or in PHC format.
- **iterations**: The number of iterations to use.
- **parallel_lanes**: The number of parallel lanes to use.
- **memory_cost**: The memory cost to use.
- **ad**: Associated data.
- **secret**: Secret data.