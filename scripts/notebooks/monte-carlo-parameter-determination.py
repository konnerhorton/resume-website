import itertools as it
import numpy as np
import numpy.typing as npt
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from utilities.plotting_template import local_theme

sample_size = 1000
bound = 2
statistics = {"phi": {"mean": 32, "std": 3}, "ocr": {"mean": 2, "std": 0.5}}

phi_values = stats.norm.rvs(
    loc=statistics["phi"]["mean"],
    scale=statistics["phi"]["std"],
    size=sample_size,
)

ocr_values = stats.norm.rvs(
    loc=statistics["ocr"]["mean"],
    scale=statistics["ocr"]["std"],
    size=sample_size,
)


def k_0_mayne_1982(phi: float, ocr: float) -> float:
    return (1 - np.sin(np.deg2rad(phi))) * (ocr ** (np.sin(np.deg2rad(phi))))


k_values = np.array(
    [k_0_mayne_1982(i[0], i[1]) for i in it.product(phi_values, ocr_values)]
)

fig = go.Figure(go.Histogram(x=k_values, histnorm="probability density")).update(
    layout=dict(
        title="PDF of K values",
        height=500,
        width=800,
        template=local_theme,
        margin=dict(t=60, b=20, l=20, r=20),
        xaxis=dict(title="Lateral Earth Pressure at Rest"),
        yaxis=dict(title="PDF"),
    )
)

fig.write_image("histogram-pdf-k-values.svg")
fig.show()

# Perform the distribution fit using `scipy.stats.beta`
a, b, loc, scale = stats.beta.fit(k_values)

# Define the min and max k (`x`) values to plot for the pdf (`y`) curve
x = np.linspace(
    stats.beta.ppf(0.001, a, b, loc, scale),
    stats.beta.ppf(0.999, a, b, loc, scale),
    100,
)
y = stats.beta.pdf(x, a, b, loc, scale)
k_mean = stats.beta.mean(a, b, loc, scale)
k_std = stats.beta.std(a, b, loc, scale)

# Plot results on the previously made histogram (`fig`).
fig.add_trace(go.Scatter(x=x, y=y)).update(
    layout=dict(showlegend=False)
).add_annotation(
    text=f"<b>Beta Distribution</b><br>Shape parameter a: {round(a, 2)}<br>Shape parameter b: {round(b, 2)}<br>Mean: {round(k_mean, 2)}<br>Standard deviation: {round(k_std, 2)}",
    x=0.4,
    xanchor="left",
    y=3.5,
    yanchor="top",
    showarrow=False,
    align="left",
)

fig.write_image("dist-pdf-k-values.svg")
fig.show()

# Define upper and lower confidence interval bounds
lower_bound, upper_bound = stats.beta.interval(
    confidence=0.95, a=a, b=b, loc=loc, scale=scale
)

# Make pdf plotting data with the newly determined bounds
x = np.linspace(lower_bound, upper_bound, 100)
y = stats.beta.pdf(x, a, b, loc, scale)

# Add the 95% confidence interval area to the plot
fig.add_trace(go.Scatter(x=x, y=y, fill="tozeroy")).add_annotation(
    text=f"<b>95% Confidence Interval</b><br>Upper bound: {round(upper_bound, 2)}<br>Expected Value (mean): {round(k_mean, 2)}<br>Lower bound: {round(lower_bound, 2)}",
    x=0.8,
    xanchor="left",
    y=3.5,
    yanchor="top",
    showarrow=False,
    align="left",
)

fig.write_image("confidence-pdf-k-values.svg")
fig.show()
