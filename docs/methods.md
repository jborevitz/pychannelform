# pychannelform — methods

Conventions, traps and limitations. Findings from the block this was developed on are in the [README](../README.md).


## Trace downstream, not upstream

Each cell has exactly one receiver, so downstream tracing is unambiguous. Walking
upstream forks at every junction and a "follow the biggest donor" rule terminates
early in flat or filled reaches. `longest_path` starts from channel heads and traces
down.

## Clip late

A property boundary is a legal object, not a hydrological one. Delineate on a buffered
grid and clip only when reporting: at Avonside, 76% of the creek bowl's 88.7 ha
catchment lies outside the title, and routing on the boundary alone starves exactly
the hollows you are looking for.

## Grade, not degrees

`reach_grades` returns a fraction; multiply by 100 for percent. 100% is 45°, and the
two units are confused constantly — label both on every figure.

## Stop at the last junction that adds your own ground

A catchment model needs a closed divide, and the temptation is to walk downstream
until the divide closes tidily. Tabulate what each step costs instead. At Avonside the
candidate outlets closed 57.7, 60.4, **112.6**, 179.7 and 214.8 ha, while the title
area inside them went 17.2, 19.7, **30.2**, 30.2, 30.4 ha. Everything past the third
outlet is catchment without ownership: it dilutes the topographic-index distribution
with land no management can touch, and it buys nothing back.

Report both numbers for every candidate — catchment area and area you manage — and
pick the last junction where the second one is still rising.

## A wetness index is slope and upslope area, and nothing else

It does not know soil depth, grazing pressure, litter hydrophobicity, or any channel
narrower than the grid. When a landholder reports rills forming along mapped flow
lines, a middling index value there is not a contradiction: those features are below
the scale a 3 m surface and a catchment index are built to resolve. Do not ask the
field to explain away an index that was never measuring the thing in question.

Flow-routing choice is not cosmetic either. Over the same 112.6 ha, multiple-flow
direction gives mean ln(a/tanβ) = 5.47 and D-infinity gives 4.88 — an offset that
propagates directly into any transmissivity parameter calibrated against it.

## Soil water: three levels, two bands, one store

A cell's water column has three levels worth naming — saturation, field capacity and
wilting point — and the bands between them do different jobs:

- **saturation to field capacity** is the only water that drains under gravity. It is
  what becomes percolation, and in a TOPMODEL-type scheme it is what recharges the
  saturated store that generates baseflow.
- **field capacity to wilting point** is the only water plants get. This is the
  available water capacity (AWC), and it is the right definition of the store's
  *capacity*.
- **below wilting point** is real water held in clay films and micropores. Setting
  `capacity = AWC` excludes it by construction, so it never needs to be a state
  variable. Keep it in the diagram, not the model, and remember that an empty store
  means wilting point rather than oven-dry — which matters only for initial
  conditions.

From SLGA v2 these come from Drained Upper Limit (DUL) and L15, with AWC = DUL − L15,
saturation from bulk density, and root-zone depth from Depth of Soil capped by
rooting depth.

**Trap in the SLGA layout:** DUL and L15 are published under `/DUL/v1/` and `/L15/v1/`
on the TERN datastore. Their `v2` directories exist and are *empty*, so a client that
hardcodes `/v2/` resolves no filename and fails silently. `SOC` is a third layout
again, split into `30m/` and `90m/`. Pixel reads need a per-user TERN API key sent as
an `x-api-key` header; directory listings are public.
