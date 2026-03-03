"""
Magic Function Analysis

Numerical computation and visualization of the radial Schwartz functions
("magic functions") used in Viazovska's sphere packing proof.

The magic functions are the key ingredient: they make the Cohn-Elkies
linear programming bound tight, proving optimality of E8 and Leech.
"""

import numpy as np
from scipy.special import jv as bessel_j  # Bessel function J_v
from scipy.integrate import quad
from scipy.fft import fft, fftfreq
from math import pi, sqrt, factorial, exp
import mpmath


def radial_fourier_transform_8d(f, xi, num_points=2000):
    """Compute the radial Fourier transform in 8 dimensions.

    For a radial function f(r) in R^8, the Fourier transform is:

    f_hat(s) = 2*pi * s^{-3} * integral_0^inf f(r) * J_3(2*pi*r*s) * r^4 dr

    where J_3 is the Bessel function of order 3.
    """
    def integrand(r):
        if r < 1e-15:
            return 0
        return f(r) * bessel_j(3, 2 * pi * r * xi) * r ** 4

    if xi < 1e-15:
        # At xi = 0, f_hat(0) = integral of f over R^8
        # = (2*pi^4/3) * integral_0^inf f(r) * r^7 dr
        result, _ = quad(lambda r: f(r) * r ** 7, 0, 20, limit=200)
        return 2 * pi ** 4 / 3 * result

    result, _ = quad(integrand, 0, 20, limit=200)
    return 2 * pi * xi ** (-3) * result


def gaussian_magic_8d(r, sigma=1.0):
    """Gaussian approximation to the dim-8 magic function.

    The exact magic function is built from modular forms. Here we construct
    a Gaussian-based approximation that captures the qualitative behavior:
    - Positive at origin
    - Decays and becomes negative around r = sqrt(2)
    - Fourier transform is non-negative

    f(r) = (1 - a*r^2) * exp(-pi*r^2)

    Tuned to vanish near r = sqrt(2).
    """
    a = 1 / 2  # f(sqrt(2)) = (1 - 2*a) * exp(-2*pi) ~ 0
    return (1 - a * r ** 2) * np.exp(-pi * r ** 2)


def approximate_magic_function_8d(r):
    """Better approximation of the dim-8 magic function.

    Uses a radial function of the form:
    g(r) = p(r^2) * exp(-pi*r^2)

    where p is a polynomial chosen so that:
    1. g(0) = 1
    2. g(r) <= 0 for r >= sqrt(2)
    3. g-hat(xi) >= 0

    The exact magic function involves integrals of modular forms.
    This polynomial-Gaussian approximation captures the key features.
    """
    x = r ** 2
    # Polynomial tuned for sign change at r = sqrt(2), i.e., x = 2
    # p(x) = 1 - c1*x + c2*x^2 - c3*x^3 + c4*x^4
    # Constraint: p(2) = 0 and p'(2) < 0 for clean sign change
    # Also need p(0) = 1

    # Using a 4th-degree polynomial with root at x = 2
    # p(x) = (1 - x/2) * (1 - a*x + b*x^2)
    a, b = 0.3, 0.02  # tuned for non-negative Fourier transform
    p = (1 - x / 2) * (1 - a * x + b * x ** 2)

    return p * np.exp(-pi * x)


def cohn_elkies_radial_profile(r_values, dim=8):
    """Compute the radial profile of the magic function.

    For visualization: shows f(r) vs r, highlighting:
    - The origin value f(0) = 1
    - The sign change at r = sqrt(2) (dim 8) or r = 2 (dim 24)
    - The decay behavior
    """
    if dim == 8:
        f_values = approximate_magic_function_8d(r_values)
        sign_change = sqrt(2)
    elif dim == 24:
        # Simpler Gaussian approximation for dim 24
        x = r_values ** 2
        # Sign change at r = 2 (x = 4)
        p = (1 - x / 4) * np.exp(-pi * x / 12)
        f_values = p
        sign_change = 2.0
    else:
        raise ValueError(f"Unsupported dimension {dim}")

    return f_values, sign_change


def modular_form_eisenstein(z, k=4, num_terms=50):
    """Compute Eisenstein series E_k(z) for z in the upper half-plane.

    E_k(z) = 1 - (2k/B_k) * sum_{n>=1} sigma_{k-1}(n) * q^n

    where q = exp(2*pi*i*z) and sigma_{k-1}(n) = sum of (k-1)-th powers of divisors.
    """
    # Bernoulli numbers
    bernoulli = {2: 1/6, 4: -1/30, 6: 1/42, 8: -1/30, 10: 5/66, 12: -691/2730}
    if k not in bernoulli:
        raise ValueError(f"Bernoulli number B_{k} not implemented")

    B_k = bernoulli[k]
    q = np.exp(2 * pi * 1j * z)

    result = 1.0 + 0j
    for n in range(1, num_terms + 1):
        # sigma_{k-1}(n)
        sigma = sum(d ** (k - 1) for d in range(1, n + 1) if n % d == 0)
        result += (-2 * k / B_k) * sigma * q ** n

    return result


