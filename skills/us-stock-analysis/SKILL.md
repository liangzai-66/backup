---
name: us-stock-analysis
description: Comprehensive US stock analysis including fundamental analysis (financial metrics, business quality, valuation), technical analysis (indicators, chart patterns, support/resistance), options flow & positioning analysis (open interest, put/call ratios, unusual activity, implied volatility), stock comparisons, and investment report generation. Use when user requests analysis of US stock tickers (e.g., "analyze AAPL", "compare TSLA vs NVDA", "give me a report on Microsoft"), evaluation of financial metrics, technical chart analysis, options activity analysis, or investment recommendations for American stocks.
---

# US Stock Analysis

## Overview

Perform comprehensive analysis of US stocks covering fundamental analysis (financials, business quality, valuation), technical analysis (indicators, trends, patterns), peer comparisons, and generate detailed investment reports. Fetch real-time market data via web search tools and apply structured analytical frameworks.

## Data Sources

Always use web search tools to gather current market data:

**Primary Data to Fetch:**
1. **Current stock price and trading data** (price, volume, 52-week range)
2. **Financial statements** (income statement, balance sheet, cash flow)
3. **Key metrics** (P/E, EPS, revenue, margins, debt ratios)
4. **Analyst ratings and price targets**
5. **Recent news and developments**
6. **Peer/competitor data** (for comparisons)
7. **Technical data** (moving averages, RSI, MACD when available)
8. **Options data** (open interest, volume, put/call ratio, implied volatility, unusual options activity)

**Search Strategy:**
- Use ticker symbol + specific data needed (e.g., "AAPL financial metrics 2024")
- For comprehensive data: Search for earnings reports, investor presentations, or SEC filings
- For technical data: Search for "AAPL technical analysis" or use financial data sites
- For options data: Search for "AAPL options flow", "AAPL put call ratio", "AAPL open interest", "AAPL unusual options activity"
- Always verify data recency (prefer data from last quarter)

**Quality Sources:**
- Yahoo Finance, Google Finance, MarketWatch, Seeking Alpha, Bloomberg, CNBC
- Company investor relations pages
- SEC filings (10-K, 10-Q) for detailed financials
- TradingView, StockCharts for technical data
- **Options-specific sources:** CBOE, Barchart, Options Flow, Cheddar Flow, Unusual Whales, CBOE Put/Call Ratios

## Analysis Types

This skill supports **five** types of analysis. Determine which type(s) the user needs:

1. **Basic Stock Info** - Quick overview with key metrics
2. **Fundamental Analysis** - Deep dive into business, financials, valuation
3. **Technical Analysis** - Chart patterns, indicators, trend analysis
4. **Options Flow & Positioning Analysis** - Options activity, open interest, put/call ratios, institutional positioning
5. **Comprehensive Report** - Complete analysis combining all approaches (including options when relevant)

## Analysis Workflows

### 1. Basic Stock Information

**When to Use:** User asks for quick overview or basic info

**Steps:**
1. Search for current stock data (price, volume, market cap)
2. Gather key metrics (P/E, EPS, revenue growth, margins)
3. Get 52-week range and year-to-date performance
4. Find recent news or major developments
5. Present in concise summary format

**Output Format:**
- Company description (1-2 sentences)
- Current price and trading metrics
- Key valuation metrics (table)
- Recent performance
- Notable recent news (if any)

### 2. Fundamental Analysis

**When to Use:** User wants financial analysis, valuation assessment, or business evaluation

**Steps:**
1. **Gather comprehensive financial data:**
   - Revenue, earnings, cash flow (3-5 year trends)
   - Balance sheet metrics (debt, cash, working capital)
   - Profitability metrics (margins, ROE, ROIC)
   
2. **Read references/fundamental-analysis.md** for analytical framework

3. **Read references/financial-metrics.md** for metric definitions and calculations

4. **Analyze business quality:**
   - Competitive advantages
   - Management track record
   - Industry position
   
5. **Perform valuation analysis:**
   - Calculate key ratios (P/E, PEG, P/B, EV/EBITDA)
   - Compare to historical averages
   - Compare to peer group
   - Estimate fair value range
   
6. **Identify risks:**
   - Company-specific risks
   - Market/macro risks
   - Red flags from financial data

7. **Generate output** following references/report-template.md structure

**Critical Analyses:**
- Profitability trends (improving/declining margins)
- Cash flow quality (FCF vs earnings)
- Balance sheet strength (debt levels, liquidity)
- Growth sustainability
- Valuation vs peers and historical average

### 3. Technical Analysis

**When to Use:** User asks for technical analysis, chart patterns, or trading signals

**Steps:**
1. **Gather technical data:**
   - Current price and recent price action
   - Volume trends
   - Moving averages (20-day, 50-day, 200-day)
   - Technical indicators (RSI, MACD, Bollinger Bands)
   
