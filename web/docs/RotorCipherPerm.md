# Rotor Machine Permutation

Creates a fixed permutation stage for rotor machines.

Source: Native Python

## Overview

This node creates a fixed (non-rotating) permutation stage. Fixed permutations are used in rotor machines for components like the entry wheel (ETW), reflector (UKW), or plugboard (Steckerbrett). Unlike rotors, these stages do not step or rotate during encryption.

## Parameters

- **alphabet**: The alphabet to use for the permutation. Default is the standard 26-letter English alphabet.
- **wiring**: The permutation wiring. Each symbol in the alphabet must appear exactly once. Default is `EKMFLGDQVZNTOWYHXUSPAIBRCJ`.

## Outputs

- **perm_obj**: A `PERMUTATION` object representing the fixed permutation stage.

## Additional Considerations

- The wiring must be a permutation of the alphabet - each symbol must appear exactly once.
- For reflectors and plugboards, the permutation must be an involution (i.e., applying it twice returns the original letter). This is enforced by the machine node, not this one.
