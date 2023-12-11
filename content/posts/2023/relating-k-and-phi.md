---
title: Relating K and Phi
date: 2023-12-01
---

In geotechnical engineering we commonly have to determine the load the ground exerts on a structure. Two of the main parameters used to determine that are the coefficient of lateral earth pressure ($K_0$) and the soil friction angle ($\phi$). In certain scenarios it is also often useful to relate these to the overconsolidation ($OCR$) ratio of the soil and the respective $K_{0,oc}$ (the lateral earth pressure coefficient for overconsolidated soils). I recently had to do this for a project, but was having a tough time visualizing these relationships, so I made a couple of contour plots to help me out.

## The relationships

Two of the more common equations used to relate the OCR with $K_0$ and $\phi$ are:

### Wroth (1975) Equation

$$K_{0, oc}=OCR * (1-sin\phi^{\prime})-\frac{\nu * (OCR - 1)}{1-\nu}$$
$v$ is the poisson's ratio for the soil

### Mayne & Kulhawy (1982) Equation

$$K_{0, oc}=K_{0, nc}*OCR^{sin\phi^{\prime}}$$

Where $K_{0, nc}$ is determined via the Jaky equation:

$$K_{0, nc}=1-sin\phi^{\prime}$$

Resulting in:

$$K_{0, oc}=(1-sin\phi^{\prime})*OCR^{sin\phi^{\prime}}$$

## Visualization

In the equations above, there are three variables: $OCR$, $K_{0, oc}$. To visualize these it seemed appropriate to use a contour plot with two variables on the x and y axes, then the third variable would be used as the z value in the contours. Somewhat arbitrarily I decided to use:  

$xaxis => OCR$  
$yaxis => \phi^\prime$  
$zaxis => K_{0, oc}$  

And I used the python library `plotly` to make contour plots (Mayne on the left, Wroth on the right):

<div class="svg-container">
    <img src="/assets/svg/relating-k-and-phi-mayne.svg" alt="Mayne">
    <img src="/assets/svg/relating-k-and-phi-wroth.svg" alt="Wroth">
</div>

### The script

```python
# Import third party libraries
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from utilities.plotting_template import local_theme

pio.templates.default = local_theme


# Write functions to represent equations
def get_k0nc_jacky(phi: float) -> float:
    return 1 - np.sin(np.deg2rad(phi))


def get_k0oc_wroth(phi: float, OCR: float, v: float) -> float:
    return OCR * (get_k0nc_jacky(phi)) - (v * (OCR - 1)) / (1 - v)


def get_k0oc_mayne(phi: float, OCR: float) -> float:
    return get_k0nc_jacky(phi) * OCR ** (np.sin(np.deg2rad(phi)))


# Define range of values for phi and OCR
phi = np.linspace(0, 45)  # Creates a array of 100 values from 0 to 45
OCR = np.linspace(0, 5.5)  # Creates a array of 100 values from 0 to 5.5

# Define poisson's ratio to be used in `get_k0oc_wroth()`
v = 0.25

# Vectorize equations so that they can be used to create a numpy 2D array
vec_get_k0oc_wroth = np.vectorize(pyfunc=get_k0oc_wroth)
vec_get_k0oc_mayne = np.vectorize(pyfunc=get_k0oc_mayne)

# Create 2D arrays from the equations
k0oc_wroth = vec_get_k0oc_wroth(phi=phi, OCR=OCR, v=v)
k0oc_mayne = vec_get_k0oc_mayne(phi=phi, OCR=OCR)


# Plot contours for both methods
def plot_countour(OCR: np.ndarray, phi: np.ndarray, k0oc: np.ndarray) -> np.ndarray:
    fig = go.Figure(
    go.Contour(
        z=k0oc,
        x=OCR,
        y=phi,
        contours=dict(start=0, end=1, size=0.05, showlabels=True),
        colorbar=dict(title="K<sub>0,oc</sub>"),
    )
).update_layout(
    height=350,
    width=450,
    xaxis=dict(title=dict(text="OCR, unitless", standoff=5), tickfont=dict(size=12),dtick=0.5),
    yaxis=dict(title=dict(text="Effective Friction Angle, deg", standoff=5), dtick=5),
    margin=dict(t=10, b=10, l=40, r=0)
)
    return fig

fig_mayne = plot_countour(OCR, phi, k0oc_mayne)
fig_wroth= plot_countour(OCR, phi, k0oc_wroth)
```
