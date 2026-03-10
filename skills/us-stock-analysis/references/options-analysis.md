# Options Flow & Positioning Analysis Reference

## Overview

Options market data provides unique insights into market sentiment, institutional positioning, and expected volatility. This reference guide covers how to interpret options data for stock analysis.

## Key Options Metrics

### 1. Put/Call Ratio (PCR)

**Definition:** Ratio of put volume to call volume (or open interest)

**Interpretation:**
| PCR Value | Sentiment | Interpretation |
|-----------|-----------|----------------|
| > 1.2 | Bearish | More puts than calls, fear dominant |
| 0.9 - 1.2 | Neutral | Balanced sentiment |
| 0.7 - 0.9 | Slightly Bullish | More call interest |
| < 0.7 | Bullish | Strong call buying |
| < 0.5 | Extremely Bullish | Potential contrarian signal (too crowded) |
| > 1.5 | Extremely Bearish | Potential contrarian signal (capitulation) |

**Contrarian Signal:** Extreme PCR readings often mark turning points
- Very high PCR (> 1.5): Market may be oversold, watch for bounce
- Very low PCR (< 0.5): Market may be overbought, watch for pullback

### 2. Open Interest (OI)

**Definition:** Total number of outstanding (unsettled) options contracts

**Key Insights:**
- **High OI strikes** act as magnets or barriers
- **OI changes** show where new money flows
- **Roll activity** (closing near-term, opening longer-term) shows conviction

**Interpretation:**
| Pattern | Interpretation |
|---------|----------------|
| Rising call OI at higher strikes | Bullish positioning, upside targets |
| Rising put OI at lower strikes | Hedging or bearish bets, support levels |
| Large OI concentration | Max pain level, potential pinning |
| OI decreasing into expiration | Positions being closed |

### 3. Options Volume

**Definition:** Number of contracts traded during the day

**Key Signals:**
- **Volume > Open Interest:** New positions being opened (fresh conviction)
- **Volume spike (> 2x average):** Unusual interest, possible informed trading
- **Sweeps:** Orders split across exchanges for fast execution (urgent trades)

**Volume Analysis:**
```
Volume/OI Ratio Interpretation:
- < 0.5: Low interest, existing positions holding
- 0.5 - 1.0: Normal trading activity
- 1.0 - 2.0: Elevated interest, new positions
- > 2.0: Unusual activity, investigate further
```

### 4. Implied Volatility (IV)

**Definition:** Market's expectation of annualized price movement (derived from options prices)

**Interpretation:**
| IV Level | Meaning | Strategy Implication |
|----------|---------|---------------------|
| Very High (> 80%) | Expecting large moves | Options expensive, consider selling premium |
| High (50-80%) | Elevated uncertainty | Earnings, events approaching |
| Normal (20-50%) | Typical volatility | Standard pricing |
| Low (< 20%) | Calm market | Options cheap, consider buying |

**IV Rank:** Current IV vs 52-week range
- IV Rank > 80%: IV in top 20% of yearly range (expensive)
- IV Rank < 20%: IV in bottom 20% of yearly range (cheap)

**IV Skew:** Compare IV across strikes
- Put skew (higher IV on puts): Fear of downside
- Call skew (higher IV on calls): FOMO or squeeze potential

### 5. Unusual Options Activity

**Definition:** Trades that stand out from normal patterns

**Red Flags for Unusual Activity:**
- **Block trades:** 1,000+ contracts in single trade
- **Sweeps:** Multiple executions across exchanges within seconds
- **Premium size:** $100k+ in premium spent
- **OTM strikes:** Far from current price (speculative bets)
- **Near-term expiration:** High conviction on timing

**Bullish Unusual Activity:**
- Large call purchases at OTM strikes
- Call sweeps at ask price (aggressive buying)
- Bull call spreads (buy lower strike call, sell higher strike)
- Call volume significantly exceeding put volume

**Bearish Unusual Activity:**
- Large put purchases for speculation (not hedging)
- Put sweeps at ask price
- Bear put spreads
- Put volume significantly exceeding call volume

**Hedging vs Speculation:**
- **Hedging:** Puts bought on existing stock position (protective)
- **Speculation:** Puts bought without stock ownership (betting on decline)
- **Collars:** Buy put + sell call (locking in range, institutional protection)

