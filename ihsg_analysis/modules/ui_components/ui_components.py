import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional

class UIComponents:
    """Module for creating Streamlit UI components"""
    
    @staticmethod
    def create_price_chart(df: pd.DataFrame, title: str = "Stock Price Chart") -> go.Figure:
        """
        Create interactive price chart with volume
        
        Args:
            df: DataFrame with OHLCV data
            title: Chart title
        
        Returns:
            Plotly figure
        """
        if df.empty:
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(title, 'Volume'),
            row_width=[0.2, 0.7]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Volume bars
        colors = ['red' if row['Open'] - row['Close'] <= 0 else 'green' for index, row in df.iterrows()]
        
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['Volume'],
                name='Volume',
                marker_color=colors
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=title,
            yaxis_title='Price (IDR)',
            xaxis_rangeslider_visible=False,
            height=600,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        return fig
    
    @staticmethod
    def create_technical_indicators_chart(df: pd.DataFrame, indicators: Dict) -> go.Figure:
        """
        Create technical indicators chart
        
        Args:
            df: DataFrame with price data
            indicators: Dictionary with indicator values
        
        Returns:
            Plotly figure
        """
        if df.empty:
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price with Moving Averages', 'RSI', 'MACD')
        )
        
        # Price and Moving Averages
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Close'],
                name='Close Price',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        if 'MA_Short' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators['MA_Short'],
                    name='MA 20',
                    line=dict(color='orange')
                ),
                row=1, col=1
            )
        
        if 'MA_Long' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators['MA_Long'],
                    name='MA 50',
                    line=dict(color='red')
                ),
                row=1, col=1
            )
        
        # RSI
        if 'RSI' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators['RSI'],
                    name='RSI',
                    line=dict(color='purple')
                ),
                row=2, col=1
            )
            
            # Add RSI overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'MACD' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators['MACD'],
                    name='MACD',
                    line=dict(color='blue')
                ),
                row=3, col=1
            )
        
        if 'Signal' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators['Signal'],
                    name='Signal',
                    line=dict(color='red')
                ),
                row=3, col=1
            )
        
        if 'Histogram' in indicators:
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=indicators['Histogram'],
                    name='Histogram',
                    marker_color='green'
                ),
                row=3, col=1
            )
        
        # Update layout
        fig.update_layout(
            title='Technical Indicators',
            height=800,
            showlegend=True
        )
        
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1)
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        
        return fig
    
    @staticmethod
    def display_company_info(company_info: Dict):
        """
        Display company information in a formatted way
        
        Args:
            company_info: Dictionary with company information
        """
        if not company_info:
            st.warning("No company information available")
            return
        
        # Company header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(company_info.get('name', 'Unknown Company'))
            st.caption(f"{company_info.get('sector', 'Unknown Sector')} • {company_info.get('industry', 'Unknown Industry')}")
        
        with col2:
            if company_info.get('website'):
                st.markdown(f"[🌐 Website]({company_info['website']})")
        
        # Key metrics
        st.subheader("Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Market Cap",
                f"IDR {company_info.get('market_cap', 0):,.0f}"
            )
        
        with col2:
            st.metric(
                "P/E Ratio",
                f"{company_info.get('pe_ratio', 0):.2f}"
            )
        
        with col3:
            st.metric(
                "P/B Ratio",
                f"{company_info.get('pb_ratio', 0):.2f}"
            )
        
        with col4:
            st.metric(
                "Dividend Yield",
                f"{company_info.get('dividend_yield', 0):.2f}%"
            )
        
        # Additional metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "ROE",
                f"{company_info.get('roe', 0):.2f}%"
            )
        
        with col2:
            st.metric(
                "Debt to Equity",
                f"{company_info.get('debt_to_equity', 0):.2f}"
            )
        
        with col3:
            st.metric(
                "Beta",
                f"{company_info.get('beta', 0):.2f}"
            )
        
        with col4:
            st.metric(
                "Employees",
                f"{company_info.get('employees', 0):,}"
            )
        
        # Business description
        if company_info.get('description'):
            st.subheader("Business Description")
            st.write(company_info['description'])
    
    @staticmethod
    def display_technical_analysis(technical_analysis: Dict):
        """
        Display technical analysis results
        
        Args:
            technical_analysis: Dictionary with technical analysis results
        """
        if not technical_analysis:
            st.warning("No technical analysis available")
            return
        
        # Signal Analysis
        signal_analysis = technical_analysis.get('signal_analysis', {})
        
        st.subheader("🎯 Trading Signal")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            signal = signal_analysis.get('signal', 'HOLD')
            signal_color = {
                'BUY': 'green',
                'SELL': 'red',
                'HOLD': 'orange'
            }.get(signal, 'gray')
            
            st.markdown(f"### :{signal_color}[{signal}]")
            st.caption("Current Signal")
        
        with col2:
            confidence = signal_analysis.get('confidence', 0)
            st.metric("Confidence", f"{confidence}%")
        
        with col3:
            buy_signals = signal_analysis.get('buy_signals', 0)
            sell_signals = signal_analysis.get('sell_signals', 0)
            st.metric("Signals", f"📈 {buy_signals} / 📉 {sell_signals}")
        
        # Trend Analysis
        trend_analysis = technical_analysis.get('trend_analysis', {})
        
        st.subheader("📈 Trend Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trend = trend_analysis.get('trend', 'NEUTRAL')
            trend_color = {
                'BULLISH': 'green',
                'BEARISH': 'red',
                'NEUTRAL': 'orange'
            }.get(trend, 'gray')
            
            st.markdown(f"### :{trend_color}[{trend}]")
            st.caption("Overall Trend")
        
        with col2:
            strength = trend_analysis.get('strength', 0)
            st.metric("Strength", f"{strength}%")
        
        with col3:
            price_change = trend_analysis.get('price_change_20d', 0)
            st.metric("20D Change", f"{price_change:.2f}%")
        
        # Current Indicator Values
        if 'indicators' in technical_analysis:
            st.subheader("📊 Current Indicator Values")
            
            indicators = technical_analysis['indicators']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # RSI
                if 'rsi' in indicators:
                    rsi_value = indicators['rsi']
                    rsi_color = 'red' if rsi_value > 70 else 'green' if rsi_value < 30 else 'orange'
                    st.markdown(f"**RSI**: :{rsi_color}[{rsi_value:.2f}]")
                
                # Moving Averages
                if 'moving_averages' in indicators:
                    ma_data = indicators['moving_averages']
                    if ma_data.get('ma_20'):
                        st.markdown(f"**MA 20**: {ma_data['ma_20']:.2f}")
                    if ma_data.get('ma_50'):
                        st.markdown(f"**MA 50**: {ma_data['ma_50']:.2f}")
                
                # Stochastic
                if 'stochastic' in indicators:
                    stoch_data = indicators['stochastic']
                    if stoch_data.get('k'):
                        st.markdown(f"**Stoch K**: {stoch_data['k']:.2f}")
                    if stoch_data.get('d'):
                        st.markdown(f"**Stoch D**: {stoch_data['d']:.2f}")
            
            with col2:
                # MACD
                if 'macd' in indicators:
                    macd_data = indicators['macd']
                    if macd_data.get('value'):
                        st.markdown(f"**MACD**: {macd_data['value']:.4f}")
                    if macd_data.get('signal'):
                        st.markdown(f"**Signal**: {macd_data['signal']:.4f}")
                    if macd_data.get('histogram'):
                        st.markdown(f"**Histogram**: {macd_data['histogram']:.4f}")
                
                # Bollinger Bands
                if 'bollinger' in indicators:
                    bb_data = indicators['bollinger']
                    if bb_data.get('upper'):
                        st.markdown(f"**BB Upper**: {bb_data['upper']:.2f}")
                    if bb_data.get('middle'):
                        st.markdown(f"**BB Middle**: {bb_data['middle']:.2f}")
                    if bb_data.get('lower'):
                        st.markdown(f"**BB Lower**: {bb_data['lower']:.2f}")
        
        # Support and Resistance
        sr_data = technical_analysis.get('support_resistance', {})
        if sr_data:
            st.subheader("🎚️ Support & Resistance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Resistance Levels:**")
                resistance = sr_data.get('resistance', [])
                for i, level in enumerate(resistance[:5], 1):
                    st.markdown(f"  R{i}: {level:,.2f}")
            
            with col2:
                st.markdown("**Support Levels:**")
                support = sr_data.get('support', [])
                for i, level in enumerate(support[:5], 1):
                    st.markdown(f"  S{i}: {level:,.2f}")
        
        # Price Targets
        price_targets = technical_analysis.get('price_targets', {})
        if price_targets:
            st.subheader("🎯 Price Targets")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_price = price_targets.get('current_price', 0)
                st.metric("Current Price", f"{current_price:,.2f}")
            
            with col2:
                stop_loss = price_targets.get('stop_loss', 0)
                if stop_loss > 0:
                    st.metric("Stop Loss", f"{stop_loss:,.2f}")
            
            with col3:
                take_profit = price_targets.get('take_profit_1', 0)
                if take_profit > 0:
                    st.metric("Take Profit", f"{take_profit:,.2f}")
    
    @staticmethod
    def display_fundamental_analysis(fundamental_analysis: Dict):
        """
        Display fundamental analysis results
        
        Args:
            fundamental_analysis: Dictionary with fundamental analysis results
        """
        if not fundamental_analysis:
            st.warning("No fundamental analysis available")
            return
        
        # Overall Score
        score_data = fundamental_analysis.get('fundamental_score', {})
        
        st.subheader("📊 Fundamental Score")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_score = score_data.get('total_score', 0)
            grade = score_data.get('grade', 'F')
            st.markdown(f"### {total_score}/100")
            st.caption(f"Grade: {grade}")
        
        with col2:
            breakdown = score_data.get('breakdown', {})
            if breakdown:
                st.metric("Valuation", breakdown.get('valuation', 0))
        
        with col3:
            if breakdown:
                st.metric("Profitability", breakdown.get('profitability', 0))
        
        # Recommendation
        recommendation = fundamental_analysis.get('fundamental_recommendation', {})
        
        st.subheader("💡 Fundamental Recommendation")
        
        rec_action = recommendation.get('recommendation', 'HOLD')
        rec_color = {
            'STRONG_BUY': 'green',
            'BUY': 'green',
            'HOLD': 'orange',
            'WEAK_HOLD': 'orange',
            'SELL': 'red'
        }.get(rec_action, 'gray')
        
        st.markdown(f"### :{rec_color}[{rec_action.replace('_', ' ')}]")
        st.write(recommendation.get('reasoning', 'No reasoning provided'))
        
        # Valuation Analysis
        valuation = fundamental_analysis.get('valuation_analysis', {})
        
        st.subheader("💰 Valuation Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pe_analysis = valuation.get('pe_analysis', {})
            if pe_analysis:
                st.markdown("**P/E Ratio Analysis:**")
                st.write(f"Current: {pe_analysis.get('current', 0):.2f}")
                st.write(f"Status: {pe_analysis.get('status', 'Unknown')}")
                st.write(pe_analysis.get('interpretation', ''))
        
        with col2:
            pb_analysis = valuation.get('pb_analysis', {})
            if pb_analysis:
                st.markdown("**P/B Ratio Analysis:**")
                st.write(f"Current: {pb_analysis.get('current', 0):.2f}")
                st.write(f"Status: {pb_analysis.get('status', 'Unknown')}")
                st.write(pb_analysis.get('interpretation', ''))
        
        # Profitability Analysis
        profitability = fundamental_analysis.get('profitability_analysis', {})
        
        st.subheader("📈 Profitability Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            roe_analysis = profitability.get('roe_analysis', {})
            if roe_analysis:
                st.markdown("**ROE Analysis:**")
                st.write(f"Current: {roe_analysis.get('current', 0):.2f}%")
                st.write(f"Status: {roe_analysis.get('status', 'Unknown')}")
                st.write(roe_analysis.get('interpretation', ''))
        
        with col2:
            margin_analysis = profitability.get('profit_margin_analysis', {})
            if margin_analysis:
                st.markdown("**Profit Margin:**")
                st.write(f"Current: {margin_analysis.get('current', 0):.2f}%")
                st.write(f"Status: {margin_analysis.get('status', 'Unknown')}")
                st.write(margin_analysis.get('interpretation', ''))
        
        # Financial Health
        health = fundamental_analysis.get('financial_health_analysis', {})
        
        st.subheader("🏥 Financial Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            debt_analysis = health.get('debt_analysis', {})
            if debt_analysis:
                st.markdown("**Debt Analysis:**")
                st.write(f"D/E Ratio: {debt_analysis.get('current', 0):.2f}")
                st.write(f"Status: {debt_analysis.get('status', 'Unknown')}")
                st.write(debt_analysis.get('interpretation', ''))
        
        with col2:
            risk_analysis = health.get('risk_analysis', {})
            if risk_analysis:
                st.markdown("**Risk Analysis:**")
                st.write(f"Beta: {risk_analysis.get('current', 0):.2f}")
                st.write(f"Status: {risk_analysis.get('status', 'Unknown')}")
                st.write(risk_analysis.get('interpretation', ''))
        
        # Dividend Analysis
        dividend = fundamental_analysis.get('dividend_analysis', {})
        
        st.subheader("💵 Dividend Analysis")
        
        if dividend:
            st.write(f"**Current Yield:** {dividend.get('current_yield', 0):.2f}%")
            st.write(f"**Status:** {dividend.get('status', 'Unknown')}")
            st.write(dividend.get('interpretation', ''))
    
    @staticmethod
    def display_recommendation(recommendation: Dict):
        """
        Display comprehensive recommendation
        
        Args:
            recommendation: Dictionary with recommendation results
        """
        if not recommendation:
            st.warning("No recommendation available")
            return
        
        # Main recommendation
        rec_data = recommendation.get('recommendation', {})
        
        st.subheader("🎯 Final Recommendation")
        
        action = rec_data.get('action', 'HOLD')
        action_color = {
            'STRONG_BUY': 'green',
            'BUY': 'green',
            'HOLD': 'orange',
            'WEAK_HOLD': 'orange',
            'SELL': 'red',
            'AVOID': 'red'
        }.get(action, 'gray')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"### :{action_color}[{action.replace('_', ' ')}]")
            st.caption("Recommendation")
        
        with col2:
            confidence = rec_data.get('confidence', 0)
            st.metric("Confidence", f"{confidence}%")
        
        with col3:
            time_horizon = rec_data.get('time_horizon', 'N/A')
            st.metric("Time Horizon", time_horizon)
        
        st.write(rec_data.get('reasoning', 'No reasoning provided'))
        
        # Risk Management
        risk_mgmt = recommendation.get('risk_management', {})
        
        if risk_mgmt:
            st.subheader("⚠️ Risk Management")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                entry_price = risk_mgmt.get('entry_price', 0)
                st.metric("Entry Price", f"{entry_price:,.2f}")
            
            with col2:
                stop_loss = risk_mgmt.get('stop_loss', 0)
                if stop_loss > 0:
                    st.metric("Stop Loss", f"{stop_loss:,.2f}")
            
            with col3:
                take_profit = risk_mgmt.get('take_profit', 0)
                if take_profit > 0:
                    st.metric("Take Profit", f"{take_profit:,.2f}")
            
            with col4:
                rr_ratio = risk_mgmt.get('risk_reward_ratio', 0)
                if rr_ratio > 0:
                    st.metric("R/R Ratio", f"{rr_ratio:.2f}")
            
            # Position Sizing
            position_sizing = risk_mgmt.get('position_sizing', {})
            if position_sizing:
                st.write(f"**Recommended Position Size:** {position_sizing.get('recommended_size', 'N/A')}")
                st.write(f"**Reasoning:** {position_sizing.get('reasoning', 'N/A')}")
        
        # Actionable Insights
        insights = recommendation.get('actionable_insights', [])
        
        if insights:
            st.subheader("💡 Actionable Insights")
            
            for insight in insights:
                insight_type = insight.get('type', 'GENERAL')
                priority = insight.get('priority', 'MEDIUM')
                
                priority_emoji = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(priority, '⚪')
                
                type_emoji = {
                    'TECHNICAL': '📈',
                    'FUNDAMENTAL': '📊',
                    'RECOMMENDATION': '🎯'
                }.get(insight_type, '💡')
                
                with st.expander(f"{priority_emoji} {type_emoji} {insight.get('insight', 'No insight')}"):
                    st.write(f"**Action:** {insight.get('action', 'No action')}")
                    st.write(f"**Priority:** {priority}")
    
    @staticmethod
    def create_comparison_table(stocks_data: List[Dict]) -> pd.DataFrame:
        """
        Create comparison table for multiple stocks
        
        Args:
            stocks_data: List of stock analysis data
        
        Returns:
            DataFrame for comparison
        """
        comparison_data = []
        
        for stock in stocks_data:
            ticker = stock.get('ticker', 'Unknown')
            
            # Technical data
            tech_signal = stock.get('technical_signal', 'HOLD')
            tech_confidence = stock.get('technical_confidence', 0)
            
            # Fundamental data
            fund_score = stock.get('fundamental_score', 0)
            fund_rec = stock.get('fundamental_recommendation', 'HOLD')
            
            # Combined data
            combined_score = stock.get('combined_score', {}).get('combined_score', 0)
            final_rec = stock.get('recommendation', {}).get('action', 'HOLD')
            
            comparison_data.append({
                'Ticker': ticker,
                'Technical Signal': tech_signal,
                'Tech Confidence': f"{tech_confidence}%",
                'Fundamental Score': fund_score,
                'Fund. Rec': fund_rec,
                'Combined Score': combined_score,
                'Final Rec': final_rec
            })
        
        return pd.DataFrame(comparison_data)
    
    @staticmethod
    def display_market_overview(market_data: Dict):
        """
        Display market overview
        
        Args:
            market_data: Dictionary with market data
        """
        st.subheader("🌍 Market Overview")
        
        # Market sentiment
        sentiment = market_data.get('sentiment', {})
        if sentiment:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sentiment_status = sentiment.get('sentiment', 'NEUTRAL')
                sentiment_color = {
                    'BULLISH': 'green',
                    'BEARISH': 'red',
                    'NEUTRAL': 'orange'
                }.get(sentiment_status, 'gray')
                
                st.markdown(f"### :{sentiment_color}[{sentiment_status}]")
                st.caption("Market Sentiment")
            
            with col2:
                avg_change = sentiment.get('average_change', 0)
                st.metric("Avg Change", f"{avg_change:.2f}%")
            
            with col3:
                positive_ratio = sentiment.get('positive_ratio', 0)
                st.metric("Positive Ratio", f"{positive_ratio:.1%}")
        
        # Market indices
        indices = market_data.get('indices', {})
        if indices:
            st.subheader("📈 Market Indices")
            
            for index_name, index_data in indices.items():
                current = index_data.get('current', 0)
                change = index_data.get('change', 0)
                change_color = 'green' if change > 0 else 'red'
                
                st.metric(
                    index_name,
                    f"{current:,.2f}",
                    f"{change:.2f}%",
                    delta_color="normal" if change >= 0 else "inverse"
                )