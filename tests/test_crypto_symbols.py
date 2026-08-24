"""Basic tests for CryptoTA symbol handling and scan shape."""
from skills.crypto.ta_scanner.implementation import scan, SYMBOL_MAP

def test_symbol_map_has_core_assets():
    for s in ["BTC", "ETH", "SOL", "SUI", "XRP"]:
        assert s in SYMBOL_MAP

def test_scan_returns_expected_keys():
    # This may hit live network; keep assertions structural
    result = scan(symbols=["BTC"])
    assert "signals" in result
    assert "summary" in result
    assert "version" in result
    assert result["version"].startswith("0.")
    assert isinstance(result["signals"], list)

def test_scan_accepts_comma_string():
    result = scan(symbols="BTC, ETH")
    assert "signals" in result
