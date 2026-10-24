# Rotor Machine Circuit Stepper

Creates a stepper using a control circuit for irregular stepping patterns.

Source: Native Python

## Overview

This node creates a stepper mechanism that uses a control circuit to drive irregular rotor stepping. The circuit defines which rotor slots are affected by which input/output symbols, allowing for complex, non-standard stepping patterns that go beyond simple rule-based mechanisms.

## Parameters

- **base**: A `STEPPER` base stepper (must be a `RuleStepper`). This stepper drives the side rotors.
- **circuit**: A string defining the control circuit connections. Default is `3`.
- **inputs**: A string defining the input symbols for the circuit. Default is `A`.
- **targets**: A string defining the target symbols and their corresponding rotor slots. Format is `symbol=slot`. Default is `E=2`.
- **evaluate_after_base**: When `True`, the circuit is evaluated after the base stepper runs. Default is `False`.
- **map_a**: (Optional) A `PERMUTATION` map for circuit symbol `a`.
- **map_b**: (Optional) A `PERMUTATION` map for circuit symbol `b`.

## Outputs

- **circuit_stepper**: A `STEPPER` object that can be passed to the Rotor Machine State node.

## Additional Considerations

- The base stepper must be a `RuleStepper` - it drives the side rotors.
- The circuit defines how the machine's internal state drives additional rotor movement beyond the base stepping rules.
- This is an advanced feature for implementing non-standard rotor machines like the SIGABA or similar complex mechanisms.
