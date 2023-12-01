---
title: Relating K and Phi
date: 2023-12-01
---

In geotechnical engineering we commonly have to determine the load the ground exerts on a structure. Two of the main parameters used to determine that are the coefficient of lateral earth pressure ($K_0$) and the soil friction angle ($\phi$). In certain scenarios it is also often useful to relate these to the overconsolidation ($OCR$) ratio of the soil and the respective $K_{0,oc}$ (the lateral earth pressure coefficient for overconsolidated soils). I recently had to do this for a project, but was having a tough time visualizing these relationships, so I made a couple of contour plots to help me out.

## The relationships

Two of the more common equations used to relate the OCR with $K_0$ and $\phi$ are:

### Wroth (1975) equation

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

And I used the python library `plotly` to make contour plots. Here is what I did:

```python
# Import libraries

```

{% plotlyChart "relating-k-and-phi-mayne_plotly", "relating-k-and-phi-mayne.json" %}
