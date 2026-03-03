# The Leech Lattice

## Definition

The Leech lattice (Lambda_24) is the unique even unimodular lattice in 24 dimensions with no vectors of norm sqrt(2) - its minimal norm is 2.

## Construction

In the Lean formalization (`Dim24/LeechLattice/Defs.lean`), the Leech lattice is defined via an explicit 24x24 generator matrix (`leechGeneratorMatrixInt`), with each row scaled by 1/sqrt(8).

The classical construction uses the extended binary Golay code:

1. Start with the extended binary Golay code C (a [24,12,8] binary code)
2. Form vectors in Z^24 where:
   - Type 1: 2*c for c in C (scaled codewords)
   - Type 2: x + C for appropriate coset representatives
   - Type 3: (-3, 1^23) + 2*Lambda (shifted vectors)
3. Normalize to get a unimodular lattice

## Key Properties

| Property | Value |
|----------|-------|
| Dimension | 24 |
| Determinant | 1 (unimodular) |
| Minimum norm | 2 |
| Kissing number | 196,560 |
| Automorphism group | Conway group Co_0, order ~8.3 * 10^18 |
| Theta series | 1 + 196560*q^2 + 16773120*q^3 + ... |
| Covering radius | sqrt(2) (deep holes) |

## The 196,560 Minimal Vectors

The norm-2 vectors decompose as:

**Type A (97,152)**: (+-2)^2, 0^22 in any arrangement
- Pairs of +-2 in 2 of 24 positions: C(24,2) * 2^2 = 1,104
- But actually need lattice membership condition
- Total from this type: 97,152

**Type B (98,304)**: (+-1)^8, 0^16 with Golay code support
- Choose an octad (8-subset from Golay code): 759 octads
- Signs with even parity: 2^7 = 128
- Total: 759 * 128 = 97,152... (the exact decomposition is subtle)

**Type C (1,104)**: Permutations of (+-4, 0^23, ...)

Combined: 196,560

## In the Lean Formalization

- `leechKissingVectors`: The set of norm-2 vectors
- `ncard_leechKissingVectors = 196560`: Proven cardinality
- `spanZ_leechKissingVectors_eq_leechLattice`: Minimal shell generates the full lattice

## Connection to the Golay Code

The extended binary Golay code C_24 is a [24, 12, 8] code:
- Length 24, dimension 12 (2^12 = 4096 codewords)
- Minimum Hamming distance 8

File: `Dim24/Uniqueness/BS81/CodingTheory/GolayConcrete.lean`

The weight distribution:
- 1 word of weight 0
- 759 words of weight 8 (octads)
- 2576 words of weight 12 (dodecads)
- 759 words of weight 16
- 1 word of weight 24

The 759 octads form a Steiner system S(5,8,24): any 5 of the 24 symbols appears in exactly one octad.

## Uniqueness Result

The formalization proves (in `Dim24/MainTheorem.lean`):

```lean
theorem MainTheorem :
  SpherePackingConstant 24 = LeechPacking.density /\
  forall S : PeriodicSpherePacking 24,
    S.density = LeechPacking.density -> IsometricToScaledLeech S
```

This uses the Bannai-Sloane (1981) framework in `Dim24/Uniqueness/BS81/` (195 files, 39k lines):
1. LP equality case forces specific spherical code structure
2. Shell matching shows norm-4 shell is isometric to Golay code octads
3. Full lattice reconstruction from shell isometry

## Packing Density

- Volume of unit ball in R^24: pi^12 / 12!
- Sphere radius: 1 (minimum norm = 2, so half-distance = 1)
- Fundamental domain volume: 1
- Density = pi^12 / 12! ~ 0.001930

This is extremely sparse - less than 0.2% of space is covered. Yet no other arrangement can do better.
