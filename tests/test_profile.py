import numpy as np, pandas as pd, pathlib, pytest
from pychannelform import long_profile, reach_grades
from pychannelform.network import OFFSETS, _OPPOSITE

HERE = pathlib.Path(__file__).parent


def test_jacobs_creek_profile_matches_published():
    p = pd.read_csv(HERE / "jacobs_creek_profile.csv")
    assert len(p) == 252
    assert p.dist_m.iloc[-1] == pytest.approx(886.0, abs=1.0)
    fall = p.elev_m_ahd.iloc[0] - p.elev_m_ahd.iloc[-1]
    assert fall == pytest.approx(213.9, abs=0.3)
    assert 100 * fall / p.dist_m.iloc[-1] == pytest.approx(24.1, abs=0.2)


def test_reach_grades_find_the_chute():
    p = pd.read_csv(HERE / "jacobs_creek_profile.csv")
    g = reach_grades(p.dist_m.values, p.elev_m_ahd.values, 100.0)
    by_start = {int(a): gr for a, b, gr in g}
    assert by_start[200] > 0.35 and by_start[400] > 0.40      # 38-42% chute
    assert by_start[800] < 0.10                               # pondable toe


def test_offsets_are_self_inverse():
    for k, (dy, dx) in enumerate(OFFSETS):
        oy, ox = OFFSETS[_OPPOSITE[k]]
        assert (oy, ox) == (-dy, -dx)
