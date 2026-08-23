"""Crypto TA Scanner – Phase 1.6 (richer multi-asset reports)."""
from typing import List, Dict, Any
from datetime import datetime

DISCLAIMER = "**Not financial advice.** DYOR. Experimental agent skill for research only."

def scan(symbols: List[str] = None, timeframes: List[str] = None) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL", "SUI", "XRP", "XLM"]
    timeframes = timeframes or ["4h", "1d"]

    bias_map = {
        "BTC": ("neutral-mild long", 3, "Holding key levels, funding neutral"),
        "ETH": ("mild long", 4, "Relative strength vs BTC"),
        "SOL": ("neutral", 2, "Watching for volume expansion"),
        "SUI": ("watch", 2, "High beta – needs confirmation"),
        "XRP": ("neutral", 2, "Range-bound"),
        "XLM": ("neutral", 1, "Low conviction"),
    }

    signals = []
    for s in symbols:
        bias, conf, notes = bias_map.get(s.upper(), ("unknown", 0, "No data"))
        for tf in timeframes:
            signals.append({
                "symbol": s.upper(),
                "timeframe": tf,
                "bias": bias,
                "confidence": conf / 5.0,
                "confluence": conf,
                "notes": notes
            })

    lines = [
        f"# Crypto TA Scan",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        f"Timeframes: {', '.join(timeframes)}",
        "",
        "| Symbol | Bias | Confluence | Notes |",
        "|--------|------|------------|-------|"
    ]
    seen = set()
    for sig in signals:
        key = sig["symbol"]
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"| {sig['symbol']} | {sig['bias']} | {sig['confluence']} | {sig['notes']} |")

    lines += [
        "",
        "### Confluence Guide",
        "- 1-2: Low / watch",
        "- 3: Moderate",
        "- 4+: Higher confluence (still not advice)",
        "",
        DISCLAIMER
    ]

    summary = "\n".join(lines)

    return {
        "signals": signals,
        "summary": summary,
        "disclaimer": DISCLAIMER,
        "version": "0.1.6",
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)

if __name__ == "__main__":
    print(scan()["summary"])
