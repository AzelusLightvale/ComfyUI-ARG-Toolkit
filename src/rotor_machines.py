# Rotor machine ciphers (Enigma, Typex, etc.)
from dataclasses import dataclass, replace
from abc import ABC, abstractmethod
from functools import lru_cache, cached_property

# Base datatypes used for this node
Perm = tuple[int, ...]
Positions = tuple[int, ...]

# Stage dataclass, for mapping symbols to other symbols
@dataclass(frozen=True)
class Stage(ABC):
    @abstractmethod
    def apply(self, pos: Positions, x: int) -> int: ...

    def validate(self, n: int) -> None: return None

    @abstractmethod
    def inverted(self): ...

    @abstractmethod
    def src_alphabet(self) -> str: ...

    @abstractmethod
    def dst_alphabet(self) -> str: ...

    def bind(self, rotors):
        return self


@dataclass(frozen=True)
class Fixed(Stage):
    src: str; dst: str; perm: Perm
    def apply(self, pos: Positions, x): return self.perm[x]
    def src_alphabet(self): return self.src
    def dst_alphabet(self): return self.dst
    def inverted(self) -> Stage:
        if len(self.src) != len(self.dst) or len(set(self.perm)) != len(self.dst):
            raise ValueError("Stage given is not a bijection, so it has no inverse.")
        return Fixed(self.dst, self.src, InitNode.perm_invert(self.perm))

@dataclass(frozen=True)
class Rotor: alphabet: str; fwd: Perm; inv: Perm; notches: frozenset[int]; ring: int = 0

@dataclass(frozen=True)
class Through(Stage):
    rotor: Rotor
    index: int
    inverse: bool = False
    def apply(self, pos, x):
        n = len(self.rotor.alphabet)
        s = pos[self.index] - self.rotor.ring
        table = self.rotor.inv if self.inverse else self.rotor.fwd
        return (table[(x + s) % n] - s) % n
    def src_alphabet(self): return self.rotor.alphabet
    def dst_alphabet(self): return self.rotor.alphabet
    def inverted(self): return replace(self, inverse=not self.inverse)

# Stepper dataclass
class Stepper(ABC):
    @abstractmethod
    def __call__(self, rotors: tuple[Rotor, ...], pos: Positions) -> Positions: ...
    def validate(self, rotors: tuple[Rotor, ...]) -> None: return None

@dataclass(frozen=True)
class Clause:
    notched: tuple[int, ...] = ()

Rule = tuple[Clause, ...]

@dataclass(frozen=True)
class SlotRef:
    index: int
    inverse: bool = False
    def bind(self, rotors) -> Through:
        if not 0 <= self.index < len(rotors):
            raise ValueError(f"circuit references slot {self.index}, "
                             f"machine has {len(rotors)} rotors")
        return Through(rotors[self.index], self.index, self.inverse)

@dataclass(frozen=True)
class RuleStepper(Stepper):
    rules: tuple[Rule, ...]
    steps: tuple[int, ...] | None = None    # +1 or -1 per rotor; None = all +1

    def __call__(self, rotors, pos):
        d = self.steps or (1,) * len(rotors)
        at = tuple(p in r.notches for r, p in zip(rotors, pos))
        return tuple((p + d[i] * int(any(all(at[j] for j in c.notched) for c in rule))) % len(r.alphabet) for i, (p, r, rule) in enumerate(zip(pos, rotors, self.rules)))

    def validate(self, rotors: tuple[Rotor, ...],) -> None:
        if len(self.rules) != len(rotors):
            raise ValueError("Rules must have one entry per rotor.")
        if self.steps is not None and (len(self.steps) != len(rotors)
                                       or any(s not in (1, -1) for s in self.steps)):
            raise ValueError("steps must be +1 or -1, one per rotor")
        for rule in self.rules:
            for c in rule:
                if any(not 0 <= j < len(rotors) for j in c.notched):
                    raise ValueError("Clause references a nonexistent rotor.")

    @staticmethod
    def parse(text: str) -> tuple[Rule, ...]:
        entries = [e.strip() for e in text.replace(";", "\n").splitlines() if e.strip()]
        rules: list[Rule] = []
        for slot, e in enumerate(entries):
            low = e.lower()
            if low == "never":
                rules.append(())
            elif low == "always":
                rules.append((Clause(),))
            else:
                clauses = []
                for part in e.split("|"):
                    try:
                        idx = tuple(int(t) for t in part.split("&"))
                    except ValueError:
                        raise ValueError(f"Rotor {slot}: bad clause {part.strip()!r}") from None
                    clauses.append(Clause(idx))
                rules.append(tuple(clauses))
        return tuple(rules)

    @staticmethod
    def parse_reverse(text: str, count: int) -> tuple[int, ...] | None:
        toks = text.replace(",", " ").split()
        if not toks:
            return None
        try:
            idx = {int(t) for t in toks}
        except ValueError:
            raise ValueError(f"bad reverse list {text!r}; expected slot numbers") from None
        bad = sorted(i for i in idx if not 0 <= i < count)
        if bad:
            raise ValueError(f"reverse slots out of range 0..{count - 1}: {bad}")
        return tuple(-1 if i in idx else 1 for i in range(count))

    @staticmethod
    def format_rule(rule) -> str:
        if not rule:
            return "never"
        if any(not c.notched for c in rule):
            return "always"
        return "|".join("&".join(map(str, c.notched)) for c in rule)

