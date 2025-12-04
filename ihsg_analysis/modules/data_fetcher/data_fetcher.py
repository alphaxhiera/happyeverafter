import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

class IHSGDataFetcher:
    """Module for fetching IHSG stock data from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            ticker: Stock ticker symbol (e.g., 'BBCA.JK')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                print(f"No data found for {ticker}")
                return pd.DataFrame()
            
            # Rename columns to be more descriptive
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
            
            # Add additional columns
            data['Ticker'] = ticker
            data['Date'] = data.index
            data['Price_Change'] = data['Close'].pct_change()
            data['Price_Change_Pct'] = data['Price_Change'] * 100
            
            return data.reset_index(drop=True)
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def get_multiple_stocks(self, tickers: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks
        
        Args:
            tickers: List of ticker symbols
            period: Time period for data
        
        Returns:
            Dictionary with ticker as key and DataFrame as value
        """
        results = {}
        
        for ticker in tickers:
            print(f"Fetching data for {ticker}...")
            data = self.get_stock_data(ticker, period)
            if not data.empty:
                results[ticker] = data
            time.sleep(0.1)  # Rate limiting
        
        return results
    
    def get_company_info(self, ticker: str) -> Dict:
        """
        Get company information and fundamentals
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dictionary with company information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract relevant information
            company_info = {
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'debt_to_equity': info.get('debtToEquity', 0),
                'revenue': info.get('totalRevenue', 0),
                'net_income': info.get('netIncomeToCommon', 0),
                'book_value': info.get('bookValue', 0),
                'eps': info.get('trailingEps', 0),
                'beta': info.get('beta', 0),
                'description': info.get('longBusinessSummary', ''),
                'website': info.get('website', ''),
                'employees': info.get('fullTimeEmployees', 0)
            }
            
            return company_info
            
        except Exception as e:
            print(f"Error fetching company info for {ticker}: {str(e)}")
            return {}
    
    def get_financial_statements(self, ticker: str) -> Dict:
        """
        Get financial statements (Income Statement, Balance Sheet, Cash Flow)
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dictionary with financial statements
        """
        try:
            stock = yf.Ticker(ticker)
            
            financials = {
                'income_statement': stock.financials,
                'quarterly_income_statement': stock.quarterly_financials,
                'balance_sheet': stock.balance_sheet,
                'quarterly_balance_sheet': stock.quarterly_balance_sheet,
                'cash_flow': stock.cashflow,
                'quarterly_cash_flow': stock.quarterly_cashflow
            }
            
            return financials
            
        except Exception as e:
            print(f"Error fetching financial statements for {ticker}: {str(e)}")
            return {}
    
    def get_market_indices(self) -> Dict:
        """
        Get Indonesian market indices data
        
        Returns:
            Dictionary with market indices information
        """
        try:
            # IHSG Index
            ihsg = yf.Ticker('^JKSE')
            ihsg_data = ihsg.history(period="1mo")
            
            # Other regional indices for comparison
            indices = {
                'IHSG': {
                    'data': ihsg_data,
                    'current': ihsg_data['Close'].iloc[-1] if not ihsg_data.empty else 0,
                    'change': ihsg_data['Close'].pct_change().iloc[-1] * 100 if not ihsg_data.empty else 0
                }
            }
            
            return indices
            
        except Exception as e:
            print(f"Error fetching market indices: {str(e)}")
            return {}
    
    def calculate_market_sentiment(self, tickers: List[str]) -> Dict:
        """
        Calculate market sentiment based on stock performance
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            Dictionary with sentiment analysis
        """
        try:
            data = self.get_multiple_stocks(tickers, "5d")
            
            if not data:
                return {}
            
            sentiment_data = []
            for ticker, df in data.items():
                if not df.empty and len(df) > 1:
                    latest_change = df['Price_Change_Pct'].iloc[-1]
                    sentiment_data.append(latest_change)
            
            if not sentiment_data:
                return {}
            
            avg_change = sum(sentiment_data) / len(sentiment_data)
            positive_count = sum(1 for x in sentiment_data if x > 0)
            total_count = len(sentiment_data)
            
            sentiment = {
                'average_change': avg_change,
                'positive_ratio': positive_count / total_count,
                'sentiment': 'BULLISH' if avg_change > 1 else 'BEARISH' if avg_change < -1 else 'NEUTRAL',
                'total_stocks': total_count,
                'positive_stocks': positive_count,
                'negative_stocks': total_count - positive_count
            }
            
            return sentiment
            
        except Exception as e:
            print(f"Error calculating market sentiment: {str(e)}")
            return {}