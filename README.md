# pychannelform

**Where the water goes after it lands.**

Rain does not stay where it falls, and a fence does not divert it. If you want to
know which part of a block will dry out first, where erosion starts, where a
revegetation planting will actually get water, or how much of the flow through your
gully is someone else's rain, you need the drainage structure rather than the
elevation map.

This package takes a flow grid derived from a bare-earth surface and returns the
things a land manager and an ecologist both ask for: the catchment above any point,
the channel network at a chosen threshold, the longest flow path through a property,
and the long profile and reach grades along it.

The useful consequence, found repeatedly, is that **a property boundary and a water
system almost never coincide.** Planning drainage, dams or riparian plantings inside
the fence line alone means planning for a fraction of the water involved.

## Where this sits

Six small packages, one chain. Each does one thing and each is useful on its own.

| package | reads | gives you |
|---|---|---|
| [pylidarterrain](https://github.com/jborevitz/pylidarterrain) | classified airborne LiDAR | the ground surface a plant actually stands on: slope, aspect, how much sky it can see |
| [pyterrainsol](https://github.com/jborevitz/pyterrainsol) | that surface + daily weather | light and evaporative demand, cell by cell, day by day |
| [pyterrainwind](https://github.com/jborevitz/pyterrainwind) | that surface + reanalysis wind | wind exposure, and the extra demand it carries |
| **pychannelform** (this one) | that surface | **where the water goes: catchments, channels, long profiles** |
| [pylandstore](https://github.com/jborevitz/pylandstore) | channels + demand | where to hold water, and what it costs to move it uphill |
| [pylandgraze](https://github.com/jborevitz/pylandgraze) | all of the above + a herd | where the animals should be, hour by hour and season by season |

## Quickstart

```python
from pychannelform import (delineate, extract_channels, longest_path,
                           long_profile, reach_grades)

catchment = delineate(flow_dirs, outlet_row, outlet_col)
channels  = extract_channels(flow_acc, cell_area_m2=9.0, min_area_ha=0.5)
path, length = longest_path(flow_dirs, channels, res=3.0, within=farm_mask)
dist, z = long_profile(dem, path, res=3.0)
grades = reach_grades(dist, z, bin_m=100.0)
```

The flow grid comes from [`pylidarterrain`](https://github.com/jborevitz/pylidarterrain).

## What it found at 845 Avonside

![Catchment and wetness](docs/catchment_and_wetness.png)

*At 3 m the drainage network resolves into individual channels rather than a smear.
The creek bowl is 88.7 ha, of which only **21.4 ha (orange) lies inside the
property** — 67.2 ha (blue) drains through from neighbouring land, and a further
24.9 ha of the farm drains to other outlets entirely. **The block straddles a divide;
it is not one water system.***

Three quarters of the water moving through the main gully is the neighbours' rain.
That sets what is and is not controllable: in-channel structures intercept a
catchment that is mostly external, while anything aimed at the farm's own runoff has
only 21.4 ha to work with. It also means a wet year upstream arrives here regardless
of how the block itself is managed.

![Longitudinal profile](docs/long_profile.png)

*The main channel: 886 m on this property, falling 213.9 m at a **24.1% mean grade**,
with a 38–42% chute through its middle. Tributary junctions are marked with the
direction each arrives from — only the lowest one, at 962.3 m, actually captures the
northern neighbour's catchment.*

A quarter grade in a channel is energy. Water arrives fast, so erosion control and
any planting in that line has to survive flow rather than merely tolerate wet feet,
and the chute through the middle is where the gradient — and the risk — concentrates.
Where that water can usefully be held, and what it costs to get it back uphill, is
[`pylandstore`](https://github.com/jborevitz/pylandstore).

### Choosing the catchment a soil-water model runs on

![Catchments at 845 Avonside](docs/avonside_catchments.png)

*The 46.81 ha title drains three ways: **north-east** (215 ha, carrying 30.4 ha of
the title), **south-east** (38 ha, 11.5 ha) and **west** (>375 ha but truncated by the
tile block, 4.8 ha). Panel b takes the north-east system apart: four tributaries —
the main drainage from the south (34 ha), Jacob's Creek down the middle of the farm
(13 ha), the south creek into Eva's pond (11 ha) and the north creek that clips the
boundary (30 ha) — plus 48 ha of trunk hillslope.*

The outlet is **E 655084, N 5966608 (MGA55), 930 m**, the trunk cell immediately above
the junction where a 44 ha northern tributary arrives. That point closes **112.6 ha**
inside the four-tile DEM and holds **30.2 ha of the title — every hectare of it that
drains north-east**.

The instructive part is what further outlets buy. A gorge 230 m downstream closes a
tidy 179.7 ha, and the tile edge closes 214.8 ha; **neither adds a single hectare of
title.** Going downstream for a cleaner-looking catchment spends the model's
topographic-index distribution on land the owner cannot act on. Stop at the last
junction that still adds ground you manage.

Routing every title cell to the creek also corrects an intuition. The block's
north-facing woodland (85.4% of it within 45° of north) feeds the trunk at **69
separate entry points over a median 196 m** — it is the valley's north wall, not a
catchment of its own. The long paths belong to the open farm land at the top: a
median **709 m**, arriving at just two cells.

> Note on an earlier figure above: the 88.7 ha "creek bowl" reported from this block
> was delineated at the tributary junction 300 m upstream of this outlet, on an
> earlier two-tile surface. Re-measured on the four-tile grid that junction closes
> 90.5 ha with 19.9 ha inside the title. The ~2% difference in area and 7% in title
> share is a DEM-build difference, not a change of definition.

### The soil store in one cell

![Soil water in one cell](docs/soil_water_cell.png)

*Three levels and two bands. Only water between field capacity and saturation drains,
and that drainage is what feeds a saturated store and becomes baseflow. Only water
between field capacity and wilting point feeds plants. Everything below wilting point
is real but is deliberately outside the model.*


## Methods

The conventions this package enforces, the traps it exists to prevent, and what it
deliberately does not do are in **[`docs/methods.md`](docs/methods.md)**.

Methods and results are kept apart on purpose. The methods travel to any site and
will be re-checked against new ground and simulated data; the findings above are one
46 ha property in the Snowy Monaro, some of them specific to it and some likely to
generalise. Either can then be argued with without disturbing the other.
