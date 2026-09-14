"""Independent state reconstruction and signed-interval checks for P113-S1."""
import math
import random

import departure_trade as trade
import pytest


def independent_coverage(d, budget, mass, payload, lo, hi):
    f = mass / (mass + payload)
    return any(max(a, d - budget) <= min(b, d + budget) + 1e-10
               for a, b in [(-f * hi, -f * lo), (f * lo, f * hi)])


def test_apsides_from_energy_and_angular_momentum():
    for alt in trade.INPUTS["reference_altitudes_km"]:
        r = trade.RE + alt * 1000
        for offset in trade.INPUTS["opposite_apsis_offsets_km"]:
            v = math.sqrt(trade.MU / r) + trade.required_increment(alt, alt + offset)
            energy = v * v / 2 - trade.MU / r
            h = r * v
            a = -trade.MU / (2 * energy)
            if offset == 0:
                assert abs(a - r) < 1e-3
                assert trade.required_increment(alt, alt) == pytest.approx(0, abs=1e-10)
                continue
            e = math.sqrt(max(0, 1 + 2 * energy * h * h / trade.MU ** 2))
            got = sorted([(a * (1 - e) - trade.RE) / 1000,
                          (a * (1 + e) - trade.RE) / 1000])
            assert got == pytest.approx(sorted([alt, alt + offset]), abs=1e-6)


def test_entire_sweep_and_momentum():
    for row in trade.build()["cases"]:
        d, budget, mass = (row[k] for k in ["required_payload_increment_m_s",
                                          "host_budget_m_s", "retained_host_mass_kg"])
        prior = False
        for name, cap in trade.INPUTS["maximum_speed_screens_m_s"].items():
            result = row["screens"][name]
            covered = result["kinematic_screen_covered"]
            assert covered == independent_coverage(d, budget, mass, 4, .5, cap)
            assert not prior or covered
            prior = covered
            if not covered:
                continue
            h, u = result["host_impulse_m_s"], result["relative_speed_m_s"]
            vp, vh = result["payload_increment_m_s"], result["retained_host_increment_m_s"]
            assert abs(4 * vp + mass * vh - (mass + 4) * h) <= 1e-8
            assert abs(vp - vh - u) <= 1e-10
            assert abs(vp - d) <= 1e-10
            assert abs(h) <= budget + 1e-10
            assert .5 - 1e-10 <= abs(u) <= cap + 1e-10
            if budget == 0:
                assert abs(u - d * (mass + 4) / mass) <= 1e-10


def test_random_intervals_and_budget_monotonicity():
    rng = random.Random(113)
    for _ in range(2000):
        d, b, mass, payload = rng.uniform(-150, 150), rng.uniform(0, 100), rng.uniform(50, 2000), rng.uniform(1, 10)
        lo, hi = rng.uniform(.1, 2), rng.uniform(2, 120)
        first = trade.allocate(d, b, mass, payload, lo, hi)["kinematic_screen_covered"]
        assert first == independent_coverage(d, b, mass, payload, lo, hi)
        assert not first or trade.allocate(d, b + 10, mass, payload, lo, hi)["kinematic_screen_covered"]


def test_negative_controls_and_boundaries():
    assert not trade.allocate(0, 0, 300, 4, .5, 2)["kinematic_screen_covered"]
    assert trade.allocate(0, 2, 300, 4, .5, 2)["kinematic_screen_covered"]
    assert trade.allocate(2 * 300 / 304, 0, 300, 4, .5, 2)["kinematic_screen_covered"]
    with pytest.raises(ValueError):
        trade.required_increment(450, 500, circular_destination=True)
    for alt, target in [(450, 0), (0, 450), (450, float("nan")), (float("inf"), 450)]:
        with pytest.raises(ValueError):
            trade.required_increment(alt, target)
    args = [10, 2, 300, 4, .5, 2]
    for index, value in [(0, float("nan")), (1, -1), (2, 0), (3, -4), (4, 0), (5, .1)]:
        changed = args.copy()
        changed[index] = value
        with pytest.raises(ValueError):
            trade.allocate(*changed)


def test_stroke_bounds():
    bound = trade.stroke_bound(100, 25, 8)
    assert bound["ideal_minimum_stroke_m"] == pytest.approx(20.3943242596, abs=1e-8)
    assert bound["mean_acceleration_over_stroke_g"] * trade.G0 * 16 == pytest.approx(100 ** 2)
    for values in [(-1, 25, 8), (100, 0, 8), (100, 25, 0), (float("inf"), 25, 8)]:
        with pytest.raises(ValueError):
            trade.stroke_bound(*values)


def test_freshness_refuses_corruption_without_writing(tmp_path):
    rendered = trade.outputs(trade.build())
    assert rendered == trade.outputs(trade.build())
    assert len(trade.check_outputs(tmp_path, rendered)) == 2
    for name, content in rendered.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    assert trade.check_outputs(tmp_path, rendered) == []
    name = "analysis/results/departure_trade.json"
    (tmp_path / name).write_text("corrupted result\n")
    assert trade.check_outputs(tmp_path, rendered) == [name]
    assert (tmp_path / name).read_text() == "corrupted result\n"
