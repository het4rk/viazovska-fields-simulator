"""
E8 Root System Visualization

Manim scenes for visualizing the 240 root vectors of the E8 lattice
via Petrie projection (2D) and 3D projections.
"""

from manim import *
import numpy as np
from itertools import combinations, product
from math import pi as PI


def e8_root_vectors():
    """Generate all 240 root vectors of E8."""
    roots = []

    # Type 1 (112): permutations of (+-1, +-1, 0^6)
    for pos in combinations(range(8), 2):
        for signs in product([-1, 1], repeat=2):
            v = np.zeros(8)
            v[pos[0]] = signs[0]
            v[pos[1]] = signs[1]
            roots.append(v)

    # Type 2 (128): (+-1/2)^8 with even number of minus signs
    for signs in product([-0.5, 0.5], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(np.array(signs))

    return np.array(roots)


def petrie_projection(roots):
    """Petrie projection of E8 roots onto Coxeter plane."""
    angles = np.array([k * PI / 15 for k in range(8)])
    proj_x = np.cos(angles)
    proj_y = np.sin(angles)
    x = roots @ proj_x
    y = roots @ proj_y
    # Normalize for display
    scale = max(np.max(np.abs(x)), np.max(np.abs(y)))
    return x / scale * 3, y / scale * 3


class E8RootSystem(Scene):
    """Visualize the 240 roots of E8 via Petrie projection."""

    def construct(self):
        # Title
        title = Text("E8 Root System", font_size=40).to_edge(UP)
        subtitle = Text("240 roots projected via Petrie projection", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.2)

        self.play(Write(title), Write(subtitle), run_time=1.5)
        self.wait(0.5)

        # Generate roots and project
        roots = e8_root_vectors()
        px, py = petrie_projection(roots)

        # Color by root type
        # Type 1 (first 112): integer coordinates
        # Type 2 (next 128): half-integer coordinates
        dots_type1 = VGroup()
        dots_type2 = VGroup()

        for i in range(len(roots)):
            x, y = px[i], py[i]
            if i < 112:
                dot = Dot(point=[x, y, 0], radius=0.04, color=BLUE)
                dots_type1.add(dot)
            else:
                dot = Dot(point=[x, y, 0], radius=0.04, color=GOLD)
                dots_type2.add(dot)

        all_dots = VGroup(dots_type1, dots_type2)
        all_dots.shift(DOWN * 0.3)

        # Animate: first type 1, then type 2
        self.play(
            FadeOut(subtitle),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_type1], lag_ratio=0.01),
            run_time=2,
        )

        label1 = Text("112 integer-coordinate roots", font_size=20, color=BLUE)
        label1.to_edge(DOWN)
        self.play(Write(label1), run_time=0.5)
        self.wait(0.5)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_type2], lag_ratio=0.01),
            run_time=2,
        )

        label2 = Text("+ 128 half-integer roots = 240 total", font_size=20, color=GOLD)
        label2.next_to(label1, UP, buff=0.15)
        self.play(Write(label2), run_time=0.5)
        self.wait(1)

        # Draw connecting lines for nearest neighbors (inner product = 1)
        self.play(FadeOut(label1), FadeOut(label2))

        # Draw a few connection lines to show structure
        edges = VGroup()
        positions = np.column_stack([px, py])
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                ip = np.dot(roots[i], roots[j])
                if abs(ip - 1.0) < 0.01:  # inner product = 1 (adjacent in root system)
                    line = Line(
                        [positions[i, 0], positions[i, 1] - 0.3, 0],
                        [positions[j, 0], positions[j, 1] - 0.3, 0],
                        stroke_width=0.3,
                        stroke_opacity=0.15,
                        color=WHITE,
                    )
                    edges.add(line)

        self.play(
            LaggedStart(*[Create(e) for e in edges[:500]], lag_ratio=0.002),
            run_time=3,
        )

        conn_label = Text("Adjacent roots connected (inner product = 1)", font_size=20)
        conn_label.to_edge(DOWN)
        self.play(Write(conn_label))
        self.wait(2)

        # Stats
        self.play(FadeOut(conn_label), FadeOut(edges))
        stats = VGroup(
            Text("E8 Lattice Properties:", font_size=24, color=WHITE),
            Text("Dimension: 8", font_size=20),
            Text("Roots (kissing number): 240", font_size=20),
            Text("Min norm: sqrt(2)", font_size=20),
            Text("Packing density: pi^4/384", font_size=20),
            Text("Coxeter number: 30", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        stats.to_edge(DOWN)

        self.play(
            LaggedStart(*[Write(s) for s in stats], lag_ratio=0.2),
            run_time=2,
        )
        self.wait(3)


class E8RootSystemRotating(Scene):
    """Animated rotation of E8 roots through different projection planes."""

    def construct(self):
        title = Text("E8 Root System - Rotating Projection", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        roots = e8_root_vectors()

        # Create dots
        dots = VGroup()
        for i in range(len(roots)):
            dot = Dot(radius=0.035)
            if i < 112:
                dot.set_color(BLUE)
            else:
                dot.set_color(GOLD)
            dots.add(dot)

        # Animate rotation through projection planes
        def update_projection(mob, alpha):
            theta = alpha * 2 * PI
            # Rotate projection plane
            angles = np.array([k * PI / 15 + theta * 0.1 * k for k in range(8)])
            proj_x = np.cos(angles)
            proj_y = np.sin(angles)

            # Normalize
            proj_x = proj_x / np.linalg.norm(proj_x)
            proj_y = proj_y / np.linalg.norm(proj_y)

            x = roots @ proj_x
            y = roots @ proj_y

            scale = max(np.max(np.abs(x)), np.max(np.abs(y))) + 0.01
            x = x / scale * 3
            y = y / scale * 3

            for i, dot in enumerate(mob):
                dot.move_to([x[i], y[i] - 0.3, 0])

        self.add(dots)
        # Initial position
        update_projection(dots, 0)
        self.play(FadeIn(dots))

        # Rotate
        self.play(
            UpdateFromAlphaFunc(dots, update_projection),
            run_time=12,
            rate_func=linear,
        )


class E8VsLeech(Scene):
    """Side-by-side comparison of E8 and Leech lattice properties."""

    def construct(self):
        title = Text("Exceptional Lattices: E8 vs Leech", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        # Two columns
        e8_header = Text("E8", font_size=32, color=BLUE).shift(LEFT * 3 + UP * 2)
        leech_header = Text("Leech", font_size=32, color=GOLD).shift(RIGHT * 3 + UP * 2)

        self.play(Write(e8_header), Write(leech_header))

        # Properties
        props = [
            ("Dimension", "8", "24"),
            ("Kissing #", "240", "196,560"),
            ("Min norm", "sqrt(2)", "2"),
            ("Density", "pi^4/384", "pi^12/12!"),
            ("Unimodular", "Yes", "Yes"),
            ("Root system", "E8", "None"),
            ("Optimal", "Proven 2017", "Proven 2017"),
        ]

        rows = VGroup()
        for i, (name, e8, leech) in enumerate(props):
            y = 1.3 - i * 0.5
            label = Text(name, font_size=18, color=GREY).move_to([0, y, 0])
            e8_val = Text(e8, font_size=18, color=BLUE_B).move_to([-3, y, 0])
            leech_val = Text(leech, font_size=18, color=GOLD_B).move_to([3, y, 0])
            row = VGroup(label, e8_val, leech_val)
            rows.add(row)

        self.play(
            LaggedStart(*[Write(r) for r in rows], lag_ratio=0.3),
            run_time=3,
        )
        self.wait(3)


class PackingDensityCurve(Scene):
    """Sphere packing density across dimensions."""

    def construct(self):
        title = Text("Sphere Packing Density by Dimension", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        # Create axes
        axes = Axes(
            x_range=[0, 26, 2],
            y_range=[-14, 1, 2],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_label = Text("Dimension", font_size=20).next_to(axes.x_axis, DOWN)
        y_label = Text("log(density)", font_size=20).next_to(axes.y_axis, LEFT)
        y_label.rotate(PI / 2)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)

        # Known densities (log scale)
        from math import log, factorial, sqrt
        known = {
            1: log(1.0),
            2: log(PI / (2 * sqrt(3))),
            3: log(PI / (3 * sqrt(2))),
            4: log(PI ** 2 / 16),
            8: log(PI ** 4 / 384),
            24: log(PI ** 12 / factorial(12)),
        }

        # Rough estimates for other dimensions
        all_dims = {}
        for d in range(1, 26):
            if d in known:
                all_dims[d] = known[d]
            else:
                all_dims[d] = -d * 0.5  # rough upper bound behavior

        # Plot general curve
        points = [(d, all_dims[d]) for d in sorted(all_dims.keys())]
        graph_points = [axes.c2p(d, v) for d, v in points]
        curve = VMobject()
        curve.set_points_smoothly(graph_points)
        curve.set_color(WHITE)
        curve.set_stroke(opacity=0.4)

        self.play(Create(curve), run_time=2)

        # Highlight special dimensions
        special = {
            1: ("dim 1", WHITE),
            2: ("dim 2\nhexagonal", GREEN),
            3: ("dim 3\nFCC", GREEN),
            8: ("dim 8\nE8", BLUE),
            24: ("dim 24\nLeech", GOLD),
        }

        special_dots = VGroup()
        for d, (label_text, color) in special.items():
            point = axes.c2p(d, known[d])
            dot = Dot(point, radius=0.08, color=color)
            label = Text(label_text, font_size=14, color=color)
            label.next_to(dot, UP + RIGHT, buff=0.1)
            special_dots.add(VGroup(dot, label))

        self.play(
            LaggedStart(*[FadeIn(s, scale=1.5) for s in special_dots], lag_ratio=0.3),
            run_time=2,
        )

        # Annotation
        note = Text(
            "Dimensions 8 and 24 are the only dimensions > 3\nwith proven optimal packings",
            font_size=18,
            color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(note), run_time=1.5)
        self.wait(3)
