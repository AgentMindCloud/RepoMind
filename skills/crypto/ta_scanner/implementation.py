"""Crypto TA Scanner – Phase 2c
Live Binance klines + RSI(14) + momentum confluence.
Falls back gracefully if network fails.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

DISCLAIMER = "**Not financial advice.** DYOR. Experimental agent skill for research only."

# Binance symbols
BINANCE_SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "SUI": "SUIUSDT",
    "XRP": "XRPUSDT",
    "XLM": "XLMUSDT",
    "BNB": "BNBUSDT",
    "DOGE": "DOGEUSDT",
    "ADA": "ADAUSDT",
    "AVAX": "AVAXUSDT",
}

INTERVAL_MAP = {
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "3h": "4h",   # closest
    "3H": "4h",
}

def _rsi(closes: List[float], period: int = 14) -> Optional[float]:
    """Simple RSI implementation."""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))

def _fetch_klines(symbol: str, interval: str = "4h", limit: int = 100) -> List[Dict]:
    """Fetch OHLCV from Binance public API."""
    pair = BINANCE_SYMBOLS.get(symbol.upper())
    if not pair:
        return []
    interval = INTERVAL_MAP.get(interval, "4h")
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": pair, "interval": interval, "limit": limit}
        with httpx.Client(timeout=12.0) as client:
            r = client.get(url, params=params)
            r.raise_for_status()
            raw = r.json()
        candles = []
        for k in raw:
            candles.append({
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            })
        return candles
    except Exception as e:
        print(f"Binance klines failed for {symbol}: {e}")
        return []

def _analyze_symbol(symbol: str, timeframes: List[str]) -> Dict[str, Any]:
    """Compute RSI + simple confluence for one symbol."""
    result = {
        "symbol": symbol,
        "price": None,
        "change_24h_approx": None,
        "rsi": {},
        "bias": "unknown",
        "confluence": 0,
        "notes": [],
        "live": False,
    }

    # Use 4h as primary, 1d as secondary
    primary_tf = "4h" if "4h" in timeframes or "1h" in timeframes else timeframes[0]
    candles = _fetch_klines(symbol, primary_tf, limit=100)

    if not candles:
        result["notes"].append("No kline data")
        return result

    closes = [c["close"] for c in candles]
    result["price"] = closes[-1]
    result["live"] = True

    # Approx 24h change from recent candles (rough)
    if len(closes) >= 7:
        # 6 x 4h ≈ 24h
        lookback = min(6, len(closes) - 1)
        change = ((closes[-1] - closes[-1 - lookback]) / closes[-1 - lookback]) * 100
        result["change_24h_approx"] = change

    rsi_val = _rsi(closes, 14)
    result["rsi"][primary_tf] = round(rsi_val, 1) if rsi_val is not None else None

    # Secondary timeframe
    if "1d" in timeframes and primary_tf != "1d":
        daily = _fetch_klines(symbol, "1d", limit=50)
        if daily:
            d_closes = [c["close"] for c in daily]
            d_rsi = _rsi(d_closes, 14)
            result["rsi"]["1d"] = round(d_rsi, 1) if d_rsi is not None else None

    # Confluence scoring
    conf = 0
    notes = []
    rsi4 = result["rsi"].get(primary_tf)
    rsi1d = result["rsi"].get("1d")

    if rsi4 is not None:
        if rsi4 < 30:
            conf += 2
            notes.append(f"RSI({primary_tf}) oversold ({rsi4})")
        elif rsi4 > 70:
            conf += 2
            notes.append(f"RSI({primary_tf}) overbought ({rsi4})")
        elif 40 <= rsi4 <= 60:
            conf += 1
            notes.append(f"RSI({primary_tf}) neutral ({rsi4})")
        else:
            notes.append(f"RSI({primary_tf}) {rsi4}")

    if rsi1d is not None:
        if rsi1d < 35:
            conf += 1
            notes.append(f"Daily RSI supportive ({rsi1d})")
        elif rsi1d > 65:
            conf += 1
            notes.append(f"Daily RSI elevated ({rsi1d})")

    change = result.get("change_24h_approx")
    if change is not None:
        if change > 4:
            conf += 1
            notes.append(f"+{change:.1f}% momentum")
        elif change < -4:
            conf += 1
            notes.append(f"{change:.1f}% pressure")

    # Final bias
    if conf >= 4 and rsi4 is not None and rsi4 < 35:
        bias = "mild long (oversold bounce potential)"
    elif conf >= 4 and rsi4 is not None and rsi4 > 65:
        bias = "mild short / caution (overbought)"
    elif conf >= 3:
        bias = "watch / mild directional"
    else:
        bias = "neutral"

    result["bias"] = bias
    result["confluence"] = min(conf, 5)
    result["notes"] = notes
    return result

def scan(
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL", "SUI", "XRP", "XLM"]
    if isinstance(symbols, str):
        symbols = [s.strip().upper() for s in symbols.split(",")]
    else:
        symbols = [s.upper() for s in symbols]

    timeframes = timeframes or ["4h", "1d"]

    analyses = []
    for s in symbols:
        analyses.append(_analyze_symbol(s, timeframes))

    # Markdown report
    lines = [
        f"# Crypto TA Scan – RSI + Binance Klines",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        f"Source: Binance public klines + RSI(14)",
        "",
        "| Symbol | Price | RSI 4h | RSI 1d | Bias | Conf | Notes |",
        "|--------|-------|--------|--------|------|------|-------|"
    ]

    for a in analyses:
        price_str = f"${a['price']:,.2f}" if a.get("price") else "–"
        rsi4 = a["rsi"].get("4h") or a["rsi"].get(timeframes[0]) or "–"
        rsi1d = a["rsi"].get("1d", "–")
        notes_str = "; ".join(a["notes"][:2]) if a["notes"] else "–"
        lines.append(
            f"| {a['symbol']} | {price_str} | {rsi4} | {rsi1d} | {a['bias']} | {a['confluence']} | {notes_str} |"
        )

    lines += [
        "",
        "### Confluence Guide",
        "- 0-1: Low conviction",
        "- 2-3: Moderate / watch",
        "- 4-5: Higher confluence (still not advice)",
        "",
        "### Method",
        "- RSI(14) on Binance 4h + 1d klines",
        "- Simple momentum overlay",
        "- No funding/OI yet (next)",
        "",
        DISCLAIMER
    ]

    live_count = sum(1 for a in analyses if a.get("live"))

    return {
        "signals": analyses,
        "summary": "\n".join(lines),
        "disclaimer": DISCLAIMER,
        "version": "0.3.0",
        "live_prices": live_count > 0,
        "live_count": live_count,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)

if __name__ == "__main__":
    print(scan()["summary"])
