# SLGA soil data for the Avonside four-tile block

Soil and Landscape Grid of Australia (SLGA) v2, clipped to the four-tile LiDAR block
around 845 Avonside and committed here so the hydrology work is reproducible without
a TERN account.

## Licence — this directory is NOT MIT

The code in this repository is MIT. **The data in this directory is not.** It is
redistributed under the **Creative Commons Attribution Licence (CC BY)** under which
TERN and CSIRO release the SLGA. You may share and adapt it provided you give
appropriate credit, cite the scientific publications describing the methods, and link
to the Soil and Landscape Grid of Australia homepage.

If you use these files, cite the SLGA, not this repository:

> Soil and Landscape Grid of Australia, Terrestrial Ecosystem Research Network (TERN)
> and CSIRO. https://esoil.io/TERNLandscapes/Public/Pages/SLGA/index.html

Per-attribute citations and the conditions of use are in the CSIRO Data Access Portal
metadata record for each product, and in the TERN portal records.

*Caveat on the licence:* the current SLGA pages state CC BY. One legacy CSIRO page
(`clw.csiro.au/aclep/tern`) still says CC BY-NC. If you intend commercial use, check
the DAP record for the specific product rather than relying on this note.

**TERN's own disclaimer applies and matters here:** SLGA is a first approximation from
digital soil mapping, the products may contain errors and artefacts, and TERN
explicitly advises that *for farm or catchment scale studies, more detailed soil
information may be available from local soil survey agencies*. At 90 m these layers
are ~30x coarser than the 3 m terrain they are used with.

## What is here

| file | what |
|---|---|
| `avonside_slga_4tile.csv` | tidy table, 3,696 rows (one per 90 m pixel) x 46 columns: `lon`, `lat`, and 44 layers |
| `avonside_slga_4tile.npz` | the same 44 layers as 56 x 66 arrays, plus `_shape`, `_transform`, `_crs`, `_bbox` |

**Grid.** EPSG:4326, 56 rows x 66 columns, pixel 0.00083333 deg (3 arc-seconds, ~90 m).
Bounding box lon 148.69049 to 148.74589, lat -36.46222 to -36.41553 — the four
Berridale 2018 LiDAR tiles (MGA55 E 652000-656000, N 5964000-5968000) plus a 0.005 deg
pad. Values are the SLGA **expected value (EV)** surface; the 5th and 95th percentile
layers were not pulled.

## Layers

Six standard GlobalSoilMap depth slices, named `<ATT>_<from>_<to>` in **millimetres**:
`000_005`, `005_015`, `015_030`, `030_060`, `060_100`, `100_200`.

| attribute | layers | units | what it is |
|---|---|---|---|
| `SND`, `SLT`, `CLY` | 6 each | % | sand, silt, clay fractions — they sum to 100 at every pixel |
| `BDW` | 6 | g/cm3 | bulk density of the whole soil |
| `DUL` | 6 | % v/v | drained upper limit — **field capacity** |
| `L15` | 6 | % v/v | water content at 15 bar — **wilting point** |
| `AWC` | 6 | % v/v | available water capacity, equals `DUL - L15` |
| `DES` | 1 (`000_200`) | m | depth of soil |
| `DER` | 1 (`000_999`) | m | depth to rock (depth of regolith) |

## How it was fetched

Windowed reads of the national cloud-optimised GeoTIFFs on the TERN datastore:

```
https://data.tern.org.au/model-derived/slga/NationalMaps/SoilAndLandscapeGrid/<ATT>/<ver>/
```

Filenames are resolved from the public directory listing rather than hardcoded,
because each attribute is published on its own release date. Pixel reads need a
per-user TERN API key sent as an `x-api-key` header (free, from
`account.tern.org.au`); directory listings are public.

**Two traps worth knowing:**

1. **`DUL` and `L15` live under `/v1/`, not `/v2/`.** Their `v2` directories exist and
   are *empty*, so a client that hardcodes `/v2/` resolves no filename and fails
   silently. `SOC` is a third layout again, split into `30m/` and `90m/`.
2. **`DUL`, `L15` and `AWC` are `uint16`.** `src.read(masked=True).filled(np.nan)`
   raises on them — cast to float32 first, then apply `src.nodatavals`.

## Summary over this window

Sandy soil on shallow regolith. Topsoil (0-5 cm) is 69-81% sand, 10-17% silt, 8-17%
clay. Across the 113 ha modelling catchment: bulk density 1.31 g/cm3, porosity 0.46,
AWC 110 mm over a 1 m profile but only 38 mm over 0.3 m.

The notable pair is **depth of soil 0.53 m against depth to rock 1.68 m** — about
1.16 m of weathered material below the mapped soil, which is where a subsoil store
lives and where deeper-rooted trees must be working.
