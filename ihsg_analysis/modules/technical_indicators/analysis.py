import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from .indicators import TechnicalIndicators

class TechnicalAnalysis:
    """Module for performing comprehensive technical analysis"""
    
    def __init__(self):
        self.indicators = TechnicalIndicators()
    
    def analyze_trend(self, df: pd.DataFrame) -> Dict:
        """
        Analyze overall trend using multiple indicators
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            Dictionary with trend analysis
        """
        if df.empty or len(df) < 50:
            return {'trend': 'UNKNOWN', 'strength': 0, 'signals': []}
        
        close = df['Close']
        signals = []
        
        # Moving Average Trend
        ma_short = self.indicators.moving_averages(close, 20, 50)
        if not ma_short['MA_Short'].isna().iloc[-1] and not ma_short['MA_Long'].isna().iloc[-1]:
            if ma_short['MA_Short'].iloc[-1] > ma_short['MA_Long'].iloc[-1]:
                signals.append('MA_BULLISH')
            else:
                signals.append('MA_BEARISH')
        
        # MACD Trend
        macd_data = self.indicators.macd(close)
        if not macd_data['MACD'].isna().iloc[-1] and not macd_data['Signal'].isna().iloc[-1]:
            if macd_data['MACD'].iloc[-1] > macd_data['Signal'].iloc[-1]:
                signals.append('MACD_BULLISH')
            else:
                signals.append('MACD_BEARISH')
        
        # Price Action Trend
        price_change_20d = (close.iloc[-1] - close.iloc[-20]) / close.iloc[-20] * 100
        if price_change_20d > 5:
            signals.append('PRICE_UPTREND')
        elif price_change_20d < -5:
            signals.append('PRICE_DOWNTREND')
        
        # Determine overall trend
        bullish_signals = sum(1 for s in signals if 'BULLISH' in s or 'UPTREND' in s)
        bearish_signals = sum(1 for s in signals if 'BEARISH' in s or 'DOWNTREND' in s)
        
        if bullish_signals > bearish_signals:
            trend = 'BULLISH'
            strength = bullish_signals / len(signals) * 100
        elif bearish_signals > bullish_signals:
            trend = 'BEARISH'
            strength = bearish_signals / len(signals) * 100
        else:
            trend = 'NEUTRAL'
            strength = 50
        
        return {
            'trend': trend,
            'strength': round(strength, 2),
            'signals': signals,
            'price_change_20d': round(price_change_20d, 2)
        }
    
    def identify_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Dict:
        """
        Identify support and resistance levels
        
        Args:
            df: DataFrame with OHLCV data
            window: Lookback window for S/R identification
        
        Returns:
            Dictionary with support and resistance levels
        """
        if df.empty or len(df) < window:
            return {'support': [], 'resistance': []}
        
        highs = df['High'].rolling(window=window, center=True).max()
        lows = df['Low'].rolling(window=window, center=True).min()
        
        # Find resistance levels (local highs)
        resistance_levels = []
        for i in range(window, len(df) - window):
            if df['High'].iloc[i] == highs.iloc[i]:
                resistance_levels.append(df['High'].iloc[i])
        
        # Find support levels (local lows)
        support_levels = []
        for i in range(window, len(df) - window):
            if df['Low'].iloc[i] == lows.iloc[i]:
                support_levels.append(df['Low'].iloc[i])
        
        # Keep only significant levels (remove duplicates and close levels)
        resistance_levels = sorted(list(set(resistance_levels)), reverse=True)[:5]
        support_levels = sorted(list(set(support_levels)))[:5]
        
        current_price = df['Close'].iloc[-1]
        
        return {
            'resistance': resistance_levels,
            'support': support_levels,
            'current_price': current_price,
            'nearest_resistance': min([r for r in resistance_levels if r > current_price], default=None),
            'nearest_support': max([s for s in support_levels if s < current_price], default=None)
        }
    
    def generate_signals(self, df: pd.DataFrame) -> Dict:
        """
        Generate buy/sell signals based on multiple indicators
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            Dictionary with trading signals
        """
        if df.empty or len(df) < 50:
            return {'signal': 'HOLD', 'confidence': 0, 'reasons': []}
        
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        signals = []
        buy_signals = 0
        sell_signals = 0
        
        # RSI Signal
        rsi = self.indicators.rsi(close)
        if not rsi.isna().iloc[-1]:
            if rsi.iloc[-1] < 30:
                signals.append('RSI_OVERSOLD')
                buy_signals += 1
            elif rsi.iloc[-1] > 70:
                signals.append('RSI_OVERBOUGHT')
                sell_signals += 1
        
        # MACD Signal
        macd_data = self.indicators.macd(close)
        if (not macd_data['MACD'].isna().iloc[-1] and 
            not macd_data['Signal'].isna().iloc[-1] and
            not macd_data['Histogram'].isna().iloc[-2]):
            
            # MACD crossover
            if (macd_data['MACD'].iloc[-2] <= macd_data['Signal'].iloc[-2] and 
                macd_data['MACD'].iloc[-1] > macd_data['Signal'].iloc[-1]):
                signals.append('MACD_BULLISH_CROSS')
                buy_signals += 1
            elif (macd_data['MACD'].iloc[-2] >= macd_data['Signal'].iloc[-2] and 
                  macd_data['MACD'].iloc[-1] < macd_data['Signal'].iloc[-1]):
                signals.append('MACD_BEARISH_CROSS')
                sell_signals += 1
        
        # Bollinger Bands Signal
        bb_data = self.indicators.bollinger_bands(close)
        if (not bb_data['Upper'].isna().iloc[-1] and 
            not bb_data['Lower'].isna().iloc[-1]):
            
            if close.iloc[-1] < bb_data['Lower'].iloc[-1]:
                signals.append('BB_OVERSOLD')
                buy_signals += 1
            elif close.iloc[-1] > bb_data['Upper'].iloc[-1]:
                signals.append('BB_OVERBOUGHT')
                sell_signals += 1
        
        # Moving Average Crossover
        ma_data = self.indicators.moving_averages(close)
        if (not ma_data['MA_Short'].isna().iloc[-2] and 
            not ma_data['MA_Long'].isna().iloc[-2]):
            
            if (ma_data['MA_Short'].iloc[-2] <= ma_data['MA_Long'].iloc[-2] and 
                ma_data['MA_Short'].iloc[-1] > ma_data['MA_Long'].iloc[-1]):
                signals.append('MA_BULLISH_CROSS')
                buy_signals += 1
            elif (ma_data['MA_Short'].iloc[-2] >= ma_data['MA_Long'].iloc[-2] and 
                  ma_data['MA_Short'].iloc[-1] < ma_data['MA_Long'].iloc[-1]):
                signals.append('MA_BEARISH_CROSS')
                sell_signals += 1
        
        # Stochastic Signal
        stoch_data = self.indicators.stochastic_oscillator(high, low, close)
        if (not stoch_data['Stoch_K'].isna().iloc[-1] and 
            not stoch_data['Stoch_D'].isna().iloc[-1]):
            
            if stoch_data['Stoch_K'].iloc[-1] < 20 and stoch_data['Stoch_D'].iloc[-1] < 20:
                signals.append('STOCH_OVERSOLD')
                buy_signals += 1
            elif stoch_data['Stoch_K'].iloc[-1] > 80 and stoch_data['Stoch_D'].iloc[-1] > 80:
                signals.append('STOCH_OVERBOUGHT')
                sell_signals += 1
        
        # Determine final signal
        total_signals = buy_signals + sell_signals
        if total_signals == 0:
            final_signal = 'HOLD'
            confidence = 50
        elif buy_signals > sell_signals:
            final_signal = 'BUY'
            confidence = (buy_signals / total_signals) * 100
        elif sell_signals > buy_signals:
            final_signal = 'SELL'
            confidence = (sell_signals / total_signals) * 100
        else:
            final_signal = 'HOLD'
            confidence = 50
        
        return {
            'signal': final_signal,
            'confidence': round(confidence, 2),
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'signals': signals
        }
    
    def calculate_price_targets(self, df: pd.DataFrame, signal: str) -> Dict:
        """
        Calculate price targets for take profit and stop loss
        
        Args:
            df: DataFrame with OHLCV data
            signal: Trading signal (BUY/SELL/HOLD)
        
        Returns:
            Dictionary with price targets
        """
        if df.empty or len(df) < 20:
            return {}
        
        current_price = df['Close'].iloc[-1]
        atr = self.indicators.average_true_range(df['High'], df['Low'], df['Close'])
        
        if atr.isna().iloc[-1]:
            atr_value = current_price * 0.02  # Default 2% if ATR not available
        else:
            atr_value = atr.iloc[-1]
        
        # Support and Resistance
        sr_levels = self.identify_support_resistance(df)
        
        targets = {
            'current_price': current_price,
            'atr': atr_value
        }
        
        if signal == 'BUY':
            # Take profit targets
            targets['take_profit_1'] = current_price + (atr_value * 2)
            targets['take_profit_2'] = current_price + (atr_value * 3)
            targets['take_profit_3'] = sr_levels.get('nearest_resistance', current_price * 1.1)
            
            # Stop loss
            targets['stop_loss'] = current_price - (atr_value * 1.5)
            targets['stop_loss_2'] = sr_levels.get('nearest_support', current_price * 0.95)
            
        elif signal == 'SELL':
            # Take profit targets (for short positions)
            targets['take_profit_1'] = current_price - (atr_value * 2)
            targets['take_profit_2'] = current_price - (atr_value * 3)
            targets['take_profit_3'] = sr_levels.get('nearest_support', current_price * 0.9)
            
            # Stop loss (for short positions)
            targets['stop_loss'] = current_price + (atr_value * 1.5)
            targets['stop_loss_2'] = sr_levels.get('nearest_resistance', current_price * 1.05)
        
        else:  # HOLD
            targets['support'] = sr_levels.get('nearest_support', current_price * 0.95)
            targets['resistance'] = sr_levels.get('nearest_resistance', current_price * 1.05)
        
        # Calculate percentage changes
        for key, value in targets.items():
            if key != 'current_price' and isinstance(value, (int, float)):
                targets[f'{key}_pct'] = round((value - current_price) / current_price * 100, 2)
        
        return targets
    
    def comprehensive_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive technical analysis
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            Dictionary with complete analysis
        """
        analysis = {
            'trend_analysis': self.analyze_trend(df),
            'signal_analysis': self.generate_signals(df),
            'support_resistance': self.identify_support_resistance(df),
            'price_targets': {}
        }
        
        # Add price targets based on signal
        signal = analysis['signal_analysis']['signal']
        analysis['price_targets'] = self.calculate_price_targets(df, signal)
        
        # Add individual indicator values
        if not df.empty and len(df) > 50:
            close = df['Close']
            high = df['High']
            low = df['Low']
            volume = df['Volume']
            
            # Calculate indicators once
            rsi_values = self.indicators.rsi(close)
            macd_values = self.indicators.macd(close)
            bb_values = self.indicators.bollinger_bands(close)
            stoch_values = self.indicators.stochastic_oscillator(high, low, close)
            ma_values = self.indicators.moving_averages(close)
            
            analysis['indicators'] = {
                'rsi': round(rsi_values.iloc[-1], 2) if not rsi_values.isna().iloc[-1] else None,
                'macd': {
                    'value': round(macd_values['MACD'].iloc[-1], 4) if not macd_values['MACD'].isna().iloc[-1] else None,
                    'signal': round(macd_values['Signal'].iloc[-1], 4) if not macd_values['Signal'].isna().iloc[-1] else None,
                    'histogram': round(macd_values['Histogram'].iloc[-1], 4) if not macd_values['Histogram'].isna().iloc[-1] else None
                },
                'bollinger': {
                    'upper': round(bb_values['Upper'].iloc[-1], 2) if not bb_values['Upper'].isna().iloc[-1] else None,
                    'middle': round(bb_values['Middle'].iloc[-1], 2) if not bb_values['Middle'].isna().iloc[-1] else None,
                    'lower': round(bb_values['Lower'].iloc[-1], 2) if not bb_values['Lower'].isna().iloc[-1] else None
                },
                'stochastic': {
                    'k': round(stoch_values['Stoch_K'].iloc[-1], 2) if not stoch_values['Stoch_K'].isna().iloc[-1] else None,
                    'd': round(stoch_values['Stoch_D'].iloc[-1], 2) if not stoch_values['Stoch_D'].isna().iloc[-1] else None
                },
                'moving_averages': {
                    'ma_20': round(ma_values['MA_Short'].iloc[-1], 2) if not ma_values['MA_Short'].isna().iloc[-1] else None,
                    'ma_50': round(ma_values['MA_Long'].iloc[-1], 2) if not ma_values['MA_Long'].isna().iloc[-1] else None
                }
            }
        
        return analysis