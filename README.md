# pychannelform

Catchments, channel networks and longitudinal profiles from a D8 flow grid.

```python
from pychannelform import delineate, extract_channels, longest_path, long_profile, reach_grades

catchment = delineate(flow_dirs, outlet_row, outlet_col)
channels  = extract_channels(flow_acc, cell_area_m2=9.0, min_area_ha=0.5)
path, length = longest_path(flow_dirs, channels, res=3.0, within=farm_mask)
dist, z = long_profile(dem, path, res=3.0)
grades = reach_grades(dist, z, bin_m=100.0)
```

## What it found at 845 Avonside

![Catchment and wetness](docs/catchment_and_wetness.png)

*At 3 m the drainage network resolves into individual channels. The delineated creek
bowl is 88.7 ha, of which only 21.4 ha (orange) lies inside the property — 67.2 ha
(blue) drains through from neighbouring land, and a further 24.9 ha of the farm drains
to other outlets entirely. The block straddles a divide; it is not one water system.*

![Longitudinal profile](docs/long_profile.png)

*The main channel: 886 m on this property, falling 213.9 m at a 24.1% mean grade, with
a 38–42% chute through its middle. Tributary junctions are marked with the direction
each arrives from — only the lowest one, at 962.3 m, actually captures the northern
neighbour's catchment.*

## Methods

The conventions this package enforces, the traps it exists to prevent, and what it
deliberately does not do are in **[`docs/methods.md`](docs/methods.md)**.

Methods and results are kept apart on purpose. The methods travel to any site and
will be re-checked against new ground and simulated data; the findings above are one
47 ha property in the Snowy Monaro, some of them specific to it and some likely to
generalise. Either can then be argued with without disturbing the other.
