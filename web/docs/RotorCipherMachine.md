# Rotor Machine State

Assembles a complete rotor machine from its components.

Source: Native Python

## Overview

This node assembles a complete rotor machine by combining rotors, a stepper mechanism, and optional auxiliary components like entry wheels, reflectors, and plugboards. The resulting machine can then be used for encryption and decryption.

## Parameters

- **rotors**: A `ROTORS` chain of rotors (from the Rotor Machine Rotor node). Required.
- **stepper**: A `STEPPER` object that defines how the rotors step (from a stepper node). Required.
- **entry**: (Optional) A `PERMUTATION` entry wheel (ETW). Applied first on the way in, and inverted on the way out. Identity for Wehrmacht Enigmas.
- **reflector**: (Optional) A `PERMUTATION` static reflector (UKW). Must be an involution. Use this OR `reflector_rotor`, not both.
- **reflector_rotor**: (Optional) A `PERMUTATION` reflector that takes a position (slot 0). A chain of exactly one rotor with an involutive wiring. Use this OR `reflector`, not both.
- **plugboard**: (Optional) A `PERMUTATION` Steckerbrett. Applied outermost, before the entry wheel. Must be an involution.
- **auxilliary_rotors**: (Optional) A `ROTORS` chain of auxiliary rotors that do not participate in stepping.

## Outputs

- **cipher_machine**: A `MACHINE` object ready for use with the Rotor Machine Encrypt/Decrypt node.

## Additional Considerations

- The machine requires at least one rotor.
- The reflector and reflector_rotor are mutually exclusive - use only one.
- The entry wheel, reflector, and plugboard must each map an alphabet to itself and must be involutions (except the entry wheel, which can be any permutation).
- When using auxiliary rotors, preset steppers are not supported. Use rule or circuit steppers instead.
