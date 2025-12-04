import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

class Config:
    # IHSG Stock Data Configuration
    IHSG_TICKERS = [
        'BBCA.JK', 'BBRI.JK', 'BBNI.JK', 'BMRI.JK', 'TLKM.JK',
        'UNVR.JK', 'ASII.JK', 'INDF.JK', 'KLBF.JK', 'HMSP.JK'
    ]
    
    # API Configuration
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    
    # Technical Analysis Parameters
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    MA_SHORT = 20
    MA_LONG = 50
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2
    
    # Fundamental Analysis Thresholds
    PE_GOOD_THRESHOLD = 15
    PBV_GOOD_THRESHOLD = 2
    ROE_GOOD_THRESHOLD = 15
    DEBT_TO_EQUITY_GOOD_THRESHOLD = 1
    
    # Risk Management
    TAKE_PROFIT_PERCENTAGE = 0.20  # 20%
    STOP_LOSS_PERCENTAGE = 0.10    # 10%
    
    # Data Source Configuration
    DATA_SOURCE = 'yahoo_finance'
    CACHE_DURATION = 3600  # 1 hour in seconds