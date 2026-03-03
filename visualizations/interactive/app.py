"""
Interactive Sphere Packing Explorer

A Plotly Dash app for interactively exploring E8 and Leech lattice
properties, packing densities, and magic function profiles.

Run with: python visualizations/interactive/app.py
"""

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from math import pi, sqrt, factorial, log, gamma
from itertools import combinations, product

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="Viazovska Fields Simulator",
)

# ============================================================
# DATA GENERATION
# ============================================================


def e8_root_vectors():
    """Generate all 240 root vectors of E8."""
    roots = []
    for pos in combinations(range(8), 2):
        for signs in product([-1, 1], repeat=2):
            v = np.zeros(8)
            v[pos[0]] = signs[0]
            v[pos[1]] = signs[1]
            roots.append(v)
    for signs in product([-0.5, 0.5], repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(np.array(signs))
    return np.array(roots)


def project_e8(roots, angle_offset=0):
    """Project E8 roots to 2D via Petrie projection with optional rotation."""
    angles = np.array([k * pi / 15 + angle_offset * k for k in range(8)])
    proj_x = np.cos(angles)
    proj_y = np.sin(angles)
    x = roots @ proj_x
    y = roots @ proj_y
    scale = max(np.max(np.abs(x)), np.max(np.abs(y))) + 0.01
    return x / scale, y / scale


def volume_unit_ball(d):
    """Volume of the unit ball in R^d."""
    return pi ** (d / 2) / gamma(d / 2 + 1)


def packing_density_data():
    """Generate packing density data across dimensions."""
    known_exact = {
        1: (1.0, "Z (integers)"),
        2: (pi / (2 * sqrt(3)), "A2 (hexagonal)"),
        3: (pi / (3 * sqrt(2)), "D3 (FCC)"),
        4: (pi ** 2 / 16, "D4"),
        8: (pi ** 4 / 384, "E8"),
        24: (pi ** 12 / factorial(12), "Leech"),
    }
    proven_optimal = {1, 2, 3, 8, 24}

    dims = list(range(1, 37))
    densities = []
    names = []
    is_proven = []
    log_densities = []

    for d in dims:
        if d in known_exact:
            dens, name = known_exact[d]
        else:
            dens = 2 ** (1 - d)  # rough Minkowski-type estimate
            name = f"best known (dim {d})"

        densities.append(dens)
        names.append(name)
        is_proven.append(d in proven_optimal)
        log_densities.append(log(dens) if dens > 0 else -50)

    return dims, densities, log_densities, names, is_proven


def approx_magic_function(r, dim=8):
    """Approximate magic function radial profile."""
    x = r ** 2
    if dim == 8:
        p = (1 - x / 2) * (1 - 0.3 * x + 0.02 * x ** 2)
        return p * np.exp(-pi * x)
    elif dim == 24:
        p = (1 - x / 4) * (1 - 0.15 * x + 0.005 * x ** 2)
        return p * np.exp(-pi * x / 12)
    return 0


def theta_series_E4(num_terms=20):
    """Compute E_4 (= theta series of E8) q-expansion coefficients."""
    # sigma_3(n) = sum of cubes of divisors
    def sigma3(n):
        return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
    return [1] + [240 * sigma3(n) for n in range(1, num_terms + 1)]


# ============================================================
# PRECOMPUTE
# ============================================================

ROOTS = e8_root_vectors()
DIMS, DENSITIES, LOG_DENSITIES, NAMES, IS_PROVEN = packing_density_data()
E4_COEFFS = theta_series_E4(20)

# ============================================================
# LAYOUT
# ============================================================

CARD_STYLE = {
    "background": "rgba(30, 30, 50, 0.7)",
    "backdropFilter": "blur(20px)",
    "WebkitBackdropFilter": "blur(20px)",
    "border": "1px solid rgba(255, 255, 255, 0.1)",
    "borderRadius": "12px",
    "padding": "20px",
    "marginBottom": "20px",
}

app.layout = dbc.Container([
    # Header
    html.Div([
        html.H1("Viazovska Fields Simulator",
                 style={"textAlign": "center", "color": "#ffd700", "marginBottom": "5px"}),
        html.P("Interactive exploration of E8, Leech lattice, and sphere packing optimality",
               style={"textAlign": "center", "color": "#aaa", "fontSize": "16px"}),
    ], style={"marginTop": "20px", "marginBottom": "30px"}),

    dbc.Tabs([
        # Tab 1: E8 Root System
        dbc.Tab(label="E8 Root System", children=[
            html.Div([
                html.Div([
                    html.H4("E8 Petrie Projection", style={"color": "#4fc3f7"}),
                    html.P("240 root vectors projected from 8D to 2D", style={"color": "#888"}),
                    dbc.Label("Projection angle offset:"),
                    dcc.Slider(
                        id="e8-angle-slider",
                        min=0, max=2 * pi, step=0.05, value=0,
                        marks={0: "0", 3.14: "pi", 6.28: "2pi"},
                    ),
                    dcc.Graph(id="e8-projection-plot", style={"height": "550px"}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H4("E8 Properties", style={"color": "#4fc3f7"}),
                    dbc.Table([
                        html.Tbody([
                            html.Tr([html.Td("Dimension"), html.Td("8")]),
                            html.Tr([html.Td("Roots (kissing #)"), html.Td("240")]),
                            html.Tr([html.Td("Min norm"), html.Td("sqrt(2) ~ 1.4142")]),
                            html.Tr([html.Td("Packing density"), html.Td("pi^4/384 ~ 0.2537")]),
                            html.Tr([html.Td("Automorphism group"), html.Td("W(E8), |G| = 696,729,600")]),
                            html.Tr([html.Td("Coxeter number"), html.Td("30")]),
                            html.Tr([html.Td("Self-dual"), html.Td("Yes")]),
                        ])
                    ], bordered=True, color="dark", striped=True, size="sm"),
                ], style=CARD_STYLE),
            ]),
        ]),

        # Tab 2: Packing Density
        dbc.Tab(label="Packing Density", children=[
            html.Div([
                html.Div([
                    html.H4("Sphere Packing Density by Dimension", style={"color": "#ffd700"}),
                    dbc.RadioItems(
                        id="density-scale",
                        options=[
                            {"label": "Linear scale", "value": "linear"},
                            {"label": "Log scale", "value": "log"},
                        ],
                        value="log",
                        inline=True,
                    ),
                    dcc.Graph(id="density-plot", style={"height": "500px"}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H4("Lattice Comparison", style={"color": "#ffd700"}),
                    dbc.Table([
                        html.Thead(html.Tr([
                            html.Th("Dim"), html.Th("Lattice"), html.Th("Density"),
                            html.Th("Kissing #"), html.Th("Proven"),
                        ])),
                        html.Tbody([
                            html.Tr([html.Td("1"), html.Td("Z"), html.Td("1.0000"),
                                     html.Td("2"), html.Td("Yes")]),
                            html.Tr([html.Td("2"), html.Td("A2"), html.Td("0.9069"),
                                     html.Td("6"), html.Td("Yes")]),
                            html.Tr([html.Td("3"), html.Td("FCC"), html.Td("0.7405"),
                                     html.Td("12"), html.Td("Yes")]),
                            html.Tr([html.Td("8"), html.Td("E8"), html.Td("0.2537"),
                                     html.Td("240"), html.Td("Yes")],
                                    style={"color": "#4fc3f7", "fontWeight": "bold"}),
                            html.Tr([html.Td("24"), html.Td("Leech"), html.Td("1.930e-3"),
                                     html.Td("196,560"), html.Td("Yes")],
                                    style={"color": "#ffd700", "fontWeight": "bold"}),
                        ]),
                    ], bordered=True, color="dark", striped=True, size="sm"),
                ], style=CARD_STYLE),
            ]),
        ]),

        # Tab 3: Magic Functions
        dbc.Tab(label="Magic Functions", children=[
            html.Div([
                html.Div([
                    html.H4("Magic Function Radial Profile", style={"color": "#66bb6a"}),
                    html.P("The Schwartz function that makes the LP bound tight",
                           style={"color": "#888"}),
                    dbc.Checklist(
                        id="magic-dims",
                        options=[
                            {"label": " Dimension 8 (E8)", "value": 8},
                            {"label": " Dimension 24 (Leech)", "value": 24},
                        ],
                        value=[8],
                        inline=True,
                    ),
                    dcc.Graph(id="magic-function-plot", style={"height": "450px"}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H4("Cohn-Elkies Conditions", style={"color": "#66bb6a"}),
                    html.Ul([
                        html.Li("g(0) = 1 (positive at origin)"),
                        html.Li("g-hat(0) = 1 (Fourier transform positive at origin)"),
                        html.Li("g(r) <= 0 for r >= sqrt(2) [dim 8] or r >= 2 [dim 24]"),
                        html.Li("g-hat(xi) >= 0 for all xi"),
                    ], style={"color": "#ccc"}),
                    html.P(
                        "When these conditions are met, the LP bound gives an upper bound "
                        "on packing density. If this bound matches a known lattice density, "
                        "that lattice is proven optimal.",
                        style={"color": "#888"},
                    ),
                ], style=CARD_STYLE),
            ]),
        ]),

        # Tab 4: Theta Series
        dbc.Tab(label="Theta Series", children=[
            html.Div([
                html.Div([
                    html.H4("E8 Theta Series = Eisenstein E_4", style={"color": "#ce93d8"}),
                    html.P("Theta_E8(q) = 1 + 240q + 2160q^2 + 6720q^3 + ...",
                           style={"color": "#aaa", "fontFamily": "monospace"}),
                    dcc.Slider(
                        id="theta-terms",
                        min=5, max=20, step=1, value=10,
                        marks={5: "5", 10: "10", 15: "15", 20: "20"},
                    ),
                    dcc.Graph(id="theta-coefficients-plot", style={"height": "400px"}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H4("Coefficient Interpretation", style={"color": "#ce93d8"}),
                    html.P(
                        "Each coefficient counts the number of lattice vectors at that "
                        "squared norm. The n-th coefficient of the theta series gives the "
                        "number of vectors v in the lattice with ||v||^2 = 2n.",
                        style={"color": "#ccc"},
                    ),
                    dbc.Table([
                        html.Thead(html.Tr([
                            html.Th("n"), html.Th("||v||^2 = 2n"), html.Th("# vectors"),
                            html.Th("Meaning"),
                        ])),
                        html.Tbody([
                            html.Tr([html.Td("0"), html.Td("0"), html.Td("1"),
                                     html.Td("Origin")]),
                            html.Tr([html.Td("1"), html.Td("2"), html.Td("240"),
                                     html.Td("Root vectors (kissing number)")]),
                            html.Tr([html.Td("2"), html.Td("4"), html.Td("2,160"),
                                     html.Td("Second shell")]),
                            html.Tr([html.Td("3"), html.Td("6"), html.Td("6,720"),
                                     html.Td("Third shell")]),
                            html.Tr([html.Td("4"), html.Td("8"), html.Td("17,520"),
                                     html.Td("Fourth shell")]),
                        ]),
                    ], bordered=True, color="dark", striped=True, size="sm"),
                ], style=CARD_STYLE),
            ]),
        ]),
    ]),

    # Footer
    html.Div([
        html.Hr(style={"borderColor": "#333"}),
        html.P([
            "Based on Viazovska's Fields Medal proof (2022) and the ",
            html.A("Math, Inc. Lean formalization",
                   href="https://github.com/math-inc/Sphere-Packing-Lean",
                   target="_blank", style={"color": "#4fc3f7"}),
            " (~180k lines of Lean 4)",
        ], style={"textAlign": "center", "color": "#666", "fontSize": "14px"}),
    ]),
], fluid=True, style={"maxWidth": "1200px"})


# ============================================================
# CALLBACKS
# ============================================================


@callback(
    Output("e8-projection-plot", "figure"),
    Input("e8-angle-slider", "value"),
)
def update_e8_projection(angle):
    x, y = project_e8(ROOTS, angle_offset=angle)

    # Color by root type
    colors = ["#4fc3f7"] * 112 + ["#ffd700"] * 128
    types = ["Integer coords"] * 112 + ["Half-integer coords"] * 128

    fig = go.Figure()

    # Edges (nearest neighbors, inner product = 1)
    for i in range(len(ROOTS)):
        for j in range(i + 1, len(ROOTS)):
            if abs(np.dot(ROOTS[i], ROOTS[j]) - 1.0) < 0.01:
                fig.add_trace(go.Scatter(
                    x=[x[i], x[j]], y=[y[i], y[j]],
                    mode="lines",
                    line=dict(width=0.3, color="rgba(255,255,255,0.08)"),
                    showlegend=False,
                    hoverinfo="skip",
                ))

    # Dots
    fig.add_trace(go.Scatter(
        x=x[:112], y=y[:112],
        mode="markers",
        marker=dict(size=5, color="#4fc3f7", opacity=0.8),
        name="Integer (112)",
        hovertemplate="(%{x:.3f}, %{y:.3f})<extra>Integer root</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x[112:], y=y[112:],
        mode="markers",
        marker=dict(size=5, color="#ffd700", opacity=0.8),
        name="Half-integer (128)",
        hovertemplate="(%{x:.3f}, %{y:.3f})<extra>Half-integer root</extra>",
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(x=0.02, y=0.98),
    )
    return fig


@callback(
    Output("density-plot", "figure"),
    Input("density-scale", "value"),
)
def update_density_plot(scale):
    y_vals = DENSITIES if scale == "linear" else LOG_DENSITIES

    colors = ["#ffd700" if p else "#4fc3f7" for p in IS_PROVEN]
    symbols = ["star" if p else "circle" for p in IS_PROVEN]

    fig = go.Figure()

    # Non-proven (estimates)
    non_proven_idx = [i for i, p in enumerate(IS_PROVEN) if not p]
    fig.add_trace(go.Scatter(
        x=[DIMS[i] for i in non_proven_idx],
        y=[y_vals[i] for i in non_proven_idx],
        mode="markers",
        marker=dict(size=6, color="#666", symbol="circle"),
        name="Best known",
        hovertemplate="dim %{x}: %{y:.4f}<extra></extra>",
    ))

    # Proven optimal
    proven_idx = [i for i, p in enumerate(IS_PROVEN) if p]
    fig.add_trace(go.Scatter(
        x=[DIMS[i] for i in proven_idx],
        y=[y_vals[i] for i in proven_idx],
        mode="markers+text",
        marker=dict(size=12, color="#ffd700", symbol="star"),
        text=[NAMES[i] for i in proven_idx],
        textposition="top center",
        textfont=dict(size=10, color="#ffd700"),
        name="Proven optimal",
        hovertemplate="dim %{x}: %{y:.6f}<br>%{text}<extra></extra>",
    ))

    y_title = "Packing Density" if scale == "linear" else "log(Packing Density)"

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Dimension",
        yaxis_title=y_title,
        margin=dict(l=60, r=20, t=30, b=50),
    )
    return fig


@callback(
    Output("magic-function-plot", "figure"),
    Input("magic-dims", "value"),
)
def update_magic_plot(selected_dims):
    fig = go.Figure()
    r = np.linspace(0.001, 4, 500)

    colors = {8: "#4fc3f7", 24: "#ffd700"}
    sign_changes = {8: sqrt(2), 24: 2.0}

    for dim in selected_dims:
        f_vals = np.array([approx_magic_function(ri, dim=dim) for ri in r])
        fig.add_trace(go.Scatter(
            x=r, y=f_vals,
            mode="lines",
            name=f"dim {dim}",
            line=dict(width=2.5, color=colors.get(dim, "white")),
        ))

        # Sign change marker
        sc = sign_changes[dim]
        fig.add_vline(
            x=sc,
            line_dash="dash",
            line_color=colors.get(dim, "white"),
            opacity=0.5,
            annotation_text=f"r = {sc:.3f}" if dim == 8 else f"r = {sc}",
            annotation_position="top",
        )

    # Zero line
    fig.add_hline(y=0, line_dash="dot", line_color="grey", opacity=0.3)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="r (radius)",
        yaxis_title="g(r)",
        margin=dict(l=60, r=20, t=30, b=50),
    )
    return fig


@callback(
    Output("theta-coefficients-plot", "figure"),
    Input("theta-terms", "value"),
)
def update_theta_plot(num_terms):
    n = list(range(num_terms + 1))
    coeffs = E4_COEFFS[:num_terms + 1]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=n,
        y=coeffs,
        marker_color=["#ce93d8" if c > 0 else "#666" for c in coeffs],
        text=[f"{c:,}" for c in coeffs],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="n=%{x}: %{y:,} vectors<extra></extra>",
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Shell index n (||v||^2 = 2n)",
        yaxis_title="Number of vectors",
        yaxis_type="log",
        margin=dict(l=60, r=20, t=30, b=50),
    )
    return fig


if __name__ == "__main__":
    print("Starting Viazovska Fields Simulator...")
    print("Open http://localhost:8050 in your browser")
    app.run(debug=True, port=8050)
