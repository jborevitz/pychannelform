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
