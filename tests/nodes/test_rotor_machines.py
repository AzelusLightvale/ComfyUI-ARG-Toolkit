import pytest
from src.rotor_machines import RotorCipherRotor, RotorCipherPerm, RotorCipherMachine, RotorCipherPosition, RotorCipherEncrypt, RotorCipherPresetStepper, RotorCipherRuleStepper, RotorCipherMap, InitNode, RuleStepper, PresetStepper, Through, RotorCipherCircuitStepper

# Setup machines and helpers for each major tests
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROTORS = [("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),   # I
          ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),   # II
          ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")]   # III
REFL_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def machine(rings=(0, 0, 0), notches=True, stepper=None):
    chain = None
    for (w, n), r in zip(ROTORS, rings):
        (chain,) = RotorCipherRotor().execute(A, w, n if notches else "", r, False, previous_rotor=chain)
    (refl,) = RotorCipherPerm().execute(A, REFL_B)
    return RotorCipherMachine().execute(chain, stepper or PresetStepper("Enigma", 3), reflector=refl)[0]

def enc(m, start, text, preserve=False):
    (p,) = RotorCipherPosition().execute(start)
    out, final = RotorCipherEncrypt().execute(m, p, text, preserve)
    return out, final.text

def run(m, pos, text, decrypt=False):
    out = []
    for c in text:
        pos, y = m.press(pos, A.index(c), decrypt=decrypt)
        out.append(A[y])
    return "".join(out)

def aux_machine(base_rules="never\nnever\nnever\nnever", after=False, targets="E=2", reverse=""):
    chain = None
    for w, n in ROTORS:
        (chain,) = RotorCipherRotor().execute(A, w, n, 0, False, previous_rotor=chain)
    (aux,) = RotorCipherRotor().execute(A, ROTORS[0][0], "", 0, False)   # a 1-rotor chain
    (refl,) = RotorCipherPerm().execute(A, REFL_B)
    (base,) = RotorCipherRuleStepper().execute(base_rules, reverse)
    (st,) = RotorCipherCircuitStepper().execute(base, "3", "A", targets, after)
    return RotorCipherMachine().execute(chain, st, reflector=refl, auxilliary_rotors=aux)[0]

def one_key(m, start):
    pos, _ = m.press(m.encode_pos(start), 0)
    return m.decode_pos(pos)

def one_rotor(wiring):
    return RotorCipherRotor().execute(A, wiring, "", 0, False)[0][0]

# --- published-style vector -------------------------------------------
def test_enigma_i_known_vector():
    # Enigma I, I-II-III, UKW-B, rings AAA, start AAA. Widely cited; confirm
    # against Crypto Museum's simulator if it ever fails.
    assert enc(machine(), "AAA", "AAAAA")[0] == "BDZGO"

# --- stepping -----------------------------------------------------------
def test_double_step_sequence():
    m, pos, seen = machine(), (0, 3, 20), []       # ADU
    for _ in range(3):
        pos = m.stepper(m.rotors, pos)
        seen.append("".join(A[p] for p in pos))
    assert seen == ["ADV", "AEW", "BFX"]

def test_odometer_does_not_double_step():
    m = machine(stepper=PresetStepper("Odometer", 3))
    pos = m.stepper(m.rotors, (0, 3, 21))      # ADV: right at notch
    assert "".join(A[p] for p in pos) == "AEW"
    pos = m.stepper(m.rotors, pos)
    assert "".join(A[p] for p in pos) == "AEX"      # middle at notch, no carry

def test_rule_string_matches_preset():
    m = machine()
    rs = RuleStepper(RuleStepper.parse("1\n2|1\nalways"))
    for pos in [(0, 3, 20), (0, 4, 22), (16, 4, 21), (0, 0, 0)]:
        assert rs(m.rotors, pos) == m.stepper(m.rotors, pos)

# --- cipher properties --------------------------------------------------
def test_reciprocity():
    m = machine()
    ct, _ = enc(m, "QEV", "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG")
    assert enc(m, "QEV", ct)[0] == "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"

def test_no_self_encryption():
    # holds for Enigma-style reflector B (no fixed points)
    m = machine()
    text = "A" * 200
    assert "A" not in enc(m, "AAA", text)[0]

def test_ring_offset_convention():
    # With no notches only the fast rotor steps, so ring r + position p must
    # equal ring 0 + position (p - r). This is a consistency check of the
    # pos - ring convention, NOT a published vector; add one from a real
    # simulator with nonzero rings for external confirmation.
    a = enc(machine(rings=(1, 2, 3), notches=False), "BDF", "HELLOWORLD")
    b = enc(machine(rings=(0, 0, 0), notches=False), "ABC", "HELLOWORLD")
    c = enc(machine(rings=(0, 0, 0), notches=False), "BDF", "HELLOWORLD")
    print(a[0] == c[0])
    assert a[0] == b[0]

def test_ring_single_rotor_external():
    ((r0,),) = RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 0, False)
    ((r1,),) = RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 1, False)
    assert A[Through(r0, 0).apply((0,), 0)] == "E"
    assert A[Through(r1, 0).apply((0,), 0)] == "K"

