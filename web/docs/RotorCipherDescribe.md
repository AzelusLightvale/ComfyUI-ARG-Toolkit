# Rotor Machine State Descriptor

Displays a human-readable description of a rotor machine's configuration.

Source: Native Python

## Overview

This node outputs a detailed text description of a rotor machine's current configuration, including the rotors, their wirings, notches, ring settings, stepping rules, and any auxiliary components. This is primarily a debugging and inspection tool.

## Parameters

- **machine**: A `MACHINE` object from the Rotor Machine State node. Required.

## Outputs

- **description**: A `STRING` containing the machine's configuration details.

## Additional Considerations

- This is an output-only node designed for debugging and inspection.
- The description includes notes about potential issues, such as non-reflecting paths that require decrypt mode.
