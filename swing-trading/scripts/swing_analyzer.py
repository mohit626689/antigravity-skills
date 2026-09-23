#!/usr/bin/env python3
"""
Swing Trading Technical Analyzer & Setup Scorer (agentskills.io standard)
Analyzes price and volume data using moving averages, RSI(14), MACD, ATR, and volume expansion
to identify high-probability short-term swing setups (3 to 15 days).
"""

import sys
import json
import math
import argparse
from typing import List, Dict, Any, Tuple


def calculate_sma(data: List[float], period: int) -> List[float]:
    """Calculates Simple Moving Average."""
    sma = []
    for i in range(len(data)):
        if i < period - 1:
            sma.append(None)
        else:
            window = data[i - period + 1 : i + 1]
            sma.append(sum(window) / period)
    return sma


def calculate_ema(data: List[float], period: int) -> List[float]:
    """Calculates Exponential Moving Average."""
    ema = []
    multiplier = 2.0 / (period + 1)
    # First EMA value is SMA
    sma_first = sum(data[:period]) / period
    for i in range(len(data)):
        if i < period - 1:
            ema.append(None)
        elif i == period - 1:
            ema.append(sma_first)
        else:
            prev = ema[-1]
            val = (data[i] - prev) * multiplier + prev
            ema.append(val)
    return ema


def calculate_rsi(closes: List[float], period: int = 14) -> List[float]:
    """Calculates Relative Strength Index (Wilder's smoothing)."""
    if len(closes) <= period:
        return [50.0] * len(closes)

    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))

    rsi = [None] * (period)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    if avg_loss == 0:
        rsi.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi.append(100.0 - (100.0 / (1.0 + rs)))

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100.0 - (100.0 / (1.0 + rs)))

    return rsi


def calculate_macd(closes: List[float]) -> Tuple[List[float], List[float], List[float]]:
    """Calculates MACD Line (12-26), Signal Line (9-EMA of MACD), and Histogram."""
    ema12 = calculate_ema(closes, 12)
    ema26 = calculate_ema(closes, 26)

    macd_line = []
    for i in range(len(closes)):
        if ema12[i] is not None and ema26[i] is not None:
            macd_line.append(ema12[i] - ema26[i])
        else:
            macd_line.append(None)

    valid_macd = [v for v in macd_line if v is not None]
    if len(valid_macd) < 9:
        return macd_line, [0.0] * len(closes), [0.0] * len(closes)

    signal_ema = calculate_ema(valid_macd, 9)
    signal_line = [None] * (len(closes) - len(valid_macd)) + signal_ema

    histogram = []
    for i in range(len(closes)):
        if macd_line[i] is not None and signal_line[i] is not None:
            histogram.append(macd_line[i] - signal_line[i])
        else:
            histogram.append(0.0)

    return macd_line, signal_line, histogram


def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
    """Calculates Average True Range."""
    tr = [highs[0] - lows[0]]
    for i in range(1, len(closes)):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        tr.append(max(hl, hc, lc))

    atr = calculate_ema(tr, period)
    return atr


