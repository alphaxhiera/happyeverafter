# IHSG Technical & Fundamental Analysis

A comprehensive web application for technical and fundamental analysis of Indonesia Stock Market (IHSG) stocks with actionable investment recommendations.

## Features

### 🔍 Technical Analysis
- **Price Charts**: Interactive candlestick charts with volume
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, Stochastic, and more
- **Trend Analysis**: Automatic trend detection and strength measurement
- **Support & Resistance**: Dynamic identification of key price levels
- **Trading Signals**: Buy/Sell/Hold signals with confidence levels

### 📊 Fundamental Analysis
- **Valuation Ratios**: P/E, P/B, and other key valuation metrics
- **Profitability Analysis**: ROE, profit margins, and earnings quality
- **Financial Health**: Debt analysis, solvency ratios, and risk assessment
- **Industry Comparison**: Benchmarking against industry standards
- **Intrinsic Value**: Multiple valuation methods (Graham, DCF, etc.)

### 🎯 Investment Recommendations
- **Comprehensive Scoring**: Combined technical and fundamental analysis
- **Risk-Adjusted Returns**: Position sizing based on risk profile
- **Actionable Insights**: Specific buy/sell/hold recommendations
- **Price Targets**: Stop loss and take profit levels
- **Portfolio Management**: Multi-stock portfolio optimization

### 📈 Market Overview
- **Market Sentiment**: Overall market mood and direction
- **Sector Analysis**: Industry-wide performance metrics
- **Stock Comparison**: Side-by-side analysis of multiple stocks
- **Market Indices**: IHSG and related market indices

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
ihsg_analysis/
├── modules/
│   ├── data_fetcher/          # Data fetching from Yahoo Finance
│   ├── technical_indicators/  # Technical analysis calculations
│   ├── fundamental_analysis/  # Fundamental analysis calculations
│   ├── recommendation_engine/ # Investment recommendation logic
│   └── ui_components/         # Streamlit UI components
├── config.py                  # Configuration settings
└── app.py                     # Main Streamlit application
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ihsg-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

### Single Stock Analysis
1. Select a stock from the dropdown (BBCA.JK, BBRI.JK, etc.)
2. Choose the time period for analysis
3. Select your risk profile (conservative, moderate, aggressive)
4. Click "Analyze" to get comprehensive analysis

### Market Overview
1. Go to the "Market Overview" tab
2. Click "Analyze Market" to see:
   - Market sentiment indicators
   - Stock comparison table
   - Performance visualization

### Portfolio Analysis
1. Go to the "Portfolio Analysis" tab
2. Enter your total capital
3. Select portfolio risk profile
4. Click "Generate Portfolio" for optimized recommendations

## Technical Indicators

### Trend Indicators
- **Moving Averages** (SMA, EMA)
- **MACD** (Moving Average Convergence Divergence)
- **Ichimoku Cloud**

### Momentum Indicators
- **RSI** (Relative Strength Index)
- **Stochastic Oscillator**
- **Williams %R**
- **CCI** (Commodity Channel Index)

### Volatility Indicators
- **Bollinger Bands**
- **ATR** (Average True Range)

### Volume Indicators
- **On-Balance Volume (OBV)**
- **Money Flow Index (MFI)**
- **VWAP** (Volume Weighted Average Price)

## Fundamental Metrics

### Valuation Ratios
- **P/E Ratio** (Price-to-Earnings)
- **P/B Ratio** (Price-to-Book)
- **P/S Ratio** (Price-to-Sales)
- **EV/EBITDA**

### Profitability Metrics
- **ROE** (Return on Equity)
- **ROA** (Return on Assets)
- **Net Profit Margin**
- **Gross Profit Margin**

### Financial Health
- **Debt-to-Equity Ratio**
- **Current Ratio**
- **Quick Ratio**
- **Interest Coverage Ratio**

## Risk Management

### Position Sizing
- **Conservative**: Max 5% per stock, 8% stop loss, 15% take profit
- **Moderate**: Max 8% per stock, 10% stop loss, 20% take profit
- **Aggressive**: Max 12% per stock, 15% stop loss, 30% take profit

### Risk Metrics
- **Beta** (Systematic risk)
- **Sharpe Ratio** (Risk-adjusted returns)
- **Maximum Drawdown**
- **Value at Risk (VaR)**

## Configuration

The application can be configured through `config.py`:

```python
# Stock tickers to analyze
IHSG_TICKERS = ['BBCA.JK', 'BBRI.JK', 'BBNI.JK', ...]

# Technical analysis parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26

# Fundamental analysis thresholds
PE_GOOD_THRESHOLD = 15
PBV_GOOD_THRESHOLD = 2
ROE_GOOD_THRESHOLD = 15
```

## Data Sources

- **Price Data**: Yahoo Finance API
- **Company Information**: Yahoo Finance
- **Financial Statements**: Yahoo Finance
- **Market Indices**: Yahoo Finance

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

---

**Note**: This application uses real market data and should be used for educational purposes only. Past performance does not guarantee future results.