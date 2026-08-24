"""Crypto TA Scanner – Phase 2a with live price data from public APIs."""
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

DISCLAIMER = "**Not financial advice.** DYOR. Experimental agent skill for research only."

# CoinGecko free public endpoint (no key required for basic prices)
COINGECKO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "SUI": "sui",
    "XRP": "ripple",
    "XLM": "stellar",
}

def _fetch_prices(symbols: List[str]) -> Dict[str, float]:
    """Fetch current USD prices. Returns empty dict on failure."""
    ids = [COINGECKO_IDS.get(s.upper()) for s in symbols if s.upper() in COINGECKO_IDS]
    ids = [i for i in ids if i]
    if not ids:
        return {}
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ",".join(ids), "vs_currencies": "usd", "include_24hr_change": "true"}
        with httpx.Client(timeout=12.0) as client:
            r = client.get(url, params=params)
            r.raise_for_status()
            data = r.json()
        prices = {}
        for sym, cid in COINGECKO_IDS.items():
            if cid in data:
                prices[sym] = {
                    "usd": data[cid].get("usd"),
                    "change_24h": data[cid].get("usd_24h_change")
                }
        return prices
    except Exception as e:
        print(f"Price fetch failed: {e}")
        return {}

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
    prices = _fetch_prices(symbols)

    # Simple heuristic bias from 24h change (placeholder until full OHLCV)
    signals = []
    for s in symbols:
        p = prices.get(s, {})
        change = p.get("change_24h")
        price = p.get("usd")

        if change is None:
            bias, conf, notes = "unknown", 0, "No live price data"
        elif change > 3.5:
            bias, conf, notes = "mild long", 3, f"+{change:.1f}% 24h – momentum"
        elif change < -3.5:
            bias, conf, notes = "mild short / watch", 3, f"{change:.1f}% 24h – pressure"
        else:
            bias, conf, notes = "neutral", 2, f"{change:.1f}% 24h – range"

        if price:
            notes = f"${price:,.2f} | {notes}"

        for tf in timeframes:
            signals.append({
                "symbol": s,
                "timeframe": tf,
                "bias": bias,
                "confidence": conf / 5.0,
                "confluence": conf,
                "notes": notes,
                "price_usd": price,
                "change_24h": change
            })

    # Markdown report
    lines = [
        f"# Crypto TA Scan (live prices)",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        f"Source: CoinGecko public + simple momentum heuristic",
        "",
        "| Symbol | Price | 24h | Bias | Confluence | Notes |",
        "|--------|-------|-----|------|------------|-------|"
    ]
    seen = set()
    for sig in signals:
        if sig["symbol"] in seen:
            continue
        seen.add(sig["symbol"])
        price_str = f"${sig['price_usd']:,.2f}" if sig.get("price_usd") else "–"
        chg = f"{sig['change_24h']:+.1f}%" if sig.get("change_24h") is not None else "–"
        lines.append(
            f"| {sig['symbol']} | {price_str} | {chg} | {sig['bias']} | {sig['confluence']} | {sig['notes']} |"
        )

    lines += [
        "",
        "### Notes",
        "- Bias is a simple 24h momentum heuristic only (not full TA yet).",
        "- Full RSI/MACD/funding/OI confluence is next.",
        "",
        DISCLAIMER
    ]

    return {
        "signals": signals,
        "summary": "\n".join(lines),
        "disclaimer": DISCLAIMER,
        "version": "0.2.0",
        "live_prices": bool(prices),
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

def run(**kwargs) -> Dict[str, Any]:
    return scan(**kwargs)

if __name__ == "__main__":
    print(scan()["summary"])
