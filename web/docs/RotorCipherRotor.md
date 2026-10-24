# Rotor Machine Rotor

Creates a rotor for use in rotor machine ciphers (e.g., Enigma).

Source: Native Python

## Overview

This node defines a single rotor, which is the core component of rotor machine ciphers. A rotor is a wheel with a wiring permutation that maps input letters to output letters. Rotors also have "notches" that cause adjacent rotors to step, and a "ring" offset that shifts the wiring relative to the alphabet.

## Parameters

- **alphabet**: The alphabet to use for the rotor. Default is the standard 26-letter English alphabet.
- **wiring**: The forward wiring permutation. Each symbol in the alphabet must appear exactly once. Default is the standard Enigma III wiring: `EKMFLGDQVZNTOWYHXUSPAIBRCJ`.
- **notches**: The symbols at which the rotor causes the next rotor to step. Default is `Q` (standard Enigma notch).
- **ring**: The ring offset (0 to 4096). Default is 0.
- **invert**: When `True`, uses the inverse wiring permutation. Default is `False`.
- **previous_rotor**: (Optional) A chain of previously created rotors (`ROTORS`). Use this to build a stack of rotors.

## Outputs

- **rotor**: A `ROTORS` object containing the rotor (and any previously chained rotors).

## Additional Considerations

- The wiring must be a permutation of the alphabet - each symbol must appear exactly once.
- The ring offset shifts the effective wiring and notch positions relative to the rotor's physical position.
- Rotors are typically chained together using the `previous_rotor` input to build a complete rotor stack.