@dataclass(frozen=True)
class CircuitStepper(Stepper):
    base: RuleStepper                      # steps the side rotors by notch rules
    circuit: tuple[Fixed | SlotRef, ...]
    inputs: str                            # live wires entering the circuit
    targets: tuple[tuple[str, int], ...]   # (output symbol, slot it advances)
    after: bool = False                    # evaluate on base-stepped positions?

    def __call__(self, rotors, pos):
        stepped = self.base(rotors, pos)
        ref = stepped if self.after else pos
        hops = [h.bind(rotors) for h in self.circuit]
        first, last = hops[0].src_alphabet(), hops[-1].dst_alphabet()
        drive = dict(self.targets)
        adv = set()
        for c in self.inputs:
            x = first.index(c)
            for h in hops:
                x = h.apply(ref, x)
            if last[x] in drive:
                adv.add(drive[last[x]])
        dirs = self.base.steps or (1,) * len(rotors)
        return tuple((p + dirs[i] * int(i in adv)) % len(r.alphabet)for i, (p, r) in enumerate(zip(stepped, rotors)))

    def validate(self, rotors):
        self.base.validate(rotors)
        hops = [h.bind(rotors) for h in self.circuit]      # also range-checks slots
        for i, (a, b) in enumerate(zip(hops, hops[1:])):
            if a.dst_alphabet() != b.src_alphabet():
                raise ValueError(f"circuit hop {i} outputs {a.dst_alphabet()!r} but "
                                 f"hop {i + 1} expects {b.src_alphabet()!r}")
        if not self.inputs or any(c not in hops[0].src_alphabet() for c in self.inputs):
            raise ValueError("inputs must be a non-empty set of circuit-entry symbols")
        for c, slot in self.targets:
            if c not in hops[-1].dst_alphabet():
                raise ValueError(f"target symbol {c!r} not in the circuit's output alphabet")
            if not 0 <= slot < len(rotors):
                raise ValueError(f"target slot {slot} out of range")
            if self.base.rules[slot]:
                raise ValueError(f"slot {slot} is driven by the circuit, "
                                 "so its base rule must be 'never'")

