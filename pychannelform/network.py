"""Catchment delineation and channel extraction on a D8 receiver grid."""
from __future__ import annotations
import numpy as np
from collections import deque

OFFSETS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
_OPPOSITE = {k: 7 - k for k in range(8)}


def delineate(flow_dirs, row, col):
    """Every cell draining through (row, col). Breadth-first search upstream.

    NOTE for anyone adapting this to reservoir storage: a dam impounds only
    its own catchment.  Flooding a DEM without masking to this region lets the
    fill escape down-valley and returns a nonsense volume.
    """
    ny, nx = flow_dirs.shape
    m = np.zeros((ny, nx), bool); m[row, col] = True
    q = deque([(row, col)])
    while q:
        cy, cx = q.popleft()
        for k, (dy, dx) in enumerate(OFFSETS):
            uy, ux = cy + dy, cx + dx
            if 0 <= uy < ny and 0 <= ux < nx and not m[uy, ux] and flow_dirs[uy, ux] == _OPPOSITE[k]:
                m[uy, ux] = True; q.append((uy, ux))
    return m


def extract_channels(flow_acc_cells, cell_area_m2, min_area_ha=0.5):
    """Boolean channel network above a contributing-area threshold."""
    return (np.asarray(flow_acc_cells) * cell_area_m2 / 1e4) >= min_area_ha


def trace_downstream(flow_dirs, row, col, stop_mask=None, max_steps=10000):
    """Follow receivers downstream from (row, col). Unambiguous: one receiver
    per cell. Prefer this to walking upstream, which forks at every junction."""
    ny, nx = flow_dirs.shape
    path = [(row, col)]
    for _ in range(max_steps):
        k = flow_dirs[path[-1]]
        if k < 0:
            break
        dy, dx = OFFSETS[k]
        y, x = path[-1][0] + dy, path[-1][1] + dx
        if not (0 <= y < ny and 0 <= x < nx):
            break
        if stop_mask is not None and not stop_mask[y, x]:
            break
        path.append((y, x))
    return np.array(path)


def longest_path(flow_dirs, channel_mask, res, within=None):
    """The longest channel flow path, traced downstream from every head."""
    ny, nx = flow_dirs.shape
    sel = channel_mask & (within if within is not None else True)
    best_len, best = 0.0, None
    ys, xs = np.where(sel)
    for y, x in zip(ys, xs):
        has_donor = any(
            0 <= y+dy < ny and 0 <= x+dx < nx and flow_dirs[y+dy, x+dx] == _OPPOSITE[k] and sel[y+dy, x+dx]
            for k, (dy, dx) in enumerate(OFFSETS))
        if has_donor:
            continue                                   # start only from heads
        p = trace_downstream(flow_dirs, y, x, stop_mask=within)
        if len(p) < 2:
            continue
        L = float(np.hypot(np.diff(p[:,0]), np.diff(p[:,1])).sum() * res)
        if L > best_len:
            best_len, best = L, p
    return best, best_len
