"""Crypto TA Scanner – Phase 1 stub."""
from typing import List, Dict, Any

def scan(symbols: List[str] = None, timeframes: List[str] = None) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL"]
    timeframes = timeframes or ["1h", "4h", "1d"]
    return {
        "signals": [
            {"symbol": s, "timeframe": tf, "bias": "neutral", "notes": "Stub – real indicators coming"}
            for s in symbols for tf in timeframes
        ],
        "summary": "Phase 1 stub scan complete. No live data connected yet.",
        "disclaimer": "Not financial advice. For research and educational purposes only."
    }
