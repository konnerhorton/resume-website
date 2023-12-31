---
title: Plot a PDF on a Histogram
date: 2023-12-31
---

It is often useful to plot data as a histogram with a representative [probability density function (PDF)](https://en.wikipedia.org/wiki/Probability_density_function).
In python, this can be done in just a few lines of code:

## Import relevant libraries

```python
# Third party libraries
import numpy as np  # for creating arrays of numbers
import plotly.express as px  # for making plots
import plotly.graph_objects as go  # for adding data to existing plots
import plotly.io as pio  # allows me to use `plotly` templates
from scipy import stats  # for various probability distributions functions

# Local library
# where I stored my `plotly` theme
from utilities.plotting_template import local_theme

# Sets my plotly theme
pio.templates.default = local_theme
```

## Define the population statistics and the sample

```python
# Define the population statistics and sample size
pop_mean = 10
pop_std = 3
samp_N = 1000

# Create random variates following a normal distribution
## in the `stats.norm` library, `loc` and `scale` are mean and standard
## deviation respectively
sample = stats.norm.rvs(loc=pop_mean, scale=pop_std, size=samp_N)

# Get the sample statistics
samp_mean = np.mean(sample)
samp_std = np.std(sample)

# Compare the population and sample mean and standard deviation
print(f"Population mean: {pop_mean}; Sample mean: {samp_mean}")
print(f"Population std: {pop_std}; Sample std {samp_std}")
```

Output:

```
Population mean: 10; Sample mean: 10.11404341677092
Population std: 3; Sample std 3.10050438539277
```

## Plot the histogram

```python
# Plot the newly created random variates (`rvs`)
fig = px.histogram(x=sample, histnorm="probability density").update(
    layout=dict(height=500, width=800)
)

fig.show()
```

<img src="/assets/svg/plot-pdf-histogram-rvs-hist.svg">


## Generate plotting points for the pdf curve

```python
# Define the lower and upper bounds of the pdf to plot
## `stats.norm.ppf` returns the `x` value for the pdf at the probability `q` 
pdf_x_lower = stats.norm.ppf(q=0.01, loc=samp_mean, scale=samp_std)
pdf_x_upper = stats.norm.ppf(q=0.99, loc=samp_mean, scale=samp_std)

print(f"Lower bound: {pdf_x_lower}; Upper bound: {pdf_x_upper}")
```

Output:  

```Lower bound: 2.901191631358146; Upper bound: 17.326895202183696```


```python
# Create a 100 element array to represent the x-values for the pdf
pdf_x = np.linspace(start=pdf_x_lower, stop=pdf_x_upper, num=100)

pdf_x
```

Output:

```
array([ 2.90119163,  3.04690581,  3.19261999,  3.33833416,  3.48404834,
        3.62976252,  3.7754767 ,  3.92119087,  4.06690505,  4.21261923,
        4.35833341,  4.50404758,  4.64976176,  4.79547594,  4.94119012,
        5.08690429,  5.23261847,  5.37833265,  5.52404683,  5.669761  ,
        5.81547518,  5.96118936,  6.10690354,  6.25261771,  6.39833189,
        6.54404607,  6.68976025,  6.83547442,  6.9811886 ,  7.12690278,
        7.27261696,  7.41833113,  7.56404531,  7.70975949,  7.85547367,
        8.00118784,  8.14690202,  8.2926162 ,  8.43833038,  8.58404455,
        8.72975873,  8.87547291,  9.02118709,  9.16690126,  9.31261544,
        9.45832962,  9.6040438 ,  9.74975797,  9.89547215, 10.04118633,
       10.18690051, 10.33261468, 10.47832886, 10.62404304, 10.76975722,
       10.91547139, 11.06118557, 11.20689975, 11.35261393, 11.4983281 ,
       11.64404228, 11.78975646, 11.93547064, 12.08118481, 12.22689899,
       12.37261317, 12.51832735, 12.66404152, 12.8097557 , 12.95546988,
       13.10118406, 13.24689823, 13.39261241, 13.53832659, 13.68404077,
       13.82975494, 13.97546912, 14.1211833 , 14.26689748, 14.41261165,
       14.55832583, 14.70404001, 14.84975418, 14.99546836, 15.14118254,
       15.28689672, 15.43261089, 15.57832507, 15.72403925, 15.86975343,
       16.0154676 , 16.16118178, 16.30689596, 16.45261014, 16.59832431,
       16.74403849, 16.88975267, 17.03546685, 17.18118102, 17.3268952 ])
```


## Add the plotting points to the histogram

```python
# Create the y-values for the pdf
pdf_y = stats.norm.pdf(x=pdf_x, loc=samp_mean, scale=samp_std)

fig.add_trace(go.Scatter(x=pdf_x, y=pdf_y, showlegend=False))

fig.show()
```

<img src="/assets/svg/plot-pdf-histogram.svg">


## Turn it into a a function

The above code can be turned into a function so the process can be replicated:

```python
def plot_hist_and_norm_pdf(x: np.ndarray) -> go.Figure:
    """
    Plots a histogram with an associated pdf (assuming the data is normally distributed).
    
    Parameters
    ----------
    x : np.ndarray
        Sample data (list of observed values)
    
    Returns
    -------
    fig : go.Figure
        Plotly figure object with a histogram and pdf representing sample data `x`
    """
    mean = np.mean(sample)
    std = np.std(sample)

    pdf_x_lower = stats.norm.ppf(q=0.01, loc=mean, scale=std)
    pdf_x_upper = stats.norm.ppf(q=0.99, loc=mean, scale=std)
    pdf_x = np.linspace(start=pdf_x_lower, stop=pdf_x_upper, num=100)
    pdf_y = stats.norm.pdf(x=pdf_x, loc=mean, scale=std)

    
    fig = px.histogram(x=sample, histnorm="probability density").update(
    layout=dict(height=500, width=800)
)
    fig.add_trace(go.Scatter(x=pdf_x, y=pdf_y, showlegend=False))
    
    return fig

plot_hist_and_norm_pdf(sample)
```

<img src="/assets/svg/plot-pdf-histogram.svg">