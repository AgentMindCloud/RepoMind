"""Crypto TA Scanner – Phase 2c with Binance klines + RSI(14)."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import httpx

DISCLAIMER = "**Not financial advice.** DYOR. Experimental agent skill for research only."

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"
BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr"

SYMBOL_MAP = {
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

def _rsi(closes: List[float], period: int = 14) -> Optional[float]:
    """Calculate RSI(14)."""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)

def _fetch_klines(symbol: str, interval: str = "4h", limit: int = 50) -> List[float]:
    """Return list of close prices from Binance."""
    pair = SYMBOL_MAP.get(symbol.upper())
    if not pair:
        return []
    try:
        with httpx.Client(timeout=12.0) as client:
            r = client.get(BINANCE_KLINES, params={
                "symbol": pair,
                "interval": interval,
                "limit": limit
            })
            r.raise_for_status()
            data = r.json()
            return [float(candle[4]) for candle in data]  # close
    except Exception as e:
        print(f"Klines failed for {symbol}: {e}")
        return []

def _fetch_24h(symbols: List[str]) -> Dict[str, Dict[str, Any]]:
    """Fetch 24h ticker data."""
    try:
        with httpx.Client(timeout=12.0) as client:
            r = client.get(BINANCE_TICKER)
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        print(f"24h ticker failed: {e}")
        return {}

    result = {}
    for item in data:
        pair = item.get("symbol")
        for sym, mapped in SYMBOL_MAP.items():
            if pair == mapped and sym in symbols:
                try:
                    result[sym] = {
                        "price": float(item["lastPrice"]),
                        "change_24h": float(item["priceChangePercent"]),
                    }
                except (KeyError, ValueError):
                    pass
    return result

def _bias(rsi: Optional[float], change_24h: Optional[float]) -> tuple[str, int, List[str]]:
    """Simple confluence from RSI + 24h change."""
    reasons = []
    score = 0.0

    if rsi is not None:
        if rsi >= 70:
            reasons.append(f"RSI {rsi} overbought")
            score -= 1.0
        elif rsi <= 30:
            reasons.append(f"RSI {rsi} oversold")
            score += 1.0
        elif rsi >= 60:
            reasons.append(f"RSI {rsi} elevated")
            score -= 0.3
        elif rsi <= 40:
            reasons.append(f"RSI {rsi} low")
            score += 0.3
        else:
            reasons.append(f"RSI {rsi}")

    if change_24h is not None:
        if change_24h >= 4.0:
            reasons.append(f"+{change_24h:.1f}% strong")
            score += 1.0
        elif change_24h >= 1.5:
            reasons.append(f"+{change_24h:.1f}%")
            score += 0.5
        elif change_24h <= -4.0:
            reasons.append(f"{change_24h:.1f}% weak")
            score -= 1.0
        elif change_24h <= -1.5:
            reasons.append(f"{change_24h:.1f}%")
            score -= 0.5
        else:
            reasons.append(f"{change_24h:.1f}% flat")

    if score >= 1.5:
        return "bullish", 4, reasons
    if score >= 0.5:
        return "mild bullish", 3, reasons
    if score <= -1.5:
        return "bearish", 4, reasons
    if score <= -0.5:
        return "mild bearish", 3, reasons
    return "neutral", 2, reasons

def scan(
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL", "SUI", "XRP"]
    if isinstance(symbols, str):
        symbols = [s.strip().upper() for s in symbols.split(",")]
    else:
        symbols = [s.upper() for s in symbols]

    symbols = [s for s in symbols if s in SYMBOL_MAP] or ["BTC", "ETH", "SOL"]

    ticker = _fetch_24h(symbols)
    signals = []
    rows = []

    for sym in symbols:
        closes = _fetch_klines(sym, interval="4h", limit=50)
        rsi = _rsi(closes) if closes else None
        t = ticker.get(sym, {})
        change = t.get("change_24h")
        price = t.get("price")

        bias, conf, reasons = _bias(rsi, change)

        price_str = f"${price:,.2f}" if price and price >= 1 else (f"${price:.4f}" if price else "–")
        chg_str = f"{change:+.1f}%" if change is not None else "–"
        rsi_str = str(rsi) if rsi is not None else "–"
        notes = " | ".join(reasons) if reasons else "No data"

        signals.append({
            "symbol": sym,
            "price": price,
            "change_24h": change,
            "rsi_4h": rsi,
            "bias": bias,
            "confidence": conf / 5.0,
            "confluence": conf,
            "notes": notes,
            "reasons": reasons,
        })

        rows.append(f"| {sym} | {price_str} | {chg_str} | {rsi_str} | {bias} | {conf}/5 | {notes} |")

    lines = [
        "# Crypto TA Scan (Binance + RSI)",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        "Source: Binance public klines (4h) + 24h ticker",
        "",
        "| Symbol | Price | 24h | RSI(4h) | Bias | Conf | Notes |",
        "|--------|-------|-----|---------|------|------|-------|",
    ] + rows + [
        "",
        "### Notes",
        "- RSI(14) calculated on 4h closes.",
        "- Bias combines RSI levels + 24h momentum.",
        "- This is a lightweight confluence heuristic, not full multi-timeframe TA.",
        "- Funding rate + multi-TF RSI planned next.",
        "",
        DISCLAIMER
    ]

    return {
        "signals": signals,
        "summary": "\n".join(lines),
        "disclaimer": DISCLAIMER,
        "version": "0.3.0",
        "live_prices": bool(ticker),
        "has_rsi": any(s.get("rsi_4h") is not None for s in signals),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)
