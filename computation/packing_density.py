"""
Sphere Packing Density Analysis

Computes and compares packing densities across dimensions,
with special focus on the exceptional dimensions 8 and 24.
"""

import numpy as np
from math import pi, factorial, sqrt, gamma, log
from scipy.special import gammaln


def volume_unit_ball(d):
    """Volume of the unit ball in R^d."""
    return pi ** (d / 2) / gamma(d / 2 + 1)


def sphere_packing_density_upper_bound(d):
    """Kabatyansky-Levenshtein upper bound (1978) on packing density.

    This asymptotic bound is: delta_d <= 2^{-0.5990d(1+o(1))}
    For finite d, we use the refined version.
    """
    if d < 2:
        return 1.0
    # Approximate KL bound
    return 2 ** (-0.599 * d)


def cohn_elkies_bound(d, f_zero, f_hat_zero, radius):
    """Cohn-Elkies linear programming bound.

    Given a magic function f with:
    - f(0) = f_zero
    - f_hat(0) = f_hat_zero
    - f(x) <= 0 for ||x|| >= radius

    The bound is: density <= (f_zero / f_hat_zero) * vol(B(radius/2))
    """
    vol = volume_unit_ball(d) * (radius / 2) ** d
    return (f_zero / f_hat_zero) * vol


def known_lattice_densities():
    """Known lattice packing densities for special dimensions."""
    return {
        1: {"density": 1.0, "lattice": "Z", "kissing": 2},
        2: {"density": pi / (2 * sqrt(3)), "lattice": "A2 (hexagonal)", "kissing": 6},
        3: {"density": pi / (3 * sqrt(2)), "lattice": "D3 (FCC)", "kissing": 12},
        4: {"density": pi ** 2 / 16, "lattice": "D4", "kissing": 24},
        5: {"density": pi ** 2 * sqrt(2) / 30, "lattice": "D5", "kissing": 40},
        6: {"density": pi ** 3 * sqrt(3) / 144, "lattice": "E6", "kissing": 72},
        7: {"density": pi ** 3 / 105, "lattice": "E7", "kissing": 126},
        8: {"density": pi ** 4 / 384, "lattice": "E8", "kissing": 240},
        24: {"density": pi ** 12 / factorial(12), "lattice": "Leech", "kissing": 196560},
    }


def packing_density_curve(max_dim=50):
    """Generate packing density data for dimensions 1 through max_dim.

    Returns best known lattice densities (exact where known, estimates elsewhere).
    """
    # Best known lattice packing densities (from Conway-Sloane tables)
    known = known_lattice_densities()

    # For other dimensions, use densest known lattice packings
    # These are from Sloane's tables of densest known lattice packings
    center_densities = {
        # delta = density / vol_ball, related to Hermite constant
        1: 1, 2: 1/sqrt(3), 3: 1/sqrt(2),
        4: 1, 5: sqrt(2), 6: sqrt(3),
        7: 2, 8: 1,  # E8 center density = 1
        9: sqrt(2), 10: 2, 11: 2*sqrt(2),
        12: 4, 13: 4*sqrt(2), 14: 8,
        15: 8*sqrt(2), 16: 16,
        24: 1,  # Leech center density = 1
    }

    results = []
    for d in range(1, max_dim + 1):
        if d in known:
            density = known[d]["density"]
            name = known[d]["lattice"]
            proven = d in [1, 2, 3, 8, 24]
        else:
            # Use Minkowski-Hlawka lower bound as rough estimate
            # There exists a lattice with density >= zeta(d) / 2^{d-1}
            density = 2 ** (1 - d)  # very rough
            name = "estimate"
            proven = False

        results.append({
            "dim": d,
            "density": density,
            "log_density": log(density) if density > 0 else float("-inf"),
            "lattice": name,
            "proven_optimal": proven,
        })

    return results


