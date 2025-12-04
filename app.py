import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ihsg_analysis'))

from ihsg_analysis.modules import (
    IHSGDataFetcher,
    TechnicalAnalysis,
    FundamentalAnalysis,
    RecommendationEngine,
    UIComponents
)
from ihsg_analysis.config import Config

# Configure page
st.set_page_config(
    page_title="IHSG Technical & Fundamental Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-buy {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-sell {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-hold {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_fetcher' not in st.session_state:
    st.session_state.data_fetcher = IHSGDataFetcher()
if 'technical_analysis' not in st.session_state:
    st.session_state.technical_analysis = TechnicalAnalysis()
if 'fundamental_analysis' not in st.session_state:
    st.session_state.fundamental_analysis = FundamentalAnalysis()
if 'recommendation_engine' not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()
if 'ui_components' not in st.session_state:
    st.session_state.ui_components = UIComponents()

# Main title
st.markdown('<h1 class="main-header">📈 IHSG Technical & Fundamental Analysis</h1>', 
            unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 Analysis Settings")

# Stock selection
st.sidebar.subheader("📊 Stock Selection")
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    Config.IHSG_TICKERS,
    index=0
)

# Time period
st.sidebar.subheader("📅 Time Period")
time_period = st.sidebar.selectbox(
    "Select Period",
    ["1mo", "3mo", "6mo", "1y", "2y"],
    index=3
)

# Risk profile
st.sidebar.subheader("⚠️ Risk Profile")
risk_profile = st.sidebar.selectbox(
    "Select Risk Profile",
    ["conservative", "moderate", "aggressive"],
    index=1
)

# Analysis type
st.sidebar.subheader("🔍 Analysis Type")
analysis_type = st.sidebar.multiselect(
    "Select Analyses",
    ["Technical Analysis", "Fundamental Analysis", "Recommendation"],
    default=["Technical Analysis", "Fundamental Analysis", "Recommendation"]
)

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Single Stock Analysis", "📈 Market Overview", "🔄 Portfolio Analysis"])

with tab1:
    st.header("Single Stock Analysis")
    
    # Analyze button
    if st.button(f"🔍 Analyze {selected_stock}", type="primary"):
        with st.spinner(f"Fetching data for {selected_stock}..."):
            # Fetch stock data
            stock_data = st.session_state.data_fetcher.get_stock_data(selected_stock, time_period)
            company_info = st.session_state.data_fetcher.get_company_info(selected_stock)
            financial_statements = st.session_state.data_fetcher.get_financial_statements(selected_stock)
        
        if stock_data.empty:
            st.error(f"No data available for {selected_stock}")
        else:
            # Display company info
            if company_info:
                st.session_state.ui_components.display_company_info(company_info)
            
            # Price chart
            st.subheader("📈 Price Chart")
            price_chart = st.session_state.ui_components.create_price_chart(
                stock_data, f"{selected_stock} Price Chart"
            )
            st.plotly_chart(price_chart, use_container_width=True)
            
            # Technical Analysis
            if "Technical Analysis" in analysis_type:
                with st.spinner("Performing technical analysis..."):
                    technical_results = st.session_state.technical_analysis.comprehensive_analysis(stock_data)
                
                st.session_state.ui_components.display_technical_analysis(technical_results)
                
                # Technical indicators chart
                st.subheader("📊 Technical Indicators")
                
                # Prepare indicators data for chart
                indicators_data = {}
                if technical_results.get('indicators'):
                    indicators = technical_results['indicators']
                    
                    # Get indicator series
                    tech_indicators = st.session_state.technical_analysis.indicators
                    
                    # Moving averages
                    if indicators.get('moving_averages', {}).get('ma_20'):
                        ma_data = tech_indicators.moving_averages(stock_data['Close'])
                        indicators_data['MA_Short'] = ma_data['MA_Short']
                        indicators_data['MA_Long'] = ma_data['MA_Long']
                    
                    # RSI
                    if indicators.get('rsi'):
                        indicators_data['RSI'] = tech_indicators.rsi(stock_data['Close'])
                    
                    # MACD
                    if indicators.get('macd', {}).get('value'):
                        macd_data = tech_indicators.macd(stock_data['Close'])
                        indicators_data['MACD'] = macd_data['MACD']
                        indicators_data['Signal'] = macd_data['Signal']
                        indicators_data['Histogram'] = macd_data['Histogram']
                
                if indicators_data:
                    indicators_chart = st.session_state.ui_components.create_technical_indicators_chart(
                        stock_data, indicators_data
                    )
                    st.plotly_chart(indicators_chart, use_container_width=True)
            
            # Fundamental Analysis
            if "Fundamental Analysis" in analysis_type and company_info:
                with st.spinner("Performing fundamental analysis..."):
                    fundamental_results = st.session_state.fundamental_analysis.comprehensive_fundamental_analysis(
                        company_info, financial_statements
                    )
                
                st.session_state.ui_components.display_fundamental_analysis(fundamental_results)
            
            # Recommendation
            if "Recommendation" in analysis_type:
                with st.spinner("Generating recommendation..."):
                    # Get technical and fundamental results
                    technical_results = st.session_state.technical_analysis.comprehensive_analysis(stock_data)
                    fundamental_results = st.session_state.fundamental_analysis.comprehensive_fundamental_analysis(
                        company_info, financial_statements
                    )
                    
                    # Generate recommendation
                    recommendation = st.session_state.recommendation_engine.generate_comprehensive_recommendation(
                        technical_results, fundamental_results, risk_profile
                    )
                
                st.session_state.ui_components.display_recommendation(recommendation)

with tab2:
    st.header("Market Overview")
    
    # Market analysis button
    if st.button("🌍 Analyze Market", type="primary"):
        with st.spinner("Analyzing market data..."):
            # Get market sentiment
            market_sentiment = st.session_state.data_fetcher.calculate_market_sentiment(Config.IHSG_TICKERS)
            
            # Get market indices
            market_indices = st.session_state.data_fetcher.get_market_indices()
            
            market_data = {
                'sentiment': market_sentiment,
                'indices': market_indices
            }
        
        st.session_state.ui_components.display_market_overview(market_data)
        
        # Multiple stocks comparison
        st.subheader("📊 Stock Comparison")
        
        with st.spinner("Analyzing multiple stocks..."):
            # Get data for multiple stocks
            multiple_stocks_data = st.session_state.data_fetcher.get_multiple_stocks(
                Config.IHSG_TICKERS[:5], "3mo"  # Limit to first 5 for performance
            )
            
            comparison_results = []
            
            for ticker, data in multiple_stocks_data.items():
                if not data.empty:
                    # Technical analysis
                    tech_results = st.session_state.technical_analysis.comprehensive_analysis(data)
                    
                    # Get company info
                    company_info = st.session_state.data_fetcher.get_company_info(ticker)
                    
                    # Fundamental analysis
                    fund_results = {}
                    if company_info:
                        fund_results = st.session_state.fundamental_analysis.comprehensive_fundamental_analysis(
                            company_info
                        )
                    
                    # Combined recommendation
                    recommendation = st.session_state.recommendation_engine.generate_comprehensive_recommendation(
                        tech_results, fund_results, risk_profile
                    )
                    
                    comparison_results.append({
                        'ticker': ticker,
                        'technical_signal': tech_results.get('signal_analysis', {}).get('signal', 'HOLD'),
                        'technical_confidence': tech_results.get('signal_analysis', {}).get('confidence', 0),
                        'fundamental_score': fund_results.get('fundamental_score', {}).get('total_score', 0),
                        'fundamental_recommendation': fund_results.get('fundamental_recommendation', {}).get('recommendation', 'HOLD'),
                        'combined_score': recommendation.get('combined_score', {}).get('combined_score', 0),
                        'recommendation': recommendation.get('recommendation', {})
                    })
        
        if comparison_results:
            # Create comparison table
            comparison_df = st.session_state.ui_components.create_comparison_table(comparison_results)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Visualize results
            st.subheader("📈 Analysis Visualization")
            
            # Create scores chart
            tickers = [result['ticker'] for result in comparison_results]
            tech_scores = [result['technical_confidence'] for result in comparison_results]
            fund_scores = [result['fundamental_score'] for result in comparison_results]
            combined_scores = [result['combined_score'] for result in comparison_results]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Technical Score',
                x=tickers,
                y=tech_scores,
                marker_color='blue'
            ))
            
            fig.add_trace(go.Bar(
                name='Fundamental Score',
                x=tickers,
                y=fund_scores,
                marker_color='green'
            ))
            
            fig.add_trace(go.Bar(
                name='Combined Score',
                x=tickers,
                y=combined_scores,
                marker_color='red'
            ))
            
            fig.update_layout(
                title='Stock Comparison Scores',
                xaxis_title='Stocks',
                yaxis_title='Score',
                barmode='group',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Portfolio Analysis")
    
    st.subheader("📊 Portfolio Recommendations")
    
    # Portfolio settings
    col1, col2 = st.columns(2)
    
    with col1:
        total_capital = st.number_input(
            "Total Capital (IDR)",
            min_value=1000000,
            max_value=10000000000,
            value=100000000,
            step=10000000
        )
    
    with col2:
        portfolio_risk_profile = st.selectbox(
            "Portfolio Risk Profile",
            ["conservative", "moderate", "aggressive"],
            index=1
        )
    
    # Generate portfolio button
    if st.button("🎯 Generate Portfolio", type="primary"):
        with st.spinner("Analyzing stocks for portfolio..."):
            # Get data for all stocks
            all_stocks_data = st.session_state.data_fetcher.get_multiple_stocks(
                Config.IHSG_TICKERS, "6mo"
            )
            
            portfolio_analysis = []
            
            for ticker, data in all_stocks_data.items():
                if not data.empty:
                    # Technical analysis
                    tech_results = st.session_state.technical_analysis.comprehensive_analysis(data)
                    
                    # Get company info
                    company_info = st.session_state.data_fetcher.get_company_info(ticker)
                    
                    # Fundamental analysis
                    fund_results = {}
                    if company_info:
                        fund_results = st.session_state.fundamental_analysis.comprehensive_fundamental_analysis(
                            company_info
                        )
                    
                    # Combined recommendation
                    recommendation = st.session_state.recommendation_engine.generate_comprehensive_recommendation(
                        tech_results, fund_results, portfolio_risk_profile
                    )
                    
                    portfolio_analysis.append({
                        'ticker': ticker,
                        'technical_analysis': tech_results,
                        'fundamental_analysis': fund_results,
                        'recommendation': recommendation
                    })
        
        # Generate portfolio recommendations
        portfolio_recommendations = st.session_state.recommendation_engine.generate_portfolio_recommendations(
            portfolio_analysis, total_capital, portfolio_risk_profile
        )
        
        # Display portfolio recommendations
        st.subheader("🎯 Recommended Portfolio")
        
        recommendations = portfolio_recommendations.get('portfolio_recommendations', [])
        
        if recommendations:
            # Create portfolio summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Allocated",
                    f"IDR {portfolio_recommendations.get('total_allocated', 0):,.0f}"
                )
            
            with col2:
                st.metric(
                    "Remaining Capital",
                    f"IDR {portfolio_recommendations.get('remaining_capital', 0):,.0f}"
                )
            
            with col3:
                st.metric(
                    "Number of Positions",
                    portfolio_recommendations.get('number_of_positions', 0)
                )
            
            with col4:
                diversification = portfolio_recommendations.get('diversification_score', {})
                st.metric(
                    "Diversification",
                    diversification.get('status', 'Unknown')
                )
            
            # Portfolio table
            portfolio_data = []
            for rec in recommendations:
                portfolio_data.append({
                    'Ticker': rec['ticker'],
                    'Action': rec['recommendation'].get('action', 'HOLD'),
                    'Position Size': f"IDR {rec['position_size']:,.0f}",
                    'Weight': f"{rec['position_percentage']:.1f}%",
                    'Score': rec['combined_score']
                })
            
            portfolio_df = pd.DataFrame(portfolio_data)
            st.dataframe(portfolio_df, use_container_width=True)
            
            # Portfolio allocation chart
            st.subheader("📊 Portfolio Allocation")
            
            fig = go.Figure(data=[go.Pie(
                labels=[rec['ticker'] for rec in recommendations],
                values=[rec['position_percentage'] for rec in recommendations],
                hole=0.3
            )])
            
            fig.update_layout(
                title="Portfolio Allocation",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No suitable stocks found for the current risk profile and market conditions.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "📈 IHSG Technical & Fundamental Analysis Tool | "
    "Data provided by Yahoo Finance | "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)

# Disclaimer
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.8em; margin-top: 1rem;'>"
    "<strong>Disclaimer:</strong> This tool is for educational purposes only. "
    "Not financial advice. Always do your own research before investing."
    "</div>",
    unsafe_allow_html=True
)