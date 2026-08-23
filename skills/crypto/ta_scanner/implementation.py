"""Crypto TA Scanner – Phase 1.6 (cleaner interface + better stub output)."""
from typing import List, Dict, Any, Optional

def scan(
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    timeframe: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    symbols = symbols or kwargs.get("symbols") or ["BTC", "ETH", "SOL"]
    if isinstance(symbols, str):
        symbols = [s.strip() for s in symbols.split(",")]

    if timeframe and not timeframes:
        timeframes = [timeframe]
    timeframes = timeframes or ["3h", "1d"]

    signals = []
    for s in symbols:
        for tf in timeframes:
            signals.append({
                "symbol": s,
                "timeframe": tf,
                "bias": "neutral",
                "confidence": 0.0,
                "notes": "Stub – live data + RSI/MACD/funding/OI confluence coming when data sources are wired",
                "confluence": []
            })

    return {
        "signals": signals,
        "summary": f"Scanned {len(symbols)} symbols ({', '.join(symbols)}) across {len(timeframes)} timeframes. All neutral (stub mode).",
        "disclaimer": "Not financial advice. For research and educational purposes only.",
        "version": "0.1.6"
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)
