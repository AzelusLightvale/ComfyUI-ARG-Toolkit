# Rotor Machine Positions

Sets the starting positions for rotors in a rotor machine.

Source: Native Python

## Overview

This node sets the initial positions (starting positions) for each rotor in a rotor machine. The positions are specified as a string of letters, one per rotor, from left to right. These positions are used as the starting state before each encryption or decryption operation.

## Parameters

- **positions**: A string of letters representing the starting position for each rotor, from left to right. Whitespace is ignored. Default is `AAA`.

## Outputs

- **rotor_pos**: A `POSITIONS` object that can be passed to the Rotor Machine Encrypt/Decrypt node.

## Additional Considerations

- The positions string must contain at least one character.
- The positions should use symbols from the rotor alphabet.
- For a machine with N rotors, provide N position characters.
