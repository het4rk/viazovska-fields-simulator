# Proof Architecture

## High-Level Flow

```
                    INPUTS
                      |
    +--E8 Lattice--+  +--Leech Lattice--+
    |   (Basic)    |  |    (Basic)       |
    +--------------+  +-----------------+
           |                  |
    +------v------+  +-------v--------+
    | Magic Func  |  | Magic Func     |
    | g (Dim8)    |  | F (Dim24)      |
    +------+------+  +-------+--------+
           |                  |
    +------v------------------v--------+
    |    Cohn-Elkies LP Bound          |
    |  (CohnElkies/LPBound.lean)       |
    +------+------------------+--------+
           |                  |
    +------v------+  +-------v--------+
    | Dim 8       |  | Dim 24         |
    | Optimality  |  | Optimality     |
    +-------------+  +-------+--------+
                              |
                     +--------v--------+
                     | Dim 24          |
                     | UNIQUENESS      |
                     | (BS81 + Golay)  |
                     +-----------------+
```

## Dimension 8 Proof (112 files, 29k lines)

### Step 1: Define E8
- File: `Dim8/E8/Basic.lean`
- Define E8 as Z-submodule of R^8
- Prove minimum norm = sqrt(2)
- Prove unimodularity (det = 1)

### Step 2: Compute E8 Packing Density
- File: `Dim8/E8/Packing.lean`
- Define E8Packing as periodic sphere packing
- Compute density = pi^4/384

### Step 3: Build Modular Forms
- Files: `ModularForms/` (48 files)
- Eisenstein series E_k, discriminant Delta
- Theta functions, eta function
- q-expansion machinery

### Step 4: Construct Magic Function g
- Files: `Dim8/MagicFunction/` (70+ files)
- Build auxiliary functions a and b from contour integrals
- Combine: g = (pi*I/8640)*a - (I/(240*pi))*b
- Prove g is a Schwartz function

### Step 5: Verify Cohn-Elkies Conditions
- Files: `Dim8/MagicFunction/g/CohnElkies/`
- g(0) = g-hat(0) = 1
- g is real-valued, g-hat is real-valued
- g(x) <= 0 for ||x|| >= sqrt(2)
- g-hat(xi) >= 0 for all xi

### Step 6: Apply LP Bound
- File: `Dim8/UpperBound.lean`
- SpherePackingConstant(8) <= pi^4/384

### Step 7: Conclude
- File: `Dim8/MainTheorem.lean`
- E8 density = pi^4/384 = upper bound
- Therefore E8 is optimal

## Dimension 24 Proof (572 files, 121k lines)

### Part A: Optimality

**Steps 1-2**: Define Leech lattice and compute density
- `Dim24/LeechLattice/Defs.lean` - explicit 24x24 generator matrix
- `Dim24/Packing.lean` - density = pi^12/12!

**Steps 3-5**: Build magic function F and verify conditions
- `Dim24/MagicFunction/A/` - Hecke eigenfunction construction
- `Dim24/MagicFunction/B/` - auxiliary function
- `Dim24/MagicFunction/F/` - combined magic function

**Step 6**: Apply LP bound
- SpherePackingConstant(24) <= pi^12/12!

### Part B: Numerical Verification (136 files, 26k lines)

The dimension 24 magic function requires computer-assisted inequality verification:

- `Dim24/Inequalities/AppendixA/` - rigorous bounds on q-expansion coefficients
- `Dim24/Inequalities/Ineq2/` - key inequality for the sign condition
- `Dim24/Inequalities/VarphiNeg/` - negativity of varphi function

This involves:
1. Truncating q-series at finite order
2. Bounding remainders with geometric series
3. Evaluating truncations with exact rational arithmetic
4. Certificate-based verification of polynomial positivity

### Part C: Uniqueness (241 files, 48k lines)

**Goal**: Any periodic packing achieving density pi^12/12! is isometric to a scaled Leech lattice.

**Step 1**: Equality case analysis (`Uniqueness/BS81/Thm14/`)
- If LP bound is tight, the packing must be a lattice
- Spherical design properties follow

**Step 2**: Shell structure (`Uniqueness/BS81/Thm15/`)
- Norm-4 shell has specific combinatorial structure
- Related to Golay code octads via distance distribution

**Step 3**: Coding theory (`Uniqueness/BS81/CodingTheory/`)
- Construct extended binary Golay code from shell
- Prove Golay code uniqueness (via Steiner system S(5,8,24))
- Witt design uniqueness

**Step 4**: Lattice reconstruction (`Uniqueness/Rigidity/`)
- From Golay code to even unimodular lattice
- Niemeier lattice classification: 24 types
- Only the rootless one (Leech) achieves the bound
- Kissing configuration uniqueness: 196,560 vectors determine the lattice

## Dependency Graph (Simplified)

```
ForMathlib (patches for Mathlib)
    |
Tactic (custom automation)
    |
Basic (sphere packing definitions)
    |
Integration + Contour (analysis tools)
    |
ModularForms (theta, Eisenstein, eta)
    |
CohnElkies (LP bound framework)
    |
MagicFunction (general parametrization)
    |
+----------+----------+
|                      |
Dim8                  Dim24
  |                   / | \
  MainThm     MagicF  Ineq  Uniqueness
                              |
                         BS81 + Golay
                              |
                         MainTheorem
```

## Bug Fixes Found During Formalization

Gauss caught two errors in the original papers:

1. **Dimension 8**: Sign error (minus sign) in Proposition 7 of Viazovska's paper
2. **Dimension 24**: Incomplete step in the computer-assisted Appendix A argument

Both were automatically fixed during autoformalization.