# Machine dataclass
@dataclass(frozen=True)
class Machine:
    rotors: tuple[Rotor, ...]; path: tuple[Stage, ...]; stepper: Stepper; roles: tuple[str, ...] = ()

    @cached_property
    def inv_path(self) -> tuple[Stage, ...]:
        return tuple(s.inverted() for s in reversed(self.path))

    @property
    def in_alphabet(self):
        return self.path[0].src_alphabet()

    @property
    def out_alphabet(self):
        return self.path[-1].dst_alphabet()

    def press(self, pos: Positions, x: int, decrypt=False) -> tuple[Positions, int]:
        pos = self.stepper(self.rotors, pos)   # step BEFORE encrypting
        for st in (self.path if not decrypt else self.inv_path):
            x = st.apply(pos, x)
        return pos, x

    def encode_pos(self, s: str) -> Positions:
        if len(s) != len(self.rotors):
            raise ValueError(f"positions has {len(s)} entries, machine has {len(self.rotors)} rotors")
        out = []
        for i, (r, c) in enumerate(zip(self.rotors, s)):
            j = r.alphabet.find(c)
            if j < 0:
                raise ValueError(f"rotor {i}: {c!r} is not in its alphabet")
            out.append(j)
        return tuple(out)

    def decode_pos(self, pos: Positions) -> str:
        return "".join(r.alphabet[p] for r, p in zip(self.rotors, pos))

    @staticmethod
    def describe_stage(s: Stage) -> str:
        if isinstance(s, Through):
            return f"rotor slot {s.index} {'inverse' if s.inverse else 'forward'}"
        if isinstance(s, Fixed):
            if len(s.src) != len(s.dst):
                return f"fixed {len(s.src)}->{len(s.dst)}, changes alphabet"
            n = len(s.perm)
            tag = ("involution" if all(s.perm[s.perm[j]] == j for j in range(n))
                   else "not an involution")
            fp = sum(s.perm[j] == j for j in range(n))
            return f"fixed {n}->{n}, {tag}" + (f", {fp} fixed points" if fp else "")
        return f"{type(s).__name__} {s.src_alphabet()!r} -> {s.dst_alphabet()!r}"


    def describe(self) -> str:
        ia, oa = self.in_alphabet, self.out_alphabet
        out = [f"Alphabet: {ia}" if ia == oa else f"Input alphabet:  {ia}\nOutput alphabet: {oa}"]

    # resolve the stepper to something printable
        st = self.stepper
        circ = st if isinstance(st, CircuitStepper) else None
        base = circ.base if circ else st
        if isinstance(base, PresetStepper):
            base = _preset(base.kind, base.k, len(self.rotors))
        rules = base.rules if isinstance(base, RuleStepper) else None
        dirs = (base.steps if isinstance(base, RuleStepper) else None) or (1,) * len(self.rotors)
        driven = {}
        if circ:
            for sym, slot in circ.targets:
                driven.setdefault(slot, []).append(sym)

        out.append(f"\nSlots ({len(self.rotors)}; the positions string needs "
                   f"{len(self.rotors)} characters, slot 0 first):")
        out.append("  slot  role       size  ring  notches    step  rule")
        for i, r in enumerate(self.rotors):
            role = self.roles[i] if i < len(self.roles) else "?"
            notches = "".join(r.alphabet[j] for j in sorted(r.notches)) or "-"
            rule = RuleStepper.format_rule(rules[i]) if rules else "?"
            if i in driven:
                rule += f" + circuit({''.join(driven[i])})"
            out.append(f"  {i:<5} {role:<10} {len(r.alphabet):<5} {r.ring:<5} "
                       f"{notches:<10} {dirs[i]:+d}    {rule}")

        if circ:
            hops = " ".join(f"{h.index}{chr(39) if h.inverse else ''}" if isinstance(h, SlotRef) else f"map({len(h.src)}->{len(h.dst)})" for h in circ.circuit)
            out.append(f"\nCircuit: {hops}   Live inputs: {circ.inputs}   after_base: {circ.after}")

        out.append(f"\nPath ({len(self.path)} stages):")
        for k, s in enumerate(self.path, 1):
            out.append(f"  {k}. {Machine.describe_stage(s)}")

        notes = []
        if rules:
            notes += [f"slot {i} never steps on its own" for i, ru in enumerate(rules) if not ru and i not in driven]
        if not any(isinstance(s, Fixed) and s is not self.path[0] for s in self.path[1:]) and \
                len(self.path) == len(set(map(id, self.path))):
            notes.append("path has no repeated stages: likely non-reflecting, so decrypt mode is required")
        if notes:
            out.append("\nNotes:\n" + "\n".join(f"  - {n}" for n in notes))
        return "\n".join(out)

@dataclass(frozen=True)
class StartPos:
    text: str



#==================================================================
#
# From this point onward, the ComfyUI node stuff begins
#
#===================================================================