## Options Greeks (Quick Reference)

| Greek | Measures | Relevance |
|-------|----------|-----------|
| **Delta** | Price change per $1 stock move | Directional exposure |
| **Gamma** | Rate of delta change | Dealer hedging, acceleration |
| **Theta** | Time decay per day | Options lose value over time |
| **Vega** | Sensitivity to IV change | Volatility exposure |
| **Rho** | Interest rate sensitivity | Usually minor impact |

## Key Options Levels

### Max Pain Level
- **Definition:** Strike price where most options expire worthless
- **Use:** Often acts as magnet into expiration (Friday)
- **Theory:** Market makers hedge to minimize payouts

### Gamma Exposure (GEX)
- **Positive Gamma:** Dealers sell into strength, buy into weakness (stabilizing)
- **Negative Gamma:** Dealers buy into strength, sell into weakness (amplifying)
- **Zero Gamma Level:** Transition point between positive/negative gamma regimes

### Call Wall / Put Wall
- **Call Wall:** Strike with largest call OI (resistance)
- **Put Wall:** Strike with largest put OI (support)
- **Use:** Key levels for price action

## Options Strategies by Outlook

| Outlook | Strategy | Risk/Reward |
|---------|----------|-------------|
| Bullish | Long calls, call spreads | Limited risk, leveraged upside |
| Very Bullish | OTM call sweeps | High risk, high reward |
| Mildly Bullish | Covered calls | Income generation |
| Neutral | Iron condors, strangles | Profit from time decay |
| Mildly Bearish | Protective puts, put spreads | Downside protection |
| Very Bearish | Long puts, put sweeps | High conviction decline |
| Volatile | Straddles, strangles | Betting on big move |

## Data Sources for Options Analysis

- **CBOE (Chicago Board Options Exchange):** Official options data, VIX
- **Barchart:** Unusual options activity screener
- **Options Flow:** Real-time flow data
- **Cheddar Flow:** Institutional flow tracking
- **Unusual Whales:** Retail + institutional flow
- **Yahoo Finance:** Basic options chains, OI, volume
- **CBOE Put/Call Ratios:** Equity, index, total PCR

## Example Analysis Output

```
Options Flow Analysis for AAPL (Current: $175.50)

SENTIMENT INDICATORS:
├─ Put/Call Ratio: 0.78 (Slightly Bullish)
├─ Total Volume: 1.2M (2.1x average)
└─ IV Rank: 45% (Normal volatility)

KEY LEVELS:
├─ Max Pain: $175 (Friday expiration)
├─ Call Wall: $180 (45k OI) - Resistance
└─ Put Wall: $170 (38k OI) - Support

UNUSUAL ACTIVITY:
├─ 5,000x $175 Calls (weekly) bought at ask - $425k premium
├─ 3,200x $180 Calls (monthly) sweep - Bullish bet on earnings
└─ 2,000x $165 Puts (quarterly) - Institutional hedge

POSITIONING:
├─ Weekly: Heavy $175-$180 call concentration
├─ Monthly: Bullish skew, more call OI above current price
└─ LEAPS: Steady accumulation at $200+ strikes

INTERPRETATION:
Options market pricing in bullish move toward $180.
Large call sweeps suggest informed buying.
Put protection at $165-$170 limits downside risk.
Max pain at $175 may pin price into Friday expiration.
```

## Integration with Stock Analysis

**Combine options insights with:**

1. **Fundamental Analysis:**
   - High IV before earnings → Expect volatility
   - Unusual call buying + strong fundamentals → Confirmed bullish thesis

2. **Technical Analysis:**
   - Call wall at resistance → Confirms technical level
   - Put floor at support → Downside protection level
   - Gamma exposure → Potential for accelerated moves

3. **Catalyst Analysis:**
   - Earnings → Elevated IV, straddle pricing
   - FDA decisions, product launches → Binary event positioning
   - M&A rumors → OTM call spikes

**Red Flags:**
- Put buying without stock ownership (bearish speculation)
- Rising put/call ratio during uptrend (divergence)
- Unusual put sweeps at support (breaking support expected)