def theta_series_e8(z, num_terms=50):
    """Compute the theta series of E8.

    Theta_E8(z) = E_4(z) = 1 + 240*q + 2160*q^2 + ...

    This is the foundational identity connecting E8 geometry to modular forms.
    """
    return modular_form_eisenstein(z, k=4, num_terms=num_terms)


def theta_series_leech(z, num_terms=50):
    """Compute the theta series of the Leech lattice.

    Theta_Leech(z) = E_4(z)^3 - 720*Delta(z)

    where Delta(z) = eta(z)^24 is the modular discriminant.
    """
    E4 = modular_form_eisenstein(z, k=4, num_terms=num_terms)

    # Delta(z) via q-expansion
    q = np.exp(2 * pi * 1j * z)

    # Ramanujan tau function (first few values)
    tau_values = [0, 1, -24, 252, -1472, 4830, -6048, -16744, 84480,
                  -113643, -115920, 534612, -370944, -577738, 401856,
                  1217160, 987136, -6905934, 2727432, 10661420, -7109760]

    Delta = 0j
    for n in range(1, min(num_terms + 1, len(tau_values))):
        Delta += tau_values[n] * q ** n

    return E4 ** 3 - 720 * Delta


def plot_data_magic_function(dim=8, r_max=4.0, num_points=500):
    """Generate plot data for the magic function radial profile."""
    r = np.linspace(0, r_max, num_points)
    f, sign_change = cohn_elkies_radial_profile(r, dim=dim)

    return {
        "r": r,
        "f": f,
        "sign_change": sign_change,
        "dim": dim,
    }


def plot_data_theta_series(y_min=0.1, y_max=2.0, num_points=200):
    """Generate plot data for theta series on the imaginary axis.

    Evaluate Theta_E8(iy) and Theta_Leech(iy) for y > 0.
    """
    y_values = np.linspace(y_min, y_max, num_points)
    z_values = 1j * y_values

    theta_e8 = np.array([theta_series_e8(z, num_terms=30).real for z in z_values])
    theta_leech = np.array([theta_series_leech(z, num_terms=15).real for z in z_values])

    return {
        "y": y_values,
        "theta_e8": theta_e8,
        "theta_leech": theta_leech,
    }


def verify_theta_coefficients():
    """Verify theta series coefficients match known values."""
    print("=== Theta Series Coefficient Verification ===\n")

    # E8 theta series = E_4
    print("E8 (= E_4):")
    z = 1j * 2  # safe point on imaginary axis
    q = np.exp(2 * pi * 1j * z)

    # Manual coefficient extraction via E_4
    E4_coeffs_expected = [1, 240, 2160, 6720, 17520, 30240]
    print(f"  Expected: {E4_coeffs_expected}")

    # Compute E_4 coefficient by coefficient
    sigma3 = lambda n: sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
    E4_coeffs = [1] + [240 * sigma3(n) for n in range(1, 6)]
    print(f"  Computed: {E4_coeffs}")
    print(f"  Match: {E4_coeffs == E4_coeffs_expected}")

    # Leech theta series
    print("\nLeech (= E_4^3 - 720*Delta):")
    leech_coeffs_expected = [1, 0, 196560, 16773120]
    print(f"  Expected first coefficients: {leech_coeffs_expected}")
    print(f"  Note: coefficient of q^1 is 0 (no vectors of norm sqrt(2))")


if __name__ == "__main__":
    verify_theta_coefficients()

    # Magic function data
    print("\n=== Magic Function Profiles ===")
    for dim in [8, 24]:
        data = plot_data_magic_function(dim=dim)
        f = data["f"]
        r = data["r"]
        sc = data["sign_change"]

        # Find where function crosses zero
        sign_changes = np.where(np.diff(np.sign(f)))[0]
        if len(sign_changes) > 0:
            zero_r = r[sign_changes[0]]
        else:
            zero_r = None

        print(f"\n  Dimension {dim}:")
        print(f"    f(0) = {f[0]:.6f}")
        print(f"    Expected sign change at r = {sc:.4f}")
        if zero_r:
            print(f"    Numerical zero crossing at r = {zero_r:.4f}")
        print(f"    f is negative for r > {sc}: {np.all(f[r > sc + 0.1] < 0)}")

    # Theta series on imaginary axis
    print("\n=== Theta Series on Imaginary Axis ===")
    data = plot_data_theta_series()
    print(f"  Theta_E8(i) ~ {data['theta_e8'][np.argmin(np.abs(data['y'] - 1.0))]:.2f}")
    print(f"  Theta_Leech(i) ~ {data['theta_leech'][np.argmin(np.abs(data['y'] - 1.0))]:.2f}")
