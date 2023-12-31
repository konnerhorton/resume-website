import plotly.io as pio

pio.templates["local_theme"] = pio.templates["simple_white"]
pio.templates["local_theme"]["layout"]["xaxis"]["showgrid"] = True
pio.templates["local_theme"]["layout"]["xaxis"]["mirror"] = True
pio.templates["local_theme"]["layout"]["xaxis"]["title"]["standoff"] = 5
pio.templates["local_theme"]["layout"]["yaxis"]["showgrid"] = True
pio.templates["local_theme"]["layout"]["yaxis"]["mirror"] = True
pio.templates["local_theme"]["layout"]["yaxis"]["title"]["standoff"] = 5
pio.templates["local_theme"]["layout"]["font"] = dict(color="black", family="arial")
pio.templates["local_theme"]["layout"]["shapedefaults"] = dict(
    line=dict(width=1, color="black"), opacity=1
)
pio.templates["local_theme"]["layout"]["margin"] = dict(t=60, b=20, l=20, r=20)

local_theme = pio.templates["local_theme"]