2. **Read references/technical-analysis.md** for indicator definitions and patterns

3. **Identify trend:**
   - Uptrend, downtrend, or sideways
   - Strength of trend
   
4. **Locate support and resistance levels:**
   - Recent highs and lows
   - Moving average levels
   - Round numbers
   
5. **Analyze indicators:**
   - RSI: Overbought (>70) or oversold (<30)
   - MACD: Crossovers and divergences
   - Volume: Confirmation or divergence
   - Bollinger Bands: Squeeze or expansion
   
6. **Identify chart patterns:**
   - Reversal patterns (head and shoulders, double top/bottom)
   - Continuation patterns (flags, triangles)
   
7. **Generate technical outlook:**
   - Current trend assessment
   - Key levels to watch
   - Risk/reward analysis
   - Short and medium-term outlook

**Interpretation Guidelines:**
- Confirm signals with multiple indicators
- Consider volume for validation
- Note divergences between price and indicators
- Always identify risk levels (stop-loss)

### 4. Options Flow & Positioning Analysis

**When to Use:** User asks about options activity, institutional positioning, market sentiment, or wants to understand smart money flows. Also use in comprehensive reports when options data provides meaningful insight into expected volatility or directional bias.

**Steps:**
1. **Gather options data:**
   - **Put/Call Ratio** (overall and by expiration)
     - PCR > 1.0: Bearish sentiment (more puts being traded)
     - PCR < 0.7: Bullish sentiment (more calls being traded)
     - Extreme readings can signal contrarian opportunities
   - **Open Interest (OI)** by strike and expiration
     - High OI strikes act as magnets or resistance levels
     - OI changes show where new money is flowing
   - **Options Volume** vs Open Interest
     - Volume > OI indicates new positions being opened
     - Unusual volume spikes may signal informed trading
   - **Implied Volatility (IV)** and IV Rank
     - High IV: Expected large price movement (earnings, events)
     - IV Rank: Current IV vs 52-week range (high = expensive options)
   - **Unusual Options Activity**
     - Large block trades (1000+ contracts)
     - Sweeps: Orders split across exchanges for fast execution
     - Note strike, expiration, premium, and whether bought/sold

2. **Analyze positioning by expiration:**
   - **Weekly options** (0-7 days): Short-term trader sentiment, gamma exposure
   - **Monthly options** (30-45 days): Institutional positioning, earnings plays
   - **LEAPS** (6+ months): Long-term conviction bets

3. **Identify key options levels:**
   - **Max Pain Level**: Strike where most options expire worthless
   - **Gamma Exposure (GEX)**: Dealer hedging levels that can amplify moves
   - **Call Walls**: Large call OI acting as resistance
   - **Put Floors**: Large put OI acting as support

4. **Interpret smart money signals:**
   - **Bullish signals:**
     - Heavy call buying at OTM strikes
     - Call sweeps at ask price
     - Decreasing put/call ratio
     - Rising OI at higher strikes
   - **Bearish signals:**
     - Heavy put buying for protection or speculation
     - Put sweeps at ask price
     - Increasing put/call ratio
     - Rising OI at lower strikes
   - **Hedging activity:**
     - Collars (buy put + sell call): Institutions protecting gains
     - Put spreads: Controlled downside protection

5. **Synthesize options insights:**
   - What is the market expecting (direction and magnitude)?
   - Where are the key pain points and levels?
   - Is there unusual activity suggesting informed trading?
   - How does options positioning complement technical/fundamental analysis?

**Output Format:**
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Put/Call Ratio | 0.85 | Slightly bullish sentiment |
| Total Options Volume | 1.2M | 2x average, elevated interest |
| Max Pain | $175 | Price where most options expire worthless |
| Highest Call OI | $180 (45k) | Resistance level |
| Highest Put OI | $170 (38k) | Support level |
| Unusual Activity | 5k $175 calls bought | Bullish bet on upside |

**Key Options Terms:**
- **Open Interest (OI)**: Total outstanding contracts
- **Volume**: Contracts traded today
- **Implied Volatility (IV)**: Expected annualized price movement
- **Delta**: Price sensitivity to $1 stock move
- **Gamma**: Rate of change of delta (dealer hedging impact)
- **Theta**: Time decay (options lose value as expiration approaches)

### 5. Comprehensive Investment Report

**When to Use:** User asks for detailed report, investment recommendation, or complete analysis

**Steps:**
1. **Perform data gathering** (as in Basic Info)

2. **Execute fundamental analysis** (follow workflow above)

3. **Execute technical analysis** (follow workflow above)

4. **Execute options analysis** (when options data is relevant and available)
   - Especially important for: earnings plays, high-volatility stocks, large-cap names with active options markets

