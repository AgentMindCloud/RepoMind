# Skill: Crypto TA Scanner

**Name:** ta_scanner  
**Version:** 0.4.0  
**Category:** crypto  
**Safety:** high (research only)

## Description
Multi-timeframe technical snapshot using public Binance data.

- Live price + 24h change
- RSI(14) on 4h and 1d closes
- Last funding rate (USDT-M)
- Simple confluence bias

## Inputs
- `symbols`: list of tickers (default BTC, ETH, SOL, SUI, XRP)

## Outputs
- Markdown table + structured signals
- Always includes “Not financial advice” disclaimer

## Data sources
- Binance spot klines + 24h ticker
- Binance futures premiumIndex (funding)
