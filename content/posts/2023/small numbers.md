---
title: The Law of Small Numbers
date: 2023-11-20
---

In 1971 two psychologists wrote a paper titled ["Belief in the Law of Small Numbers"](http://stats.org.uk/statistical-inference/TverskyKahneman1971.pdf). Their thesis is that individuals (both trained scientists and laypeople) consider a sample (a set of data) drawn from a population to be more representative of the population than they should, especially when the sample is small. In other words, when dealing with small data sets, we will erroneously assume that our "mean" value is _very_ representative of the population mean.

Statistical theory suggests (via the [Law of Large Numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers)) that as the sample size increases, the sample mean becomes more and more similar to the population mean. The Law of Small Numbers considers the inverse: as sample size decreases, the sample mean becomes less and less similar to the population mean. When we have small samples, we should expect to see extreme values.

In geotechnical engineering it is common to be working with small datasets. So we should expect extreme values in our data, and not always trust the mean to be "representative" of the soil, rock, or whatever else we are measuring. To illustrate this, I ran an experiment where I:

- drew random samples from a normally distributed population;
- calculated the sample mean;
- then plotted the sample means versus the sample size (N)

For each sample size (I used 1 through 30), I drew 100 samples to calculate the mean. So, by the end I had 3000 sample mean values. The results are plotted below (along with some python code if you want to plot it yourself). Only when N > 5 does the sample mean consistently fall within one standard deviation of the population mean.

What is the point of this? In geotechincal engineering (or anywhere else small sample size are common), it is prudent to use rigorous  statistical tools to "correct" for small samples. We would also benefit from using more probabilistic approaches to determine confidence intervals of a given statistical value.

{% include "html/small_numbers.html" %}

```python
import numpy as np
import pandas as pd
import plotly.express as px

# Define population statistics
population_mean = 20
population_std = 3

# Number of samples to take for each round of events
observation_count_range = np.arange(1, 31)

# Number of observations to take for each sampling event
sampling_events = 100


# Perform the sampling events
records = []
for sample_count in observation_count_range:
    for event in np.arange(sampling_events):
        # the sample consists of random variables drawn normally distributed data
        # (as defined with the population statistics above)
        sample = np.random.normal(
            loc=population_mean, scale=population_std, size=sample_count
        )

        sample_mean = np.mean(sample)

        records.append({"count": sample_count, "event": event, "mean": sample_mean})

# Create the dataframe (table) for the calculated values
df = pd.DataFrame(records)

# Plot the data to show how variation in sample mean changes with the sample count
fig = px.scatter(df, x="count", y="mean").update_layout(
    height=500,
    width=800,
    xaxis=dict(title="sample count (N)", rangemode="tozero"),
    yaxis=dict(title="sample mean"),
    margin=dict(t=20, b=20, l=20, r=20),
)

# Add the horizontal lines and labels
fig.add_hline(
    y=population_mean + population_std,
).add_hline(
    y=population_mean - population_std,
).add_annotation(
    text="Horizontal lines represent mean +/- one standard deviation",
    xref="paper",
    x=0.5,
    yref="paper",
    y=0.8,
    showarrow=False,
)

fig.show()
```
