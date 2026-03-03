# Magic Functions

## The Core Idea

The Cohn-Elkies linear programming bound says: find a Schwartz function f on R^n such that

1. f(0) = f-hat(0) = 1 (normalized)
2. f(x) <= 0 for ||x|| >= r (non-positive outside radius r)
3. f-hat(xi) >= 0 for all xi (non-negative Fourier transform)

Then: packing density <= vol(B(r/2))

If you can find f that makes this bound EQUAL to a known lattice packing density, you've proven that lattice is optimal.

The functions that achieve this are called "magic functions."

## Dimension 8: The Function g

File: `SpherePacking/Dim8/MagicFunction/g/Basic.lean`

### Construction

g is built from two auxiliary Schwartz functions a and b:

```
g = (pi * I / 8640) * a - (I / (240 * pi)) * b
```

**Function a** (files in `Dim8/MagicFunction/a/`):
- Built from 6 contour integrals I_1' through I_6'
- Uses a modular form phi_0'' (derived from Eisenstein series)
- Integral representation involving the upper half-plane

**Function b** (files in `Dim8/MagicFunction/b/`):
- Built from 6 contour integrals J_1' through J_6'
- Uses psi_T' and psi_I' (theta function derivatives)
- Complementary to a in providing the sign conditions

### Key Properties

- `g(0) = 1` (normalization at origin)
- `g-hat(0) = 1` (Fourier transform normalization)
- g is real-valued (despite complex construction)
- g-hat is real-valued
- g(x) <= 0 for ||x|| >= sqrt(2) (non-positive outside E8 minimum distance)
- g-hat(xi) >= 0 for all xi (everywhere non-negative transform)

### Scaled Version

The actual function applied to the LP bound is `scaledMagic`:

```
scaledMagic(x) = g(x / sqrt(2))
```

This gives:
- scaledMagic(0) = 1
- fourier(scaledMagic)(0) = 1/16
- Ratio = 16 (the key eigenvalue)
- Bound = vol(B(1/2)) in dim 8 * 16 = pi^4/384

## Dimension 24: The Function F

Files: `SpherePacking/Dim24/MagicFunction/` (176 files, 45k lines)

### Construction

Three nested functions:

**Function A** (the Hecke eigenfunction):
- 6 contour integrals with modular form kernels
- Files in `Dim24/MagicFunction/A/`
- Built via Schwartz function theory: smoothness + rapid decay
- Must be an eigenfunction of Fourier transform with double zeros

**Function B** (auxiliary):
- Similar integral construction
- Files in `Dim24/MagicFunction/B/`
- Provides complementary spectral properties

**Function F** (final magic function):
- Combination of A and B satisfying all LP conditions
- Files in `Dim24/MagicFunction/F/`
- Sign conditions verified via Laplace transforms

### Why Dim 24 is Harder

The dimension 24 case required:
1. **45k lines** vs 29k for dim 8 (the magic function alone)
2. **Computer-assisted verification** of key inequalities (AppendixA: 72 files, 14k lines)
3. **Laurent series expansion** analysis (30+ files for DerivTwoLaurent)
4. **Three functions** instead of one simple combination

The difficulty comes from:
- More intricate modular form identities at higher weight
- Subtler sign conditions requiring numerical bounds
- The uniqueness result needs additional spectral analysis

## How Magic Functions Relate to Lattice Geometry

The magic functions encode lattice geometry through their construction from modular forms:

1. **Theta series connection**: The theta series of E8 is the Eisenstein series E_4. The magic function's modular form components are built from the SAME family of functions.

2. **Root system encoding**: g vanishes (changes sign) at exactly the minimum distance sqrt(2) - this is the distance between nearest neighbors in E8.

3. **Self-duality**: E8 is self-dual (E8 = E8*). The magic function reflects this: g and g-hat have the same structure.

4. **Fourier eigenfunction**: In the LP framework, the tightest bound comes from Fourier eigenfunctions. The modular S-transformation (z -> -1/z) IS the Fourier transform on theta functions - so modular forms are natural sources of eigenfunctions.

## Verification in the Formalization

The sign conditions are verified through:

1. **Integral representations**: Express g(x) as integrals with explicit signs
2. **Laplace transform**: Convert to Laplace domain where signs are clearer
3. **Contour deformation**: Move integration contours to regions where bounds are tractable
4. **Numerical certificates** (dim 24 only): Computer-verified bounds on specific expressions

Key files:
- `Dim8/MagicFunction/g/CohnElkies/SignConditions.lean`
- `Dim8/MagicFunction/g/CohnElkies/RealValued.lean`
- `Dim24/Inequalities/AppendixA/` (computer-assisted bounds)
