import pandas as pd
import numpy as np
import talib
from typing import Dict, Tuple, List

class TechnicalIndicators:
    """Module for calculating various technical analysis indicators"""
    
    @staticmethod
    def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            prices: Price series
            period: RSI period (default: 14)
        
        Returns:
            RSI values
        """
        rsi_values = talib.RSI(prices.values, timeperiod=period)
        return pd.Series(rsi_values, index=prices.index)
    
    @staticmethod
    def macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            prices: Price series
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        
        Returns:
            Dictionary with MACD, Signal, and Histogram
        """
        macd_line, signal_line, histogram = talib.MACD(prices.values, fastperiod=fast, slowperiod=slow, signalperiod=signal)
        
        return {
            'MACD': pd.Series(macd_line, index=prices.index),
            'Signal': pd.Series(signal_line, index=prices.index),
            'Histogram': pd.Series(histogram, index=prices.index)
        }
    
    @staticmethod
    def bollinger_bands(prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            prices: Price series
            period: Period for moving average
            std_dev: Standard deviation multiplier
        
        Returns:
            Dictionary with Upper, Middle, and Lower bands
        """
        upper, middle, lower = talib.BBANDS(prices.values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
        
        return {
            'Upper': pd.Series(upper, index=prices.index),
            'Middle': pd.Series(middle, index=prices.index),
            'Lower': pd.Series(lower, index=prices.index)
        }
    
    @staticmethod
    def moving_averages(prices: pd.Series, short_period: int = 20, long_period: int = 50) -> Dict[str, pd.Series]:
        """
        Calculate Simple Moving Averages
        
        Args:
            prices: Price series
            short_period: Short MA period
            long_period: Long MA period
        
        Returns:
            Dictionary with short and long MAs
        """
        ma_short = talib.SMA(prices.values, timeperiod=short_period)
        ma_long = talib.SMA(prices.values, timeperiod=long_period)
        
        return {
            'MA_Short': pd.Series(ma_short, index=prices.index),
            'MA_Long': pd.Series(ma_long, index=prices.index)
        }
    
    @staticmethod
    def exponential_moving_averages(prices: pd.Series, short_period: int = 12, long_period: int = 26) -> Dict[str, pd.Series]:
        """
        Calculate Exponential Moving Averages
        
        Args:
            prices: Price series
            short_period: Short EMA period
            long_period: Long EMA period
        
        Returns:
            Dictionary with short and long EMAs
        """
        ema_short = talib.EMA(prices.values, timeperiod=short_period)
        ema_long = talib.EMA(prices.values, timeperiod=long_period)
        
        return {
            'EMA_Short': pd.Series(ema_short, index=prices.index),
            'EMA_Long': pd.Series(ema_long, index=prices.index)
        }
    
    @staticmethod
    def stochastic_oscillator(high: pd.Series, low: pd.Series, close: pd.Series, 
                           k_period: int = 14, d_period: int = 3) -> Dict[str, pd.Series]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            k_period: %K period
            d_period: %D period
        
        Returns:
            Dictionary with %K and %D values
        """
        slowk, slowd = talib.STOCH(high.values, low.values, close.values, 
                                  fastk_period=k_period, slowk_period=d_period, slowd_period=d_period)
        
        return {
            'Stoch_K': pd.Series(slowk, index=close.index),
            'Stoch_D': pd.Series(slowd, index=close.index)
        }
    
    @staticmethod
    def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Williams %R
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Calculation period
        
        Returns:
            Williams %R values
        """
        willr_values = talib.WILLR(high.values, low.values, close.values, timeperiod=period)
        return pd.Series(willr_values, index=close.index)
    
    @staticmethod
    def commodity_channel_index(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20) -> pd.Series:
        """
        Calculate Commodity Channel Index (CCI)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Calculation period
        
        Returns:
            CCI values
        """
        cci_values = talib.CCI(high.values, low.values, close.values, timeperiod=period)
        return pd.Series(cci_values, index=close.index)
    
    @staticmethod
    def average_true_range(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Calculation period
        
        Returns:
            ATR values
        """
        atr_values = talib.ATR(high.values, low.values, close.values, timeperiod=period)
        return pd.Series(atr_values, index=close.index)
    
    @staticmethod
    def money_flow_index(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Money Flow Index (MFI)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            volume: Volume data
            period: Calculation period
        
        Returns:
            MFI values
        """
        mfi_values = talib.MFI(high.values, low.values, close.values, volume.values, timeperiod=period)
        return pd.Series(mfi_values, index=close.index)
    
    @staticmethod
    def on_balance_volume(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        Calculate On Balance Volume (OBV)
        
        Args:
            close: Close prices
            volume: Volume data
        
        Returns:
            OBV values
        """
        obv_values = talib.OBV(close.values, volume.values)
        return pd.Series(obv_values, index=close.index)
    
    @staticmethod
    def volume_weighted_average_price(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        Calculate Volume Weighted Average Price (VWAP)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            volume: Volume data
        
        Returns:
            VWAP values
        """
        typical_price = (high + low + close) / 3
        vwap = (typical_price * volume).cumsum() / volume.cumsum()
        return vwap
    
    @staticmethod
    def fibonacci_retracements(high_price: float, low_price: float) -> Dict[str, float]:
        """
        Calculate Fibonacci Retracement Levels
        
        Args:
            high_price: Highest price
            low_price: Lowest price
        
        Returns:
            Dictionary with Fibonacci levels
        """
        diff = high_price - low_price
        
        levels = {
            '0%': high_price,
            '23.6%': high_price - (0.236 * diff),
            '38.2%': high_price - (0.382 * diff),
            '50%': high_price - (0.5 * diff),
            '61.8%': high_price - (0.618 * diff),
            '78.6%': high_price - (0.786 * diff),
            '100%': low_price
        }
        
        return levels
    
    @staticmethod
    def pivot_points(high: float, low: float, close: float) -> Dict[str, float]:
        """
        Calculate Pivot Points
        
        Args:
            high: Previous day high
            low: Previous day low
            close: Previous day close
        
        Returns:
            Dictionary with pivot points
        """
        pivot = (high + low + close) / 3
        
        levels = {
            'Pivot': pivot,
            'R1': (2 * pivot) - low,
            'R2': pivot + (high - low),
            'R3': high + 2 * (pivot - low),
            'S1': (2 * pivot) - high,
            'S2': pivot - (high - low),
            'S3': low - 2 * (high - pivot)
        }
        
        return levels
    
    @staticmethod
    def ichimoku_cloud(high: pd.Series, low: pd.Series, close: pd.Series) -> Dict[str, pd.Series]:
        """
        Calculate Ichimoku Cloud components
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
        
        Returns:
            Dictionary with Ichimoku components
        """
        # Tenkan-sen (Conversion Line): 9-period high+low average
        tenkan_high = high.rolling(window=9).max()
        tenkan_low = low.rolling(window=9).min()
        tenkan_sen = (tenkan_high + tenkan_low) / 2
        
        # Kijun-sen (Base Line): 26-period high+low average
        kijun_high = high.rolling(window=26).max()
        kijun_low = low.rolling(window=26).min()
        kijun_sen = (kijun_high + kijun_low) / 2
        
        # Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, shifted 26 periods ahead
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
        
        # Senkou Span B (Leading Span B): 52-period high+low average, shifted 26 periods ahead
        senkou_high = high.rolling(window=52).max()
        senkou_low = low.rolling(window=52).min()
        senkou_span_b = ((senkou_high + senkou_low) / 2).shift(26)
        
        # Chikou Span (Lagging Span): Close price, shifted 26 periods behind
        chikou_span = close.shift(-26)
        
        return {
            'Tenkan_sen': tenkan_sen,
            'Kijun_sen': kijun_sen,
            'Senkou_Span_A': senkou_span_a,
            'Senkou_Span_B': senkou_span_b,
            'Chikou_Span': chikou_span
        }