class InitNode:
    CATEGORY = "ARG Toolkit/Cryptography/Classical/Rotor Machines"
    FUNCTION = "execute"
    COMMON_ALIASES = ["rotor machine", "rotor cipher", "cipher machine", "enigma", "encryption"]

    # Check a set of wiring against the alphabet
    @staticmethod
    def perm_wiring(alphabet: str, string:str, type: str) -> Perm:
        index = {char: i for i, char in enumerate(alphabet)}
        bad = sorted({char for char in string if char not in index})
        if bad:
            raise ValueError(f"{type}: symbols not in alphabet: {bad}")
        return tuple(index[c] for c in string)

    # Inversion of a permutation for decrypting a message
    @staticmethod
    def perm_invert(permutation: Perm) -> Perm:
        output = [0] * len(permutation)
        for index, variant in enumerate(permutation):
            output[variant] = index
        return tuple(output)

    @staticmethod
    def str_cleanup(string: str):
        return "".join(string.split())

    def odometer(k: int, total: int | None = None) -> RuleStepper:
        """Rightmost k rotors carry on notch; the rest are fixed."""
        total = k if total is None else total
        first = total - k
        rules: list[Rule] = [()] * first
        for i in range(first, total):
            rules.append((Clause(tuple(range(i + 1, total))),))
        return RuleStepper(tuple(rules))

    @staticmethod
    def enigma(k: int = 3, total: int | None = None) -> RuleStepper:
        total = total or k
        first = total - k
        rules: list[Rule] = [()] * first
        for i in range(first, total):
            if i == total - 1:
                rules.append((Clause(),))
            elif i == first:
                rules.append((Clause((i + 1,)),))
            else:
                rules.append((Clause((i + 1,)), Clause((i,))))
        return RuleStepper(tuple(rules))

    @staticmethod
    def check_alphabet(alphabet: str) -> int:
        if not alphabet or len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet must be non-empty with unique symbols")
        return len(alphabet)

    @staticmethod
    def _fold(c: str) -> str:
        u = c.upper()
        return u if len(u) == 1 else c

    @staticmethod
    def parse_circuit(text, maps):
        hops = []
        for tok in text.split():
            if tok in maps:
                if maps[tok] is None:
                    raise ValueError(f"Circuit uses {tok!r} but no map is connected to it")
                hops.append(maps[tok])
            else:
                try:
                    hops.append(SlotRef(int(tok.rstrip("'")), tok.endswith("'")))
                except ValueError:
                    raise ValueError(f"Bad circuit token {tok!r}") from None
        if not hops:
            raise ValueError("Circuit is empty.")
        return tuple(hops)

    @staticmethod
    def parse_targets(text):
        out = []
        for group in text.split():
            syms, sep, slot = group.partition("=")
            try:
                if not sep:
                    raise ValueError
                n = int(slot)
            except ValueError:
                raise ValueError(f"Bad target group {group!r}; expected symbols=slot") from None
            out += [(c, n) for c in syms]
        chars = [c for c, _ in out]
        if len(set(chars)) != len(chars):
            raise ValueError("An output symbol may drive only one rotor")
        return tuple(out)


## Rotors
class RotorCipherRotor(InitNode):
    RETURN_TYPES = ("ROTORS",)
    RETURN_NAMES = ("rotor",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["rotor", "wheel", "scrambler"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "alphabet": ("STRING", {"default": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}),
                "wiring": ("STRING", {"default": "EKMFLGDQVZNTOWYHXUSPAIBRCJ"}),
                "notches": ("STRING", {"default": "Q"}),
                "ring": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "invert": ("BOOLEAN", {"default": False}),
                },
            "optional": {
                "previous_rotor": ("ROTORS", {"forceInput": True})
            }
        }

    def execute(self, alphabet, wiring, notches, ring, invert, previous_rotor=None):
        alphabet = InitNode.str_cleanup(alphabet)
        n = InitNode.check_alphabet(alphabet=alphabet)

        w = InitNode.perm_wiring(alphabet, wiring, type="Wiring")
        if len(w) != n or len(set(w)) != n:
            raise ValueError(f"Wiring must use each of the {n} alphabet symbols exactly once")

        if not 0 <= ring < n:
            raise ValueError(f"Ring must be in [0, {n - 1}]")

        fwd, inv = w, InitNode.perm_invert(w)
        if invert:
            fwd, inv = inv, fwd

        rotor= Rotor(alphabet, fwd, inv, frozenset(InitNode.perm_wiring(alphabet, InitNode.str_cleanup(notches), "Notches")), ring)
        return (((*previous_rotor, rotor) if previous_rotor else (rotor,)),)