5. **Read references/report-template.md** for complete report structure

6. **Synthesize findings:**
   - Integrate fundamental, technical, and options insights
   - Develop bull and bear cases
   - Assess risk/reward
   - Consider options-implied expectations vs your analysis
   
7. **Generate recommendation:**
   - Buy/Hold/Sell rating
   - Target price with timeframe
   - Conviction level
   - Entry strategy
   - Options strategy suggestions (if applicable): covered calls, protective puts, spreads
   
8. **Create formatted report** following template structure

**Report Must Include:**
- Executive summary with recommendation
- Company overview
- Investment thesis (bull and bear cases)
- Fundamental analysis section
- Technical analysis section
- **Options flow & positioning** (when relevant)
- Valuation analysis
- Risk assessment
- Catalysts and timeline
- Conclusion

## Stock Comparison Analysis

**When to Use:** User asks to compare two or more stocks (e.g., "compare AAPL vs MSFT")

**Steps:**
1. **Gather data for all stocks:**
   - Follow data gathering steps for each ticker
   - Ensure comparable timeframes
   
2. **Read references/fundamental-analysis.md** and references/financial-metrics.md

3. **Create side-by-side comparison:**
   - Business models comparison
   - Financial metrics table (all key ratios)
   - Valuation metrics table
   - Growth rates comparison
   - Profitability comparison
   - Balance sheet strength
   
4. **Identify relative strengths:**
   - Where each company excels
   - Quantified advantages
   
5. **Technical comparison:**
   - Relative strength
   - Momentum comparison
   - Which is in better technical position
   
6. **Generate recommendation:**
   - Which stock is more attractive and why
   - Consider both fundamental and technical factors
   - Portfolio allocation suggestion
   - Risk-adjusted return assessment

**Output Format:** Follow "Comparison Report Structure" in references/report-template.md

## Output Guidelines

**General Principles:**
- Use tables for financial data and comparisons (easy to scan)
- Bold key metrics and findings
- Include data sources and dates
- Quantify whenever possible
- Present both bull and bear perspectives
- Be clear about assumptions and uncertainties

**Formatting:**
- **Headers** for clear section separation
- **Tables** for metrics, comparisons, historical data
- **Bullet points** for lists, factors, risks
- **Bold text** for key findings, important metrics
- **Percentages** for growth rates, returns, margins
- **Currency** formatted consistently ($B for billions, $M for millions)

**Tone:**
- Objective and balanced
- Acknowledge uncertainty
- Support claims with data
- Avoid hyperbole
- Present risks clearly

## Reference Files

Load these references as needed during analysis:

**references/technical-analysis.md**
- When: Performing technical analysis or interpreting indicators
- Contains: Indicator definitions, chart patterns, support/resistance concepts, analysis workflow

**references/fundamental-analysis.md**
- When: Performing fundamental analysis or business evaluation
- Contains: Business quality assessment, financial health analysis, valuation frameworks, risk assessment, red flags

**references/financial-metrics.md**
- When: Need definitions or calculation methods for financial ratios
- Contains: All key metrics with formulas (profitability, valuation, growth, liquidity, leverage, efficiency, cash flow)

**references/options-analysis.md**
- When: Performing options flow & positioning analysis
- Contains: Options metrics (PCR, OI, IV, volume), unusual activity interpretation, key levels (max pain, gamma exposure), Greeks reference, integration with stock analysis

**references/report-template.md**
- When: Creating comprehensive report or comparison
- Contains: Complete report structure, formatting guidelines, section templates, comparison format

## Example Queries

**Basic Info:**
- "What's the current price of AAPL?"
- "Give me key metrics for Tesla"
- "Quick overview of Microsoft stock"

**Fundamental:**
- "Analyze NVDA's financials"
- "Is Amazon overvalued?"
- "Evaluate Apple's business quality"
- "What's Google's debt situation?"

**Technical:**
- "Technical analysis of TSLA"
- "Is Netflix oversold?"
- "Show me support levels for AAPL"
- "What's the trend for AMD?"

**Comprehensive:**
- "Complete analysis of Microsoft"
- "Give me a full report on AAPL"
- "Should I invest in Tesla? Give me detailed analysis"

**Comparison:**
- "Compare AAPL vs MSFT"
- "Tesla vs Nvidia - which is better?"
- "Analyze Meta vs Google"

**Options Flow & Positioning:**
- "Show me AAPL options flow today"
- "What's the put/call ratio for TSLA?"
- "Any unusual options activity on NVDA?"
- "Where is the max pain level for SPY this week?"
- "What are institutions doing with AMD options?"
- "Show me the options open interest for MSFT earnings"
- "Is there heavy call buying on AAPL?"
- "What's the implied volatility telling us about GOOGL?"
