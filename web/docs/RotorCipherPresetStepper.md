# Rotor Machine Preset Stepper

Creates a stepper using a preset stepping pattern.

Source: Native Python

## Overview

This node creates a stepper mechanism using one of two preset patterns: Enigma or Odometer. These are common stepping patterns used in historical rotor machines.

## Parameters

- **type**: The preset stepping pattern to use.
    - **Enigma**: The standard Enigma stepping pattern, which includes the double-stepping mechanism.
    - **Odometer**: A simple odometer pattern where the rightmost rotor always steps, and each subsequent rotor steps only when the previous one completes a full rotation.
- **k**: The number of rightmost rotors that participate in stepping (1 to 64). Default is 3.

## Outputs

- **stepper**: A `STEPPER` object that can be passed to the Rotor Machine State node.

## Additional Considerations

- The `k` parameter determines how many rotors from the right side participate in the stepping mechanism.
- Preset steppers count every rotor in the machine, including auxiliary rotors. If using auxiliary rotors, use a rule or circuit stepper instead.