# --- modes --------------------------------------------------------------
def test_skip_mode_drops_and_uppercases():
    m = machine()
    out, _ = enc(m, "AAA", "Hello, World!")
    assert out == enc(m, "AAA", "HELLOWORLD")[0]

def test_preserve_mode_format():
    m = machine()
    text = "Hello, World!"
    out, _ = enc(m, "AAA", text, preserve=True)
    assert len(out) == len(text)
    for i, c in enumerate(text):
        assert (out[i] == c) if not c.isalpha() else (out[i].isupper() == c.isupper())

def test_preserve_round_trip():
    m = machine()
    text = "Hello, World! Attack at Dawn."
    ct, _ = enc(m, "MCK", text, preserve=True)
    assert enc(m, "MCK", ct, preserve=True)[0] == text

def test_preserve_and_skip_agree_on_letters():
    m = machine()
    p, _ = enc(m, "AAA", "Hi there", preserve=True)
    s, _ = enc(m, "AAA", "Hi there")
    assert "".join(c for c in p if c.isalpha()).upper() == s

def test_chaining_continues_stream():
    m = machine()
    whole, final = enc(m, "AAA", "ABCDEFGH")
    first, mid = enc(m, "AAA", "ABCD")
    second, end = enc(m, mid, "EFGH")
    assert first + second == whole and end == final

# --- validation ---------------------------------------------------------
def test_bad_wiring_rejected():
    with pytest.raises(ValueError):
        RotorCipherRotor().execute(A, "AB" + A[2:-1], "Q", 0, False)      # too short
    with pytest.raises(ValueError):
        RotorCipherRotor().execute(A, "A" * 26, "Q", 0, False)            # repeats

def test_ring_out_of_range():
    with pytest.raises(ValueError):
        RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 26, False)

def test_non_involution_reflector_rejected():
    (chain,) = RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 0, False)
    (bad,) = RotorCipherPerm().execute(A, A[1:] + A[0])                   # shift by one
    with pytest.raises(ValueError):
        RotorCipherMachine().execute(chain, RotorCipherPresetStepper().execute("Odometer", 1), reflector=bad)

def test_alphabet_mismatch_across_rotors():
    (c1,) = RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 0, False)
    rev = A[::-1]
    with pytest.raises(ValueError):
        (c2,) = RotorCipherRotor().execute(rev, rev, "Q", 0, False, previous_rotor=c1)
        RotorCipherMachine().execute(c2, RotorCipherPresetStepper().execute("Odometer", 2))

def test_positions_length_mismatch():
    m = machine()
    with pytest.raises(ValueError):
        enc(m, "AA", "HELLO")

def test_positions_outside_rotor_alphabet():
    m = machine()
    (p,) = RotorCipherPosition().execute("123")
    with pytest.raises(ValueError):
        RotorCipherEncrypt().execute(m, p, "HELLO", False)

def test_preset_k_too_large():
    (chain,) = RotorCipherRotor().execute(A, ROTORS[0][0], "Q", 0, False)
    with pytest.raises(ValueError):
        RotorCipherMachine().execute(chain, PresetStepper("Enigma", 3))

# --- decryption --------------------------------------------------

def no_reflector_machine():
    chain = None
    for w, n in ROTORS:
        (chain,) = RotorCipherRotor().execute(A, w, n, 0, False, previous_rotor=chain)
    (plug,) = RotorCipherPerm().execute(A, "BACDEFGHIJKLMNOPQRSTUVWXYZ")   # swaps A,B
    (entry,) = RotorCipherPerm().execute(A, A[1:] + A[0])                  # not an involution, on purpose
    return RotorCipherMachine().execute(chain, PresetStepper("Enigma", 3),
                                        entry=entry, plugboard=plug)[0]

def test_non_reflecting_round_trip():
    m, start = no_reflector_machine(), (16, 4, 21)       # start near notches
    text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG" * 3
    ct = run(m, start, text)
    assert ct != text
    assert run(m, start, ct, decrypt=True) == text

def test_non_reflecting_is_not_self_inverse():
    m, start = no_reflector_machine(), (0, 0, 0)
    ct = run(m, start, "HELLOWORLD")
    assert run(m, start, ct) != "HELLOWORLD"      # decrypting needs decrypt=True

def test_reflecting_decrypt_equals_encrypt():
    m, start = machine(), (0, 3, 20)
    text = "ATTACKATDAWN"
    assert run(m, start, text) == run(m, start, text, decrypt=True)

