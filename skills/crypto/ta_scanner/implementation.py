"""Crypto TA Scanner – Phase 3a
Binance multi-TF RSI + funding + volume confluence.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import httpx

DISCLAIMER = "**Not financial advice.** DYOR. Experimental agent skill for research only."

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"
BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_PREMIUM = "https://fapi.binance.com/fapi/v1/premiumIndex"

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
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)

def _fetch_klines(symbol: str, interval: str = "4h", limit: int = 100) -> List[float]:
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
            return [float(c[4]) for c in data]
    except Exception as e:
        print(f"Klines failed {symbol} {interval}: {e}")
        return []

def _fetch_24h(symbols: List[str]) -> Dict[str, Dict[str, Any]]:
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
                        "volume": float(item.get("quoteVolume") or item.get("volume") or 0),
                    }
                except (KeyError, ValueError):
                    pass
    return result

def _fetch_funding(symbol: str) -> Optional[float]:
    pair = SYMBOL_MAP.get(symbol.upper())
    if not pair:
        return None
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.get(BINANCE_PREMIUM, params={"symbol": pair})
            r.raise_for_status()
            data = r.json()
            return float(data.get("lastFundingRate", 0)) * 100
    except Exception as e:
        print(f"Funding failed {symbol}: {e}")
        return None

def _confluence(rsi_4h, rsi_1d, change_24h, funding, volume) -> tuple:
    reasons = []
    score = 0.0

    if rsi_4h is not None:
        if rsi_4h <= 30:
            reasons.append(f"4h RSI oversold ({rsi_4h})")
            score += 1.5
        elif rsi_4h >= 70:
            reasons.append(f"4h RSI overbought ({rsi_4h})")
            score -= 1.5
        elif rsi_4h <= 40:
            reasons.append(f"4h RSI low ({rsi_4h})")
            score += 0.5
        elif rsi_4h >= 60:
            reasons.append(f"4h RSI elevated ({rsi_4h})")
            score -= 0.5
        else:
            reasons.append(f"4h RSI {rsi_4h}")

    if rsi_1d is not None:
        if rsi_1d <= 35:
            reasons.append(f"1d RSI supportive ({rsi_1d})")
            score += 1.0
        elif rsi_1d >= 65:
            reasons.append(f"1d RSI elevated ({rsi_1d})")
            score -= 1.0
        else:
            reasons.append(f"1d RSI {rsi_1d}")

    if change_24h is not None:
        if change_24h >= 4:
            reasons.append(f"+{change_24h:.1f}% momentum")
            score += 1.0
        elif change_24h <= -4:
            reasons.append(f"{change_24h:.1f}% pressure")
            score -= 1.0
        else:
            reasons.append(f"{change_24h:+.1f}% 24h")

    if funding is not None:
        if funding > 0.05:
            reasons.append(f"Funding +{funding:.3f}%")
            score -= 0.4
        elif funding < -0.02:
            reasons.append(f"Funding {funding:.3f}%")
            score += 0.4
        else:
            reasons.append(f"Funding {funding:.3f}%")

    if volume is not None and volume > 0:
        # Just surface volume, light influence
        vol_m = volume / 1_000_000
        reasons.append(f"Vol ${vol_m:.1f}M")
        if vol_m > 500:  # high activity
            score += 0.2 if (change_24h or 0) > 0 else -0.1

    conf = max(0, min(5, int(round(abs(score) + 1.5))))
    if score >= 2.0:
        bias = "mild long"
    elif score >= 0.8:
        bias = "lean long / watch"
    elif score <= -2.0:
        bias = "mild short / caution"
    elif score <= -0.8:
        bias = "lean short / watch"
    else:
        bias = "neutral"

    return bias, conf, reasons

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

    symbols = [s for s in symbols if s in SYMBOL_MAP] or ["BTC", "ETH", "SOL"]

    ticker = _fetch_24h(symbols)
    signals = []
    rows = []

    for sym in symbols:
        closes_4h = _fetch_klines(sym, "4h", 100)
        closes_1d = _fetch_klines(sym, "1d", 50)
        rsi_4h = _rsi(closes_4h) if closes_4h else None
        rsi_1d = _rsi(closes_1d) if closes_1d else None
        funding = _fetch_funding(sym)

        t = ticker.get(sym, {})
        change = t.get("change_24h")
        price = t.get("price")
        volume = t.get("volume")

        bias, conf, reasons = _confluence(rsi_4h, rsi_1d, change, funding, volume)

        price_str = f"${price:,.2f}" if price and price >= 1 else (f"${price:.4f}" if price else "–")
        chg_str = f"{change:+.1f}%" if change is not None else "–"
        rsi4_str = str(rsi_4h) if rsi_4h is not None else "–"
        rsi1_str = str(rsi_1d) if rsi_1d is not None else "–"
        fund_str = f"{funding:.3f}%" if funding is not None else "–"
        vol_str = f"${volume/1e6:.1f}M" if volume else "–"
        notes = "; ".join(reasons[:3]) if reasons else "No data"

        signals.append({
            "symbol": sym,
            "price": price,
            "change_24h": change,
            "volume": volume,
            "rsi_4h": rsi_4h,
            "rsi_1d": rsi_1d,
            "funding": funding,
            "bias": bias,
            "confluence": conf,
            "notes": notes,
            "reasons": reasons,
        })

        rows.append(
            f"| {sym} | {price_str} | {chg_str} | {rsi4_str} | {rsi1_str} | {fund_str} | {vol_str} | {bias} | {conf}/5 |"
        )

    lines = [
        "# Crypto TA Scan – Phase 3a (RSI + Funding + Volume)",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        "Source: Binance public klines + ticker + funding",
        "",
        "| Symbol | Price | 24h | RSI 4h | RSI 1d | Funding | Volume | Bias | Conf |",
        "|--------|-------|-----|--------|--------|---------|--------|------|------|",
    ] + rows + [
        "",
        "### Method",
        "- RSI(14) on 4h and 1d",
        "- 24h price change + quote volume",
        "- Perpetual funding rate",
        "- Weighted confluence → bias",
        "",
        DISCLAIMER
    ]

    return {
        "signals": signals,
        "summary": "\n".join(lines),
        "disclaimer": DISCLAIMER,
        "version": "0.5.0",
        "live_prices": bool(ticker),
        "has_rsi": any(s.get("rsi_4h") is not None for s in signals),
        "has_funding": any(s.get("funding") is not None for s in signals),
        "has_volume": any(s.get("volume") for s in signals),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)

if __name__ == "__main__":
    print(scan()["summary"])
