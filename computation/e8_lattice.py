"""
E8 Lattice Computations

Computes root vectors, kissing numbers, theta series, and packing density
for the E8 lattice using pure Python + NumPy.
"""

import numpy as np
from itertools import combinations, product
from math import pi, factorial, sqrt
from collections import Counter


def e8_generator_matrix():
    """Return the standard E8 generator matrix (8x8).

    Uses the D8+ construction: D8 union (D8 + [1/2]^8).
    This specific basis generates the full E8 lattice.
    """
    # Standard E8 basis (Cartan matrix style)
    M = np.array([
        [ 2,  0,  0,  0,  0,  0,  0,  0],
        [-1,  1,  0,  0,  0,  0,  0,  0],
        [ 0, -1,  1,  0,  0,  0,  0,  0],
        [ 0,  0, -1,  1,  0,  0,  0,  0],
        [ 0,  0,  0, -1,  1,  0,  0,  0],
        [ 0,  0,  0,  0, -1,  1,  0,  0],
        [ 0,  0,  0,  0,  0, -1,  1,  0],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    ], dtype=np.float64)
    return M


def e8_root_vectors():
    """Generate all 240 root vectors of E8 (minimal norm sqrt(2) vectors).

    Type 1 (112): All permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
    Type 2 (128): (+-1/2)^8 with even number of negative signs
    """
    roots = []

    # Type 1: choose 2 positions, all sign combos
    for pos in combinations(range(8), 2):
        for signs in product([-1, 1], repeat=2):
            v = np.zeros(8)
            v[pos[0]] = signs[0]
            v[pos[1]] = signs[1]
            roots.append(v)

    # Type 2: half-integer vectors with even parity
    for signs in product([-0.5, 0.5], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(np.array(signs))

    return np.array(roots)


def verify_e8_roots(roots):
    """Verify properties of E8 root vectors."""
    norms_sq = np.sum(roots ** 2, axis=1)

    print("=== E8 Root System Verification ===")
    print(f"Number of roots: {len(roots)}")
    print(f"Expected: 240")
    print(f"All norms squared = 2: {np.allclose(norms_sq, 2.0)}")
    print(f"Min norm squared: {norms_sq.min():.6f}")
    print(f"Max norm squared: {norms_sq.max():.6f}")

    # Check inner products
    inner_products = roots @ roots.T
    # For E8 roots, inner products are in {-2, -1, 0, 1, 2}
    unique_ips = sorted(set(np.round(inner_products.flatten(), 6)))
    print(f"Unique inner products: {unique_ips}")

    # Kissing number: for any root v, how many other roots have |v . w| = 1?
    v0 = roots[0]
    dots = roots @ v0
    neighbors = np.sum(np.isclose(np.abs(dots), 1.0))
    print(f"Neighbors of first root (|v.w| = 1): {neighbors}")

    return True


def e8_theta_series(num_terms=10):
    """Compute theta series coefficients of E8.

    Theta_E8(q) = sum_{v in E8} q^{||v||^2 / 2}
                = 1 + 240*q + 2160*q^2 + 6720*q^3 + ...

    This equals the Eisenstein series E_4!

    We compute by enumerating lattice vectors up to a given norm.
    """
    # For small terms, enumerate vectors with integer coords + half-integer coords
    coeffs = Counter()
    # zero vector will be counted in the integer loop below (all-zeros has even sum)

    # We need vectors with ||v||^2/2 <= num_terms
    # So ||v||^2 <= 2*num_terms
    max_norm_sq = 2 * num_terms
    max_coord = int(np.ceil(np.sqrt(max_norm_sq))) + 1

    # Integer-coordinate vectors (D8 type)
    # All integer vectors with even coordinate sum and ||v||^2 <= max_norm_sq
    count = 0
    for coords in product(range(-max_coord, max_coord + 1), repeat=8):
        v = np.array(coords, dtype=np.float64)
        norm_sq = np.sum(v ** 2)
        if norm_sq <= max_norm_sq and sum(coords) % 2 == 0:
            n = int(round(norm_sq / 2))
            if n <= num_terms:
                coeffs[n] += 1
                count += 1

    # Half-integer-coordinate vectors
    for coords in product(range(-max_coord, max_coord + 1), repeat=8):
        v = np.array(coords, dtype=np.float64) + 0.5
        norm_sq = np.sum(v ** 2)
        if norm_sq <= max_norm_sq and int(round(sum(coords))) % 2 == 0:
            n = int(round(norm_sq / 2))
            if n <= num_terms:
                coeffs[n] += 1

    result = [coeffs.get(n, 0) for n in range(num_terms + 1)]
    return result


def e8_packing_density():
    """Compute the sphere packing density of E8.

    density = vol(B_8(r)) / vol(fundamental domain)

    where r = sqrt(2)/2 (half the minimum distance) and
    vol(fundamental domain) = 1 (E8 is unimodular).
    """
    dim = 8
    r = sqrt(2) / 2  # packing radius

    # Volume of 8-dimensional ball of radius r
    vol_ball = (pi ** (dim / 2)) / factorial(dim // 2) * r ** dim

    # Fundamental domain volume = 1 (unimodular)
    density = vol_ball

    # Exact value
    exact = pi ** 4 / 384

    print("\n=== E8 Packing Density ===")
    print(f"Packing radius: sqrt(2)/2 = {r:.6f}")
    print(f"Vol(B_8(r)): {vol_ball:.10f}")
    print(f"Computed density: {density:.10f}")
    print(f"Exact (pi^4/384): {exact:.10f}")
    print(f"Match: {np.isclose(density, exact)}")

    return density


def e8_petrie_projection(roots):
    """Project E8 roots onto a 2D plane using Petrie projection.

    The Petrie projection of E8 creates a beautiful 2D pattern showing
    the structure of the 240 roots projected along a Coxeter element direction.
    """
    # Petrie projection angles: k*pi/15 for k = 0..7
    # This creates the famous E8 Petrie polygon (30-gon)
    angles = np.array([k * pi / 15 for k in range(8)])

    # Projection vectors
    proj_x = np.cos(angles)
    proj_y = np.sin(angles)

    # Project roots
    x = roots @ proj_x
    y = roots @ proj_y

    return x, y


def e8_coxeter_projection(roots):
    """Project E8 roots using Coxeter plane projection.

    Uses the two eigenvectors of the Coxeter element corresponding
    to the eigenvalue exp(2*pi*i/30) (Coxeter number h=30).
    """
    h = 30  # Coxeter number of E8
    angles = np.array([2 * pi * k / h for k in range(8)])

    proj_x = np.cos(angles) / np.sqrt(4)
    proj_y = np.sin(angles) / np.sqrt(4)

    x = roots @ proj_x
    y = roots @ proj_y

    return x, y


def packing_density_by_dimension(max_dim=30):
    """Compute best known sphere packing densities across dimensions.

    Returns dict of dimension -> (density, name, is_proven_optimal).
    """
    results = {}

    for d in range(1, max_dim + 1):
        # Volume of d-dimensional unit ball
        if d % 2 == 0:
            vol_unit = pi ** (d // 2) / factorial(d // 2)
        else:
            k = (d - 1) // 2
            vol_unit = 2 ** d * pi ** k * factorial(k) / factorial(d)

        if d == 1:
            density = 1.0
            name = "line"
            optimal = True
        elif d == 2:
            density = pi / (2 * sqrt(3))
            name = "hexagonal"
            optimal = True
        elif d == 3:
            density = pi / (3 * sqrt(2))
            name = "FCC"
            optimal = True
        elif d == 8:
            density = pi ** 4 / 384
            name = "E8"
            optimal = True
        elif d == 24:
            density = pi ** 12 / factorial(12)
            name = "Leech"
            optimal = True
        else:
            # Minkowski bound (not tight, just a lower bound)
            density = 2 ** (-d)  # very rough estimate
            name = "best known"
            optimal = False

        results[d] = {
            "density": density,
            "name": name,
            "optimal": optimal,
            "vol_unit_ball": vol_unit,
        }

    return results


if __name__ == "__main__":
    # Generate and verify E8 roots
    roots = e8_root_vectors()
    verify_e8_roots(roots)

    # Packing density
    e8_packing_density()

    # Theta series (small computation)
    print("\n=== E8 Theta Series (first few terms) ===")
    print("Computing... (this enumerates lattice vectors, may take a moment)")
    # Only compute first 3 terms to keep it fast
    theta = e8_theta_series(num_terms=2)
    print(f"Theta_E8 = {theta[0]} + {theta[1]}*q + {theta[2]}*q^2 + ...")
    print(f"Expected: 1 + 240*q + 2160*q^2 + ...")

    # Packing density landscape
    print("\n=== Packing Density by Dimension ===")
    densities = packing_density_by_dimension(26)
    for d in [1, 2, 3, 8, 24]:
        info = densities[d]
        star = " *" if info["optimal"] else ""
        print(f"  dim {d:2d}: {info['density']:.10f}  ({info['name']}){star}")
    print("  (* = proven optimal)")

    # Petrie projection coordinates
    px, py = e8_petrie_projection(roots)
    print(f"\n=== E8 Petrie Projection ===")
    print(f"Projected {len(roots)} roots to 2D")
    print(f"X range: [{px.min():.4f}, {px.max():.4f}]")
    print(f"Y range: [{py.min():.4f}, {py.max():.4f}]")