def test_positioned_reflector_matches_static_at_A():
    chain = None
    for w, n in ROTORS:
        (chain,) = RotorCipherRotor().execute(A, w, n, 0, False, previous_rotor=chain)
    (rr,) = RotorCipherRotor().execute(A, REFL_B, "", 0, False)
    m = RotorCipherMachine().execute(chain, PresetStepper("Enigma", 3), reflector_rotor=rr)[0]
    assert run(m, (0, 0, 0, 0), "HELLOWORLD") == run(machine(), (0, 0, 0), "HELLOWORLD")

def test_positioned_reflector_reciprocal_and_position_dependent():
    chain = None
    for w, n in ROTORS:
        (chain,) = RotorCipherRotor().execute(A, w, n, 0, False, previous_rotor=chain)
    (rr,) = RotorCipherRotor().execute(A, REFL_B, "", 0, False)
    m = RotorCipherMachine().execute(chain, PresetStepper("Enigma", 3), reflector_rotor=rr)[0]
    a = run(m, (5, 0, 0, 0), "ATTACKATDAWN")
    assert run(m, (5, 0, 0, 0), a) == "ATTACKATDAWN"
    assert a != run(m, (0, 0, 0, 0), "ATTACKATDAWN")

def test_mapping_stage_changes_alphabet():
    D = "0123456789"
    (chain,) = RotorCipherRotor().execute(D, "5290817346", "", 0, False)
    (ent,) = RotorCipherMap().execute(A, D, "0123456789" * 2 + "012345")
    m = RotorCipherMachine().execute(chain, PresetStepper("Odometer", 1), entry=ent)[0]
    assert (m.in_alphabet, m.out_alphabet) == (A, D)
    pos, y = m.press((0,), A.index("C"))
    assert 0 <= y < 10
    with pytest.raises(ValueError):
        m.press((0,), 0, decrypt=True)

# --- auxiliary rotors ---------------------------------------------------------------------------------------

def test_circuit_depends_on_aux_position():
    m = aux_machine()
    assert one_key(m, "AAAA") == "AABA"     # aux A -> E -> target: slot 2 steps
    assert one_key(m, "AAAB") == "AAAB"     # aux B -> J -> no step

def test_evaluate_after_base():
    rules = "never\nnever\nnever\nalways"   # aux rotor steps every key
    assert one_key(aux_machine(rules, after=False), "AAAA") == "AABB"   # evaluated at A
    assert one_key(aux_machine(rules, after=True),  "AAAA") == "AAAB"   # evaluated at B

def test_aux_reflecting_round_trip():
    m = aux_machine("never\nnever\nnever\nalways")
    start = m.encode_pos("AAAA")
    ct = run(m, start, "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG")
    assert run(m, start, ct) == "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"

def test_driven_slot_must_be_never():
    with pytest.raises(ValueError):
        aux_machine("never\nnever\nalways\nnever")      # slot 2 also driven by the circuit

def test_circuit_slot_out_of_range():
    with pytest.raises(ValueError):
        aux_machine(targets="E=9")

def test_preset_stepper_rejected_with_aux():
    chain = None
    for w, n in ROTORS:
        (chain,) = RotorCipherRotor().execute(A, w, n, 0, False, previous_rotor=chain)
    (aux,) = RotorCipherRotor().execute(A, ROTORS[0][0], "", 0, False)
    with pytest.raises(ValueError):
        RotorCipherMachine().execute(chain, PresetStepper("Enigma", 3), auxilliary_rotors=aux)

# --- reversal ---------------------------------------------------------------------------------

def test_parse_reverse():
    assert RuleStepper.parse_reverse("", 4) is None
    assert RuleStepper.parse_reverse("0 2", 4) == (-1, 1, -1, 1)
    assert RuleStepper.parse_reverse("1,3", 4) == (1, -1, 1, -1)
    with pytest.raises(ValueError):
        RuleStepper.parse_reverse("9", 4)
    with pytest.raises(ValueError):
        RuleStepper.parse_reverse("x", 4)

def test_reverse_rule_stepper():
    rs = (one_rotor(ROTORS[0][0]), one_rotor(ROTORS[0][0]))
    (st,) = RotorCipherRuleStepper().execute("always\nalways", "1")
    assert st(rs, (1, 1)) == (2, 0)       # slot 0 forward, slot 1 backward
    assert st(rs, (0, 0)) == (1, 25)      # backward wraps A -> Z

def test_reverse_circuit_driven_slot():
    m = aux_machine(targets="E=2", reverse="2")
    assert one_key(m, "AAAA") == "AAZA"

def test_no_reverse_unchanged():
    # existing behavior: a blank reverse list gives steps=None
    (st,) = RotorCipherRuleStepper().execute("1\n2|1\nalways", "")
    assert st.steps is None

# --- description ---------------------------------------------------------

def test_describe_enigma():
    d = machine().describe()
    assert "slot 0 first" in d and "2|1" in d and "always" in d
    assert "rotor slot 2 forward" in d and "involution" in d

def test_describe_aux_roles_and_circuit():
    d = aux_machine().describe()
    assert "aux" in d and "Circuit:" in d and "circuit(E)" in d
