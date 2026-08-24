"""Synthetic tests for OI delta math used by CryptoTA."""

def oi_delta_pct(first: float, last: float):
    if first <= 0:
        return None
    return round(((last - first) / first) * 100, 2)


def test_oi_delta_up():
    assert oi_delta_pct(100.0, 110.0) == 10.0


def test_oi_delta_down():
    assert oi_delta_pct(100.0, 90.0) == -10.0


def test_oi_delta_invalid():
    assert oi_delta_pct(0.0, 10.0) is None
