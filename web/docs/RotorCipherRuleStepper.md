# Rotor Machine Rule-Based Stepper

Defines custom stepping rules for rotor machines.

Source: Native Python

## Overview

This node creates a stepper mechanism that defines how rotors turn during encryption. It uses a rule-based system where each rotor has a set of conditions (clauses) that determine when it steps. This allows for complex stepping patterns like the Enigma double-stepping mechanism.

## Parameters

- **rules**: A multiline string defining the stepping rules. Each line corresponds to a rotor (from left to right). The default is `1\n2|1\nalways`, which implements the standard Enigma stepping pattern.
- **reverse**: (Optional) A string defining reverse stepping rules for decryption. Default is empty (no reverse rules).

## Outputs

- **stepper**: A `STEPPER` object that can be passed to the Rotor Machine State node.

## Additional Considerations

- The rule format uses a simple syntax where each line defines the conditions under which a rotor steps.
- The `always` keyword means the rotor steps on every character.
- Reverse rules are used for decryption and should mirror the forward rules.
