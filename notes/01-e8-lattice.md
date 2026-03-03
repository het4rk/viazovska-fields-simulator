# The E8 Lattice

## Definition

The E8 lattice in R^8 consists of all vectors (x1, ..., x8) where:

1. **All integer coordinates**: Each xi is an integer, AND the sum x1 + ... + x8 is even
2. **All half-integer coordinates**: Each xi is a half-odd-integer (n + 1/2), AND the sum is even

Equivalently: E8 = D8 union (D8 + [1/2, 1/2, ..., 1/2])

where D8 is the checkerboard lattice (integer vectors with even coordinate sum).

## In the Lean Formalization

File: `SpherePacking/Dim8/E8/Basic.lean`

Three equivalent definitions are proven:
1. **Parity-based** (`Submodule.E8`): Z-submodule with the conditions above
2. **Matrix span** (`span_E8Matrix`): Z-span of an explicit 8x8 generator matrix
3. **Supremum form** (`E8_eq_sup`): E8 = evenLattice + span{1/2}

## Key Properties

| Property | Value |
|----------|-------|
| Dimension | 8 |
| Determinant | 1 (unimodular) |
| Minimum norm | sqrt(2) |
| Kissing number | 240 |
| Automorphism group | Weyl group W(E8), order 696,729,600 |
| Theta series | 1 + 240*q + 2160*q^2 + 6720*q^3 + ... |

## The 240 Root Vectors

The minimal vectors (norm sqrt(2)) of E8 are the 240 roots:

**Type 1 (112 vectors)**: All permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
- Choose 2 positions from 8: C(8,2) = 28
- Choose signs: 2^2 = 4
- Total: 28 * 4 = 112

**Type 2 (128 vectors)**: (+-1/2, +-1/2, +-1/2, +-1/2, +-1/2, +-1/2, +-1/2, +-1/2)
- All 2^8 = 256 sign choices, but only those with even number of minus signs
- Total: 256 / 2 = 128

Combined: 112 + 128 = 240

## Packing Density

The E8 sphere packing places non-overlapping spheres of radius sqrt(2)/2 at each lattice point.

- Volume of unit ball in R^8: pi^4 / 24
- Sphere radius: sqrt(2)/2
- Fundamental domain volume: 1 (unimodular)
- Density = vol(sphere) / vol(fund. domain) = pi^4/24 * (sqrt(2)/2)^8 / 1 = pi^4/384

## Why E8 is Special

E8 is the unique even unimodular lattice in 8 dimensions (by the classification of even unimodular lattices - they exist only in dimensions divisible by 8).

"Even" means all inner products v.v are even integers.
"Unimodular" means the fundamental domain has volume 1.

These two properties together force extremely tight packing.

## Connection to the Magic Function

In the Lean formalization (`Dim8/MagicFunction/g/`), the magic function is:

```
g = (pi * I / 8640) * a - (I / (240 * pi)) * b
```

where a and b are constructed from contour integrals of modular forms. The key results:
- g(0) = 1
- g-hat(0) = 1
- g(x) <= 0 for ||x|| >= sqrt(2)
- g-hat(x) >= 0 everywhere

This makes the LP bound tight at exactly pi^4/384.
