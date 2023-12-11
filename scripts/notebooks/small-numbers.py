import os
import numpy as np
import pandas as pd


import plotly


import plotly.express as px


import plotly.io as pio


from utilities.plotting_template import local_theme

pio.templates.default = local_theme


# Define population statistics


population_mean = 20


population_std = 3


# Number of samples to take for round of events


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

fig.write_image("small-numbers.svg")
