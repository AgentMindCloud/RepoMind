"""Crypto TA Scanner – Phase 1.5 (structured stub with clearer interface)."""
from typing import List, Dict, Any

def scan(symbols: List[str] = None, timeframes: List[str] = None) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL"]
    timeframes = timeframes or ["1h", "4h", "1d"]

    signals = []
    for s in symbols:
        for tf in timeframes:
            signals.append({
                "symbol": s,
                "timeframe": tf,
                "bias": "neutral",
                "confidence": 0.0,
                "notes": "Stub – live data + indicators (RSI/MACD/funding/OI) coming when data sources are wired",
                "confluence": []
            })

    return {
        "signals": signals,
        "summary": f"Scanned {len(symbols)} symbols across {len(timeframes)} timeframes. All neutral (stub mode).",
        "disclaimer": "Not financial advice. For research and educational purposes only.",
        "version": "0.1.5"
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)