## Fixed permutations
class RotorCipherPerm(InitNode):
    RETURN_TYPES = ("PERMUTATION",)
    RETURN_NAMES = ("perm_obj",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["reflector", "entry wheel", "etw", "ukw", "permutation", "wiring"]


    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "alphabet": ("STRING", {"default": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}),
                "wiring": ("STRING", {"default": "EKMFLGDQVZNTOWYHXUSPAIBRCJ"})
            }
        }

    def execute(self, alphabet, wiring):
        alphabet = InitNode.str_cleanup(alphabet)
        n = len(alphabet)
        w = InitNode.perm_wiring(alphabet, InitNode.str_cleanup(wiring), "Wiring")
        if len(w) != n or len(set(w)) != n:
            raise ValueError (f"Wiring must use every symbols exactly once. Required {n}, got {len(w)}.")
        return (Fixed(alphabet, alphabet, w),)

## Mapper node for cases that needs to convert between different alphabet sizes
class RotorCipherMap(InitNode):
    RETURN_TYPES = ("PERMUTATION",)
    RETURN_NAMES = ("perm_obj",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["alphabet map", "grouping", "mapping stage", "relabel", "permutation"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "src_alphabet": ("STRING", {"default": "ABCEDEFGHIJKLMNOPQRSTUVWXYZ"}),
                "dst_alphabet": ("STRING", {"default": "ABCEDEFGHIJKLMNOPQRSTUVWXYZ"}),
                "mapping": ("STRING", {"default": ""})
            }
        }

    def execute(self, src_alphabet, dst_alphabet, mapping):
        src, dst = map(InitNode.str_cleanup, (src_alphabet, dst_alphabet))
        InitNode.check_alphabet(src); InitNode.check_alphabet(dst)
        m = InitNode.perm_wiring(dst, InitNode.str_cleanup(mapping), "Mapping")
        if len(m) != len(src):
            raise ValueError(f"Mapping needs one symbol per source symbol ({len(src)})")
        return (Fixed(src, dst, m),)

# Machine node to construct the necessary machine to encrypt/decrypt

class RotorCipherMachine(InitNode):
    RETURN_TYPES = ("MACHINE",)
    RETURN_NAMES = ("cipher_machine",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["assemble machine", "rotor stack", "build machine"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "rotors": ("ROTORS", {"forceInput": True}),
                "stepper": ("STEPPER", {"forceInput": True})
                },
            "optional": {
                "entry": ("PERMUTATION", {"forceInput": True, "tooltip": "Entry wheel (ETW). Applied first on the way in, and inverted on the way out. Identity for Wehrmacht Enigmas."}),
                "reflector": ("PERMUTATION", {"forceInput": True, "tooltip": "Static reflector (UKW). Must be an involution. Use this OR reflector_rotor, not both."}),
                "reflector_rotor": ("PERMUTATION", {"forceInput": True, "tooltip": "Reflector that takes a position (slot 0). A chain of exactly one rotor with an involutive wiring."}),
                "plugboard": ("PERMUTATION", {"forceInput": True, "tooltip": "Steckerbrett. Applied outermost, before the entry wheel. Must be an involution."}),
                "auxilliary_rotors": ("ROTORS", {"forceInput": True}),
                },
        }

    def execute(self, rotors, stepper, entry=None, reflector=None, reflector_rotor=None, plugboard=None, auxilliary_rotors=None):
        if reflector is not None and reflector_rotor is not None:
            raise ValueError("Use either a static reflector or a reflector rotor, not both.")

        ref_rot = None
        if reflector_rotor is not None:
            if len(reflector_rotor) != 1 or not isinstance(reflector_rotor[0], Rotor):
                raise ValueError("reflector_rotor must be a chain of exactly one rotor.")
            ref_rot = reflector_rotor[0]
            if any(ref_rot.fwd[ref_rot.fwd[i]] != i for i in range(len(ref_rot.fwd))):
                raise ValueError("Reflector rotor wiring must be an involution.")

        slot = 1 if ref_rot else 0                  # slot 0 reserved for the reflector
        stages = []
        for item in rotors:
            if isinstance(item, Rotor):
                stages.append(Through(item, slot)); slot += 1
            else:
                stages.append(item)
        path_rotors = tuple(i for i in rotors if isinstance(i, Rotor))
        aux_rotors = tuple(auxilliary_rotors) if auxilliary_rotors else ()
        if not all(isinstance(r, Rotor) for r in aux_rotors):
            raise ValueError("aux must be a chain of rotors only")
        if aux_rotors and isinstance(stepper, PresetStepper):
            raise ValueError("Preset steppers count every rotor, aux included. Please use a rule or circuit stepper with aux rotors.")
        rotors = ((ref_rot,) if ref_rot else ()) + path_rotors + aux_rotors
        if not rotors:
            raise ValueError("Machine needs at least one rotor")

        for name, f in (("reflector", reflector), ("plugboard", plugboard)):
            if f is not None:
                if f.src != f.dst:
                    raise ValueError(f"{name} must map an alphabet to itself")
                if any(f.perm[f.perm[i]] != i for i in range(len(f.perm))):
                    raise ValueError(f"{name} must be an involution")

        pre = [s for s in (plugboard, entry) if s is not None]
        fwd = (*pre, *reversed(stages))
        mid = Through(ref_rot, 0) if ref_rot else reflector
        path = fwd if mid is None else (*fwd, mid, *(s.inverted() for s in reversed(fwd)))

        for i, (a, b) in enumerate(zip(path, path[1:])):
            if a.dst_alphabet() != b.src_alphabet():
                raise ValueError(f"stage {i} outputs {a.dst_alphabet()!r} but stage {i + 1} "
                             f"expects {b.src_alphabet()!r}; add a mapping stage between them")
        stepper.validate(rotors)
        roles = (("reflector",) if ref_rot else ()) + ("path",) * len(path_rotors) + ("aux",) * len(aux_rotors)
        return (Machine(rotors, path, stepper, roles),)

