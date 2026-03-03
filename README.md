# viazovska-fields-simulator

Computational exploration and visualization of Maryna Viazovska's Fields Medal-winning sphere packing proof.

This project studies the formal verification (in Lean 4) of the proof that the **E8 lattice** and **Leech lattice** achieve optimal sphere packing density in dimensions 8 and 24 respectively, and builds interactive simulations to make these structures tangible.

## What's here

- **formalization/** - Git submodule of [math-inc/Sphere-Packing-Lean](https://github.com/math-inc/Sphere-Packing-Lean), the ~180k line Lean 4 formalization
- **notes/** - Structured study notes breaking down the proof architecture
- **computation/** - SageMath and Python scripts for lattice computations
- **visualizations/** - Manim animations and Plotly Dash interactive explorer

## Key concepts

| Structure | Dimension | Kissing number | Packing density |
|-----------|-----------|---------------|-----------------|
| E8 lattice | 8 | 240 | pi^4/384 ~ 0.2537 |
| Leech lattice | 24 | 196,560 | pi^12/12! ~ 0.001930 |

## Setup

```bash
git clone --recursive https://github.com/het4rk/viazovska-fields-simulator.git
cd viazovska-fields-simulator
pip install -e .
```

## Run visualizations

```bash
# Manim animations
manim -pql visualizations/manim/e8_roots.py E8RootSystem

# Interactive dashboard
python visualizations/interactive/app.py
```

## References

- [Viazovska (2017) - The sphere packing problem in dimension 8](https://arxiv.org/abs/1603.04246)
- [Cohn, Kumar, Miller, Radchenko, Viazovska (2017) - The sphere packing problem in dimension 24](https://arxiv.org/abs/1603.06518)
- [Math, Inc. - Formal verification of sphere packing](https://www.math.inc/sphere-packing)
- [Sphere Packing Lean Blueprint](https://thefundamentaltheor3m.github.io/Sphere-Packing-Lean/)
