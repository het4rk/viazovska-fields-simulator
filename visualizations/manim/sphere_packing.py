"""
Sphere Packing Visualization

Manim scenes showing sphere packing in low dimensions and
the concept of packing density.
"""

from manim import *
import numpy as np
from math import pi as PI, sqrt


class SpherePacking2D(Scene):
    """Visualize hexagonal sphere packing in 2D (circles)."""

    def construct(self):
        title = Text("Optimal Circle Packing in 2D", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        r = 0.4  # circle radius
        circles = VGroup()
        centers = []

        # Hexagonal lattice
        for row in range(-4, 5):
            for col in range(-6, 7):
                x = col * 2 * r + (row % 2) * r
                y = row * r * sqrt(3)
                if abs(x) < 5.5 and abs(y) < 3:
                    circle = Circle(radius=r, stroke_width=1.5)
                    circle.set_stroke(BLUE, opacity=0.7)
                    circle.set_fill(BLUE, opacity=0.15)
                    circle.move_to([x, y - 0.3, 0])
                    circles.add(circle)
                    centers.append([x, y - 0.3])

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.01),
            run_time=2,
        )

        # Show density
        density = PI / (2 * sqrt(3))
        density_text = Text(
            f"Density = pi / (2*sqrt(3)) = {density:.4f} = {density*100:.2f}%",
            font_size=22,
        ).to_edge(DOWN)
        self.play(Write(density_text), run_time=1)
        self.wait(2)

        # Highlight a fundamental domain
        c0 = np.array(centers[len(centers) // 2])
        # Hexagonal fundamental domain
        hex_vertices = []
        for k in range(6):
            angle = k * PI / 3 + PI / 6
            hex_vertices.append(c0 + r * sqrt(3) * np.array([np.cos(angle), np.sin(angle)]))
        hex_vertices.append(hex_vertices[0])

        hex_poly = Polygon(
            *[np.append(v, 0) for v in hex_vertices],
            stroke_width=3,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2,
        )

        fund_label = Text("Fundamental domain", font_size=18, color=YELLOW)
        fund_label.next_to(hex_poly, UP, buff=0.3)
        self.play(Create(hex_poly), Write(fund_label), run_time=1)
        self.wait(2)


class SpherePacking3D(ThreeDScene):
    """Visualize FCC sphere packing in 3D."""

    def construct(self):
        title = Text("FCC Sphere Packing in 3D", font_size=36)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        r = 0.35
        spheres = VGroup()

        # FCC lattice: face-centered cubic
        # Basis vectors: (1,1,0)/2, (1,0,1)/2, (0,1,1)/2
        for i in range(-2, 3):
            for j in range(-2, 3):
                for k in range(-2, 3):
                    # FCC positions
                    positions = [
                        np.array([i, j, k], dtype=float),
                        np.array([i + 0.5, j + 0.5, k], dtype=float),
                        np.array([i + 0.5, j, k + 0.5], dtype=float),
                        np.array([i, j + 0.5, k + 0.5], dtype=float),
                    ]
                    for pos in positions:
                        if np.linalg.norm(pos) < 2.5:
                            sphere = Sphere(radius=r * 0.5, resolution=(8, 8))
                            sphere.move_to(pos * 2 * r)
                            sphere.set_color(BLUE)
                            sphere.set_opacity(0.6)
                            spheres.add(sphere)

        self.play(
            LaggedStart(*[FadeIn(s) for s in spheres[:50]], lag_ratio=0.02),
            run_time=2,
        )

        # Rotate
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # Show density
        density = PI / (3 * sqrt(2))
        density_text = Text(
            f"Kepler: density = pi/(3*sqrt(2)) = {density:.4f}",
            font_size=22,
        )
        density_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(density_text)
        self.play(Write(density_text))
        self.wait(2)


class DimensionComparison(Scene):
    """Show how packing efficiency changes with dimension."""

    def construct(self):
        title = Text("The Dimension Puzzle", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        # Dimension labels and densities
        from math import factorial, log

        data = [
            (1, 1.0, "line"),
            (2, PI / (2 * sqrt(3)), "hexagonal"),
            (3, PI / (3 * sqrt(2)), "FCC"),
            (8, PI ** 4 / 384, "E8"),
            (24, PI ** 12 / factorial(12), "Leech"),
        ]

        bars = VGroup()
        labels = VGroup()
        x_start = -5

        for i, (dim, density, name) in enumerate(data):
            x = x_start + i * 2.5

            # Use log scale for bar height
            if density > 0:
                height = max(0.1, (log(density) + 14) / 3)
            else:
                height = 0.1

            bar = Rectangle(
                width=1.5,
                height=height,
                fill_opacity=0.7,
                stroke_width=1,
            )

            if dim in [8, 24]:
                bar.set_fill(GOLD)
                bar.set_stroke(GOLD)
            else:
                bar.set_fill(BLUE)
                bar.set_stroke(BLUE)

            bar.move_to([x, -2 + height / 2, 0])
            bars.add(bar)

            dim_label = Text(f"dim {dim}", font_size=18)
            dim_label.next_to(bar, DOWN, buff=0.1)

            name_label = Text(name, font_size=14, color=GREY)
            name_label.next_to(dim_label, DOWN, buff=0.05)

            density_label = Text(f"{density:.4e}" if density < 0.01 else f"{density:.4f}",
                                 font_size=14)
            density_label.next_to(bar, UP, buff=0.1)

            labels.add(VGroup(dim_label, name_label, density_label))

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2),
            run_time=2,
        )
        self.play(
            LaggedStart(*[Write(l) for l in labels], lag_ratio=0.2),
            run_time=2,
        )

        # Annotation
        note = Text(
            "Density drops exponentially with dimension.\nE8 and Leech are exceptionally efficient.",
            font_size=20,
            color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(note), run_time=1.5)
        self.wait(3)
