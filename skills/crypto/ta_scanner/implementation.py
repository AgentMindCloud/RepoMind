"""Crypto TA Scanner – Phase 2d: Multi-TF RSI (4h + 1d) + Binance funding rate."""
from typing import List, Dict, Any, Optional, Tuple
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
    """Wilder-style RSI."""
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

def _fetch_klines(symbol: str, interval: str = "4h", limit: int = 60) -> List[float]:
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
        print(f"Klines {symbol} {interval} failed: {e}")
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
                    }
                except (KeyError, ValueError):
                    pass
    return result

def _fetch_funding(symbol: str) -> Optional[float]:
    """Last funding rate from Binance USDT-M futures (public)."""
    pair = SYMBOL_MAP.get(symbol.upper())
    if not pair:
        return None
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.get(BINANCE_PREMIUM, params={"symbol": pair})
            r.raise_for_status()
            data = r.json()
            rate = data.get("lastFundingRate")
            return round(float(rate) * 100, 4) if rate is not None else None  # as %
    except Exception as e:
        print(f"Funding {symbol} failed: {e}")
        return None

def _confluence(
    rsi_4h: Optional[float],
    rsi_1d: Optional[float],
    change_24h: Optional[float],
    funding: Optional[float]
) -> Tuple[str, int, List[str]]:
    """Score multi-TF RSI + momentum + funding."""
    reasons = []
    score = 0.0

    # RSI 4h
    if rsi_4h is not None:
        if rsi_4h >= 70:
            reasons.append(f"4h RSI {rsi_4h} OB")
            score -= 1.2
        elif rsi_4h <= 30:
            reasons.append(f"4h RSI {rsi_4h} OS")
            score += 1.2
        elif rsi_4h >= 60:
            reasons.append(f"4h RSI {rsi_4h}")
            score -= 0.4
        elif rsi_4h <= 40:
            reasons.append(f"4h RSI {rsi_4h}")
            score += 0.4
        else:
            reasons.append(f"4h RSI {rsi_4h}")

    # RSI 1d
    if rsi_1d is not None:
        if rsi_1d >= 70:
            reasons.append(f"1d RSI {rsi_1d} OB")
            score -= 1.0
        elif rsi_1d <= 30:
            reasons.append(f"1d RSI {rsi_1d} OS")
            score += 1.0
        elif rsi_1d >= 60:
            reasons.append(f"1d RSI {rsi_1d}")
            score -= 0.3
        elif rsi_1d <= 40:
            reasons.append(f"1d RSI {rsi_1d}")
            score += 0.3

    # 24h momentum
    if change_24h is not None:
        if change_24h >= 4.0:
            reasons.append(f"+{change_24h:.1f}% strong")
            score += 1.0
        elif change_24h >= 1.5:
            reasons.append(f"+{change_24h:.1f}%")
            score += 0.4
        elif change_24h <= -4.0:
            reasons.append(f"{change_24h:.1f}% weak")
            score -= 1.0
        elif change_24h <= -1.5:
            reasons.append(f"{change_24h:.1f}%")
            score -= 0.4

    # Funding rate (positive = longs paying shorts → crowded long)
    if funding is not None:
        if funding >= 0.05:
            reasons.append(f"fund {funding:.3f}% high")
            score -= 0.6
        elif funding <= -0.02:
            reasons.append(f"fund {funding:.3f}% neg")
            score += 0.5
        else:
            reasons.append(f"fund {funding:.3f}%")

    if score >= 2.0:
        return "bullish", 5, reasons
    if score >= 0.8:
        return "mild bullish", 3, reasons
    if score <= -2.0:
        return "bearish", 5, reasons
    if score <= -0.8:
        return "mild bearish", 3, reasons
    return "neutral", 2, reasons

def scan(
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]:
    symbols = symbols or ["BTC", "ETH", "SOL", "SUI", "XRP"]
    if isinstance(symbols, str):
        symbols = [s.strip().upper() for s in symbols.replace(",", " ").split() if s.strip()]
    else:
        symbols = [s.upper() for s in symbols]

    symbols = [s for s in symbols if s in SYMBOL_MAP][:6] or ["BTC", "ETH", "SOL"]

    ticker = _fetch_24h(symbols)
    signals = []
    rows = []

    for sym in symbols:
        closes_4h = _fetch_klines(sym, "4h", 60)
        closes_1d = _fetch_klines(sym, "1d", 40)
        rsi_4h = _rsi(closes_4h) if closes_4h else None
        rsi_1d = _rsi(closes_1d) if closes_1d else None
        funding = _fetch_funding(sym)

        t = ticker.get(sym, {})
        change = t.get("change_24h")
        price = t.get("price")

        bias, conf, reasons = _confluence(rsi_4h, rsi_1d, change, funding)

        price_str = f"${price:,.2f}" if price and price >= 1 else (f"${price:.4f}" if price else "–")
        chg_str = f"{change:+.1f}%" if change is not None else "–"
        rsi4 = str(rsi_4h) if rsi_4h is not None else "–"
        rsi1 = str(rsi_1d) if rsi_1d is not None else "–"
        fund_str = f"{funding:.3f}%" if funding is not None else "–"
        notes = " · ".join(reasons[:4]) if reasons else "No data"

        signals.append({
            "symbol": sym,
            "price": price,
            "change_24h": change,
            "rsi_4h": rsi_4h,
            "rsi_1d": rsi_1d,
            "funding_rate_pct": funding,
            "bias": bias,
            "confidence": conf / 5.0,
            "confluence": conf,
            "notes": notes,
            "reasons": reasons,
        })

        rows.append(
            f"| {sym} | {price_str} | {chg_str} | {rsi4} | {rsi1} | {fund_str} | {bias} | {conf}/5 |"
        )

    lines = [
        "# Crypto TA Scan – Multi-TF RSI + Funding",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        "Source: Binance public klines (4h + 1d) + 24h ticker + funding rate",
        "",
        "| Symbol | Price | 24h | RSI 4h | RSI 1d | Funding | Bias | Conf |",
        "|--------|-------|-----|--------|--------|---------|------|------|",
    ] + rows + [
        "",
        "### How to read",
        "- **RSI 4h / 1d**: <30 oversold, >70 overbought",
        "- **Funding**: positive = crowded longs (slightly bearish pressure), negative = opposite",
        "- **Bias**: confluence of multi-TF RSI + 24h momentum + funding",
        "- Lightweight heuristic only – not a trading system",
        "",
        DISCLAIMER
    ]

    return {
        "signals": signals,
        "summary": "\n".join(lines),
        "disclaimer": DISCLAIMER,
        "version": "0.4.0",
        "live_prices": bool(ticker),
        "has_rsi": any(s.get("rsi_4h") is not None for s in signals),
        "has_funding": any(s.get("funding_rate_pct") is not None for s in signals),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)
