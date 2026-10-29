"""Longitudinal profiles, reach grades and tributary junctions."""
from __future__ import annotations
import numpy as np
from .network import OFFSETS, _OPPOSITE


def long_profile(dem, path, res):
    """(distance_m, elevation) along a traced path."""
    z = np.asarray(dem)[path[:,0], path[:,1]]
    step = np.hypot(np.diff(path[:,0]), np.diff(path[:,1])) * res
    return np.concatenate([[0.0], np.cumsum(step)]), z


def reach_grades(dist, z, bin_m=100.0):
    """Mean grade (fraction) per fixed-length reach. Grade, not degrees --
    100% is 45 degrees, and the two are confused constantly."""
    out = []
    for a in np.arange(0, dist[-1], bin_m):
        m = (dist >= a) & (dist < a + bin_m)
        if m.sum() < 2:
            continue
        dz = z[m][0] - z[m][-1]; dx = max(dist[m][-1] - dist[m][0], 1e-9)
        out.append((a, a + bin_m, dz / dx))
    return out


def junctions(flow_acc_cells, flow_dirs, path, cell_area_m2, min_trib_ha=0.8):
    """Tributary junctions on a path, with the direction each arrives from."""
    acc = np.asarray(flow_acc_cells); ny, nx = acc.shape
    found = []
    for i, (y, x) in enumerate(map(tuple, path)):
        donors = [(acc[y+dy, x+dx] * cell_area_m2 / 1e4, y+dy, x+dx, dy, dx)
                  for k, (dy, dx) in enumerate(OFFSETS)
                  if 0 <= y+dy < ny and 0 <= x+dx < nx and flow_dirs[y+dy, x+dx] == _OPPOSITE[k]]
        if len(donors) < 2:
            continue
        donors.sort(reverse=True)
        trib_ha, ty, tx, dy, dx = donors[1]
        if trib_ha < min_trib_ha:
            continue
        comp = ("N" if dy < 0 else "S" if dy > 0 else "") + ("E" if dx > 0 else "W" if dx < 0 else "")
        found.append(dict(index=i, row=y, col=x, main_ha=donors[0][0],
                          trib_ha=trib_ha, trib_row=ty, trib_col=tx, from_direction=comp))
    return found