# Rotor stepping rules

@lru_cache(maxsize=None)
def _preset(kind: str, k: int, total: int) -> RuleStepper:
    return (InitNode.enigma if kind == "Enigma" else InitNode.odometer)(k, total)

@dataclass(frozen=True)
class PresetStepper(Stepper):
    kind: str      # "Enigma" | "Odometer"
    k: int

    def __call__(self, rotors, pos):
        return _preset(self.kind, self.k, len(rotors))(rotors, pos)

    def validate(self, rotors):
        if not 1 <= self.k <= len(rotors):
            raise ValueError(f"k must be in [1, {len(rotors)}] for this machine")
        _preset(self.kind, self.k, len(rotors)).validate(rotors)

class RotorCipherPresetStepper(InitNode):
    RETURN_TYPES = ("STEPPER",)
    RETURN_NAMED = ("stepper",)

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "type": (["Enigma", "Odometer"], {"default": "Enigma",}),
            "k": ("INT", {"default": 3, "min": 1, "max": 64, "tooltip": "The rightmost k rotor steps."}),
        }}

    def execute(self, type, k):
        return (PresetStepper(type, k),)


class RotorCipherRuleStepper(InitNode):
    RETURN_TYPES = ("STEPPER",)
    RETURN_NAMES = ("stepper",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["stepping", "turnover", "notch rules", "odometer", "double step"]

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "rules": ("STRING", {"multiline": True, "default": "1\n2|1\nalways"}),
            "reverse": ("STRING", {"default": "", "multiline": False})
        }}

    def execute(self, rules: str, reverse=""):
        parsed_rules = RuleStepper.parse(rules)
        return (RuleStepper(parsed_rules, RuleStepper.parse_reverse(reverse, len(parsed_rules))),)

class RotorCipherPosition(InitNode):
    RETURN_TYPES = ("POSITIONS",)
    RETURN_NAMES = ("rotor_pos",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["start positions", "key setting", "grundstellung", "window letters"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positions": ("STRING", {"default": "AAA", "tooltip": "From left to right, where the rotors will start at, whitespace permitting."}),
            }
        }

    def execute(self, positions):
        position = self.str_cleanup(positions)
        if not position:
            raise ValueError("Positions must list at least one rotor.")
        return (StartPos(position),)