def analyze_swing_setup(candles: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Main evaluation function for a list of daily OHLCV candlestick dictionaries:
    Each candle: {"open": ..., "high": ..., "low": ..., "close": ..., "volume": ...}
    """
    if len(candles) < 30:
        raise ValueError(f"Insufficient history: Need at least 30 candles for swing analysis, got {len(candles)}.")

    closes = [c["close"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    volumes = [c.get("volume", 1.0) for c in candles]

    current_price = closes[-1]
    current_vol = volumes[-1]

    # Technical Indicators
    ema20 = calculate_ema(closes, 20)
    sma50 = calculate_sma(closes, min(50, len(closes)))
    sma200 = calculate_sma(closes, min(200, len(closes))) if len(closes) >= 100 else [closes[0]] * len(closes)
    rsi14 = calculate_rsi(closes, 14)
    macd_line, signal_line, hist = calculate_macd(closes)
    atr14 = calculate_atr(highs, lows, closes, 14)

    curr_ema20 = ema20[-1] if ema20[-1] is not None else current_price
    curr_sma50 = sma50[-1] if sma50[-1] is not None else current_price
    curr_sma200 = sma200[-1] if sma200[-1] is not None else current_price
    curr_rsi = rsi14[-1] if rsi14[-1] is not None else 50.0
    curr_macd_hist = hist[-1]
    curr_atr = atr14[-1] if atr14[-1] is not None else (highs[-1] - lows[-1])

    # Volume comparison (20-day volume average)
    vol_period = min(20, len(volumes))
    avg_volume = sum(volumes[-vol_period:]) / vol_period
    volume_surge_ratio = current_vol / avg_volume if avg_volume > 0 else 1.0

    # Key Support & Resistance levels (last 20 days)
    lookback = min(20, len(candles))
    recent_high = max(highs[-lookback:])
    recent_low = min(lows[-lookback:])

    # Setup Scoring Engine (0 - 100)
    score = 0
    reasons = []

    # 1. Macro Trend Filter (Max 25 pts)
    if current_price > curr_sma200:
        score += 25
        reasons.append("Price is trading comfortably above 200 SMA (Long-term Bullish Trend).")
    elif current_price > curr_sma50:
        score += 15
        reasons.append("Price is above 50 SMA (Intermediate Bullish Trend).")
    else:
        reasons.append("⚠️ Price is below key long-term moving averages (Downtrend Risk).")

    # 2. Moving Average Alignment (Max 15 pts)
    if curr_ema20 > curr_sma50:
        score += 15
        reasons.append("20 EMA is above 50 SMA (Short-term momentum aligned with trend).")

    # 3. Momentum & RSI Health (Max 20 pts)
    if 50 <= curr_rsi <= 70:
        score += 20
        reasons.append(f"RSI(14) is in the sweet spot ({curr_rsi:.1f}) - strong momentum without extreme exhaustion.")
    elif 40 <= curr_rsi < 50:
        score += 15
        reasons.append(f"RSI(14) is at {curr_rsi:.1f} - healthy pullback to dynamic support zone.")
    elif curr_rsi > 70:
        score += 8
        reasons.append(f"⚠️ RSI is overbought ({curr_rsi:.1f}) - elevated momentum, trail stop closely.")
    else:
        reasons.append(f"⚠️ RSI is bearish/weak ({curr_rsi:.1f}).")

    # 4. MACD Momentum (Max 15 pts)
    if curr_macd_hist > 0:
        score += 15
        reasons.append("MACD histogram is positive and expanding (Upward acceleration).")
    elif hist[-1] > hist[-2]:
        score += 10
        reasons.append("MACD histogram is turning upwards (Momentum exhaustion of pullback).")

    # 5. Volume Confirmation (Max 15 pts)
    if volume_surge_ratio >= 1.5:
        score += 15
        reasons.append(f"Institutional volume surge: {volume_surge_ratio:.2f}x of 20-day average.")
    elif volume_surge_ratio >= 1.1:
        score += 10
        reasons.append(f"Above-average volume expansion ({volume_surge_ratio:.2f}x).")
    else:
        reasons.append(f"Volume is neutral or light ({volume_surge_ratio:.2f}x).")

    # 6. Price Action Setup Recognition (Max 10 pts)
    # Detect Breakout vs Pullback
    pct_from_20d_high = ((recent_high - current_price) / recent_high) * 100.0
    pct_from_20_ema = abs((current_price - curr_ema20) / curr_ema20) * 100.0

    setup_type = "Consolidation / Base"
    if pct_from_20d_high <= 2.0 and volume_surge_ratio >= 1.3:
        setup_type = "🚀 20-Day Range Breakout"
        score += 10
        reasons.append("High-volume breakout near 20-day resistance high.")
    elif pct_from_20_ema <= 1.5 and current_price >= curr_ema20:
        setup_type = "🎯 20 EMA Dip Pullback"
        score += 10
        reasons.append("Classic pullback test of the rising 20 EMA support.")
    elif current_price < curr_ema20 and current_price > curr_sma50:
        setup_type = "⏳ 50 SMA Trend Support Test"
        score += 8
        reasons.append("Testing 50 SMA support area in an ongoing uptrend.")

    # Calculate Trade Execution Levels
    # Stop Loss: Placed below the recent swing low or 1.5 * ATR below current price
    atr_stop = current_price - (1.5 * curr_atr)
    swing_low_stop = recent_low * 0.99  # 1% buffer below swing low
    stop_loss = max(atr_stop, swing_low_stop)
    if stop_loss >= current_price:
        stop_loss = current_price * 0.95

    risk_per_share = current_price - stop_loss
    target_1 = current_price + (risk_per_share * 2.0)  # 1:2 R:R
    target_2 = current_price + (risk_per_share * 3.0)  # 1:3 R:R

    # Quality Verdict
    if score >= 80:
        verdict = "🔥 HIGH PROBABILITY SWING SETUP (Prime Entry)"
    elif score >= 65:
        verdict = "✅ SOLID SWING SETUP (Execute with confirmation)"
    elif score >= 50:
        verdict = "👀 WATCHLIST (Wait for volume or candlestick trigger)"
    else:
        verdict = "🚫 NO TRADE / WEAK STRUCTURE"

    return {
        "current_price": current_price,
        "ema_20": round(curr_ema20, 2),
        "sma_50": round(curr_sma50, 2),
        "sma_200": round(curr_sma200, 2),
        "rsi_14": round(curr_rsi, 1),
        "atr_14": round(curr_atr, 2),
        "volume_surge_ratio": round(volume_surge_ratio, 2),
        "setup_type": setup_type,
        "score": score,
        "verdict": verdict,
        "reasons": reasons,
        "recommended_entry": round(current_price, 2),
        "stop_loss": round(stop_loss, 2),
        "target_1": round(target_1, 2),
        "target_2": round(target_2, 2),
        "risk_reward_ratio": "1:2.0 (Target 1) / 1:3.0 (Target 2)",
    }


def print_analysis_report(symbol: str, analysis: Dict[str, Any]):
    """Outputs a rich terminal report of the swing setup analysis."""
    print("=" * 65)
    print(f"       📈 SWING TRADING TECHNICAL REPORT: {symbol.upper()}")
    print("=" * 65)
    print(f" Current Price    : {analysis['current_price']:.2f}")
    print(f" Setup Type       : {analysis['setup_type']}")
    print(f" Setup Quality    : {analysis['score']} / 100  -->  {analysis['verdict']}")
    print("-" * 65)
    print(" 🛠️  KEY INDICATORS:")
    print(f" • 20 EMA         : {analysis['ema_20']:.2f}")
    print(f" • 50 SMA         : {analysis['sma_50']:.2f}")
    print(f" • 200 SMA        : {analysis['sma_200']:.2f}")
    print(f" • RSI(14)        : {analysis['rsi_14']:.1f}")
    print(f" • ATR(14)        : {analysis['atr_14']:.2f}")
    print(f" • Volume Surge   : {analysis['volume_surge_ratio']}x (vs 20-day avg)")
    print("-" * 65)
    print(" 🎯 RECOMMENDED EXECUTION PARAMETERS:")
    print(f" • Entry Price    : {analysis['recommended_entry']:.2f}")
    print(f" • Stop Loss      : {analysis['stop_loss']:.2f} (-{((analysis['recommended_entry'] - analysis['stop_loss'])/analysis['recommended_entry'])*100:.2f}%)")
    print(f" • Target 1 (1:2) : {analysis['target_1']:.2f} (+{((analysis['target_1'] - analysis['recommended_entry'])/analysis['recommended_entry'])*100:.2f}%)")
    print(f" • Target 2 (1:3) : {analysis['target_2']:.2f} (+{((analysis['target_2'] - analysis['recommended_entry'])/analysis['recommended_entry'])*100:.2f}%)")
    print("-" * 65)
    print(" 📋 TECHNICAL RATIONALE:")
    for r in analysis["reasons"]:
        print(f"   {r}")
    print("=" * 65)


def generate_synthetic_candles(base_price: float = 100.0, trend: str = "bullish", count: int = 60) -> List[Dict[str, float]]:
    """Generates synthetic OHLCV data for testing and offline analysis."""
    import random
    random.seed(42)
    candles = []
    price = base_price
    for i in range(count):
        drift = 0.003 if trend == "bullish" else -0.002
        change = random.gauss(drift, 0.015)
        open_p = price
        close_p = price * (1.0 + change)
        high_p = max(open_p, close_p) * (1.0 + abs(random.gauss(0, 0.005)))
        low_p = min(open_p, close_p) * (1.0 - abs(random.gauss(0, 0.005)))
        vol = 100000 * random.uniform(0.7, 1.8)
        if i == count - 1 and trend == "bullish":
            vol *= 1.6  # simulated volume breakout on last candle
        candles.append({
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": int(vol),
        })
        price = close_p
    return candles


def main():
    parser = argparse.ArgumentParser(description="Swing Trading Setup Analyzer")
    parser.add_argument("--symbol", type=str, default="DEMO_STOCK", help="Ticker symbol (e.g. RELIANCE, NVDA)")
    parser.add_argument("--file", type=str, default=None, help="Path to JSON file containing candle array")
    parser.add_argument("--demo", action="store_true", help="Run with demo synthetic market data")

    args = parser.parse_args()

    candles = None
    if args.file:
        try:
            with open(args.file, "r") as f:
                candles = json.load(f)
        except Exception as e:
            print(f"Error loading file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        candles = generate_synthetic_candles(base_price=500.0, trend="bullish", count=60)

    try:
        results = analyze_swing_setup(candles)
        print_analysis_report(args.symbol, results)
    except Exception as e:
        print(f"Analysis failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
