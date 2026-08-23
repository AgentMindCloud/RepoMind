# Skill: Crypto TA Scanner (Heavy)

**Name:** ta_scanner  
**Version:** 0.1.0  
**Category:** crypto  
**Safety:** high (financial disclaimer required)

## Description
Multi-timeframe technical analysis scanner for BTC/ETH/SOL and selected alts. Looks for confluence across RSI, MACD, funding rates, open interest, and candlestick patterns.

## Inputs
- symbols: list[str] (default ["BTC", "ETH", "SOL"])
- timeframes: list[str] (default ["1h", "4h", "1d"])

## Outputs
- signals: list[dict]
- summary: str
- disclaimer: always present

## Notes
- Not financial advice
- Designed for later integration with live data sources (Binance, Coingecko, etc.)