class RotorCipherCircuitStepper(InitNode):
    RETURN_TYPES = ("STEPPER",)
    RETURN_NAMES = ("circuit_stepper",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["irregular stepping", "control circuit", "driven stepping"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": ("STEPPER", {"forceInput": True}),
                "circuit": ("STRING", {"default": "3"}),
                "inputs": ("STRING", {"default": "A"}),
                "targets": ("STRING", {"default": "E=2"}),
                "evaluate_after_base": ("BOOLEAN", {"default": False}),
                },
            "optional": {
                "map_a": ("PERMOBJ", {"forceInput": True}),
                "map_b": ("PERMOBJ", {"forceInput": True})
                }
            }

    def execute(self, base, circuit, inputs, targets, evaluate_after_base, map_a=None, map_b=None):
        if not isinstance(base, RuleStepper):
            raise ValueError("base must be a rule stepper (it steps the side rotors)")
        return (CircuitStepper(base, InitNode.parse_circuit(circuit, {"a": map_a, "b": map_b}), InitNode.str_cleanup(inputs), InitNode.parse_targets(targets), evaluate_after_base),)


# Encrypt/Decrypt function node
class RotorCipherEncrypt(InitNode):
    RETURN_TYPES = ("STRING", "POSITIONS",)
    RETURN_NAMES = ("encrypted_msg", "rotor_pos",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["encrypt", "decrypt", "cipher text", "plaintext", "run machine"]

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "machine": ("MACHINE", {"forceInput": True,}),
            "positions": ("POSITIONS", {"forceInput": True,}),
            "text": ("STRING", {"multiline": True, "default": "Hello World!", "placeholder": "Type your message here..."}),
            "preserve": ("BOOLEAN", {"default": False, "tooltip": "When set to true, attempt to preserve the form of the message, including case and punctuation marks."}),
            "mode": ("BOOLEAN", {"default": False, "label_on": "Decrypt", "label_off": "Encrypt", "tooltip": "Whether to encrypt or decrypt the message."})
        }}

    def execute(self, machine: Machine, positions, text, preserve, mode=False):
        src, dst = ((machine.out_alphabet, machine.in_alphabet) if mode else (machine.in_alphabet, machine.out_alphabet))
        for a in (src, dst):
            if any(InitNode._fold(c) != c for c in a):
                raise ValueError("alphabets must be uppercase/uncased: input is case-folded")

        idx = {c: i for i, c in enumerate(src)}
        pos = machine.encode_pos(positions.text)

        out = []
        for ch in text:
            i = idx.get(InitNode._fold(ch))
            if i is None:
                if preserve:
                    out.append(ch)
                continue
            pos, y = machine.press(pos, i, mode)
            c = dst[y]
            out.append(c.lower() if preserve and ch != InitNode._fold(ch) else c)
        return ("".join(out), StartPos(machine.decode_pos(pos)))

class RotorCipherDescribe(InitNode):
    RETURN_TYPES = ("STRING",)
    RETURN_TYPES = ("description",)
    SEARCH_ALIASES = InitNode.COMMON_ALIASES + ["describe", "inspect", "debug", "machine layout", "slots"]
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls): return {"required": {"machine": ("MACHINE",)}}

    def execute(self, machine: Machine):
        return (machine.describe(),)

NODE_CLASS_MAPPINGS = {
    "RotorCipherRotor": RotorCipherRotor,
    "RotorCipherPerm": RotorCipherPerm,
    "RotorCipherMachine": RotorCipherMachine,
    "RotorCipherRuleStepper": RotorCipherRuleStepper,
    "RotorCipherPresetStepper": RotorCipherPresetStepper,
    "RotorCipherPosition": RotorCipherPosition,
    "RotorCipherEncrypt": RotorCipherEncrypt,
    "RotorCipherMapper": RotorCipherMap,
    "RotorCipherDescribe": RotorCipherDescribe,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RotorCipherRotor": "Rotor Machine Rotor",
    "RotorCipherPerm": "Rotor Machine Permutation",
    "RotorCipherMachine": "Rotor Machine State",
    "RotorCipherRuleStepper": "Rotor Machine Rule-Based Stepper",
    "RotorCipherPresetStepper": "Rotor Machine Preset Stepper",
    "RotorCipherPosition": "Rotor Machine Positions",
    "RotorCipherEncrypt": "Rotor Machine Encrypt/Decrypt",
    "RotorCipherMapper": "Rotor Machine Rotor Mapper",
    "RotorCipherDescribe": "Rotor Machine State Descriptor",
}
