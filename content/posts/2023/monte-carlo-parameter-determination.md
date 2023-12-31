---
title: Monte Carlo Parameter Determination
date: 2023-12-30
---

Over the past year I have spent a significant amount of time determining the geotechnical parameters to use for modeling and other analyses.
This led to a lot of thinking on how to have a better understanding of the range of conditions to expect at a given site.

While working with some risk analysis software, I learned methods that can be re-purposed for my parameter assessments.

## Monte Carlo simulation

A Monte Carlo simulation, in its simplest form, involves generating random variates (i.e. values) from a given
probability distribution and using those to run some sort of model. "Many" is typically in the thousands or more. After
running the model many times, you can determine to probability distribution of the model results, which can be used to 
help you make better decisions.

For this example, I will use a simple model: an equation (Mayne, 1982) to relate effective friction angle
($\phi^\prime$) and overconsolidation ratio ($OCR$) to determine the coefficient of lateral earth pressure at rest
($k_{0, oc}$).

$$k_{0, oc} = 1 - \sin{\phi^\prime} \times {OCR}^{\sin{\phi^\prime}}$$

This can be expressed in python as:
```python
def k_0_mayne_1982(phi: float, ocr: float) -> float:
    import numpy as np

    return (1 - np.sin(np.deg2rad(phi))) * (ocr ** (np.sin(np.deg2rad(phi))))
```

Generally, the process will be as follows:

1. Define the probability distribution and relevant statistics for the two inputs ($\phi^\prime$&nbsp; and &nbsp;${OCR}$).
1. Generate many random variates for the two inputs.
1. Run the model for all combinations of the inputs.
1. Determine the probability distribution and relevant statistics of the output.
1. Determine the expected value and 95% confidence interval of the output to report as the expected, maximum, and
minimum values.

I only have two inputs to my model (i.e. equation) and I'll consider both normally distributed (just for simplicity).
I'm sure there are ways to make this process more precise, but what is included here is just intended to be a
proof-of-concept.

## The Process

### Define Input Statistics and Distribution

I will assume both random variables are continuous and normally distributed, with the following statistics:

```python
# `std` is standard deviation
statistics = {
                "phi": {"mean": 32, "std": 2},
                "ocr": {"mean": 2, "std": 0.5}
                }
```

Using the normal distribution might not entirely appropriate here, both &nbsp;$\phi^\prime$&nbsp; and &nbsp;$OCR$&nbsp; have real upper and lower bounds that may not be fully expressed. To compensate for this, I keep the `std` low so that most of the generated variates will be within a realistic range. For &nbsp;$\phi^\prime$, ~95% of values will be between 28 and 36, for &nbsp;$OCR$, 1 and 3.

### Generate Random Variates

Now I generate 1000 random variates for each input:

```python
from scipy import stats

sample_size = 1000
statistics = {
                "phi": {"mean": 32, "std": 2},
                "ocr": {"mean": 2, "std": 0.5}
                }

# The stats.norm.rvs() method takes `loc` as the mean and `scale` as the
# standard deviation
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
```

### Run the Model With All Combinations

```python
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

fig.show()
```

<img src="/assets/svg/histogram-pdf-k-values.svg">

### Determine Probability Distribution

It looks like the results are _almost_ normally distributed, but with a slight left-skew. I found a beta distribution to fit pretty well:

```python
# Perform the distribution fit using `scipy.stats.beta`
a, b, loc, scale = stats.beta.fit(k_values)

# Define the min and max k (`x`) values to plot for the pdf (`y`) curve
x = np.linspace(stats.beta.ppf(0.001, a, b, loc, scale),
                stats.beta.ppf(0.999, a, b, loc, scale), 100)
y = stats.beta.pdf(x, a, b, loc, scale)
k_mean = stats.beta.mean(a, b, loc, scale)
k_std = stats.beta.std(a, b, loc, scale)

# Plot results
fig.add_trace(go.Scatter(x=x, y=y)).update(
    layout=dict(showlegend=False)
).add_annotation(
    text=f"<b>Beta Distribution</b><br>Shape parameter a: {round(a, 2)}<br>Shape parameter b: {round(b, 2)}<br>Mean: {round(k_mean, 2)}<br>Standard deviation: {round(k_std, 2)}",
    x=0.4,
    xanchor='left',
    y=3.5,
    yanchor='top',
    showarrow=False,
    align="left",
)

fig.show()
```
<img src="/assets/svg/dist-pdf-k-values.svg">

### Confidence Intervals (Results)

The fit in the image above looks pretty good, so I will skip a goodness-of-fit test for the sake of brevity. Now I can
use the same python library to calculate the 95% confidence interval. The upper and lower bounds will represent the
range within which I should expect 95% of observations to fall. In other words, given the input distribution and
statistics of &nbsp;$\phi^\prime$&nbsp; and &nbsp;$OCR$&nbsp;, 95% of observed &nbsp;$k_{0, oc}$&nbsp; will be between the upper and lower bounds of the 95%
confidence interval.

```python
# Define upper and lower confidence interval bounds
upper_bound, lower_bound = stats.beta.interval(confidence=0.95, a=a, b=b, loc=loc, scale=scale)

# Make pdf plotting data with the newly determined bounds
x = np.linspace(lower_bound,
                upper_bound, 100)
y = stats.beta.pdf(x, a, b, loc, scale)

# Add the 95% confidence interval area to the plot
fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy'))

fig.show()
```

See the results in the right side of the plot. The "Expected Value" would be the most representative of the soil, while
the upper and lower bounds may be reasonable limits to use when performing sensitivity analyses.

<img src="/assets/svg/confidence-pdf-k-values.svg">

## Room for Improvement

The above approach is a simplified version of what one could use for a real-world condition. Some ways I can think of to
improve it are:

- Use original data sets (instead of just the statistics) to produce a CDF, then use the CDF to produce the random
variates to use in the analysis.
- Remove outliers before performing the analysis (there may be benefit in removing outliers in the produced random
variates, though I'd have to do some more reading to confirm that).
- Assign practical limits to the input data, like a lower and upper bound on the inputs that represent real-world
bounds. This may be effectively address by implementing the two items above. 