def kissing_number_analysis():
    """Known and conjectured kissing numbers by dimension.

    The kissing number tau(d) is the maximum number of non-overlapping
    unit spheres that can touch a central unit sphere in R^d.
    """
    # Exact values
    exact = {
        1: 2,
        2: 6,
        3: 12,    # Newton (1694), proved Schutte & van der Waerden (1953)
        4: 24,    # Musin (2008)
        8: 240,   # Levenshtein (1979) / Odlyzko-Sloane (1979)
        24: 196560,  # Levenshtein (1979) / Odlyzko-Sloane (1979)
    }

    # Best known lower bounds for other dimensions
    lower_bounds = {
        5: 40, 6: 72, 7: 126,
        9: 306, 10: 500, 11: 582, 12: 840,
        13: 1154, 14: 1606, 15: 2564, 16: 4320,
    }

    print("=== Kissing Numbers ===")
    print(f"{'Dim':>4} {'Kissing #':>10} {'Status':>12}")
    print("-" * 30)
    for d in range(1, 25):
        if d in exact:
            print(f"{d:4d} {exact[d]:10d} {'exact':>12}")
        elif d in lower_bounds:
            print(f"{d:4d} {lower_bounds[d]:10d} {'lower bound':>12}")

    return exact, lower_bounds


def compare_e8_leech():
    """Side-by-side comparison of E8 and Leech lattice properties."""
    print("\n=== E8 vs Leech Lattice Comparison ===")
    print(f"{'Property':<30} {'E8':>20} {'Leech':>20}")
    print("-" * 72)

    props = [
        ("Dimension", "8", "24"),
        ("Determinant", "1", "1"),
        ("Even unimodular", "Yes", "Yes"),
        ("Min norm", "sqrt(2)", "2"),
        ("Kissing number", "240", "196,560"),
        ("Density", f"{pi**4/384:.10f}", f"{pi**12/factorial(12):.10e}"),
        ("Exact density", "pi^4/384", "pi^12/12!"),
        ("Automorphism group", "W(E8)", "Co_0"),
        ("|Aut|", "696,729,600", "~8.3 * 10^18"),
        ("Theta = Eisenstein?", "Yes (E_4)", "No (E_4^3 - 720*Delta)"),
        ("Coxeter number", "30", "N/A"),
        ("Root system", "E8", "None (rootless)"),
        ("Covering radius", "~1.414", "sqrt(2)"),
        ("Deep holes", "Minimal", "23 types"),
        ("Optimality proven", "2017 (Viazovska)", "2017 (CKMRV)"),
        ("Uniqueness proven", "Classical", "2017 (CKMRV) + 2025 formal"),
    ]

    for name, e8_val, leech_val in props:
        print(f"{name:<30} {e8_val:>20} {leech_val:>20}")


if __name__ == "__main__":
    print("=== Sphere Packing Density Analysis ===\n")

    # Known densities
    known = known_lattice_densities()
    print("Proven Optimal Packings:")
    for d in sorted(known.keys()):
        info = known[d]
        proven = d in [1, 2, 3, 8, 24]
        star = " [PROVEN OPTIMAL]" if proven else ""
        print(f"  dim {d:2d}: {info['density']:.10f}  {info['lattice']:<20} "
              f"kissing={info['kissing']}{star}")

    # Kissing numbers
    kissing_number_analysis()

    # E8 vs Leech
    compare_e8_leech()

    # Cohn-Elkies verification for E8
    print("\n=== Cohn-Elkies Bound Verification (E8) ===")
    # scaledMagic: f(0) = 1, f_hat(0) = 1/16, radius = 1 (after scaling)
    # But we use the original: g(0) = g_hat(0) = 1, radius = sqrt(2)
    bound_e8 = cohn_elkies_bound(8, f_zero=1, f_hat_zero=1, radius=sqrt(2))
    exact_e8 = pi ** 4 / 384
    print(f"LP bound: {bound_e8:.10f}")
    print(f"E8 density: {exact_e8:.10f}")
    print(f"Bound is tight: {np.isclose(bound_e8, exact_e8)}")

    # Cohn-Elkies verification for Leech
    print("\n=== Cohn-Elkies Bound Verification (Leech) ===")
    bound_leech = cohn_elkies_bound(24, f_zero=1, f_hat_zero=1, radius=2)
    exact_leech = pi ** 12 / factorial(12)
    print(f"LP bound: {bound_leech:.10e}")
    print(f"Leech density: {exact_leech:.10e}")
    print(f"Bound is tight: {np.isclose(bound_leech, exact_leech)}")
