#!/usr/bin/env python3
"""
Simple demo script to showcase IHSG Analysis functionality
"""

import warnings
import os
os.environ['PYTHONWARNINGS'] = 'ignore'

warnings.filterwarnings("ignore")

import sys
import pandas as pd
import numpy as np

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_basic_functionality():
    """Demonstrate basic functionality"""
    print("🚀 IHSG Analysis Application Demo")
    print("=" * 40)
    print("This demo showcases the core functionality of the IHSG Analysis application.")
    print("The application provides comprehensive technical and fundamental analysis")
    print("for Indonesian Stock Market (IHSG) stocks with actionable recommendations.\n")
    
    try:
        # Test imports
        from ihsg_analysis.config import Config
        from ihsg_analysis.modules.data_fetcher import IHSGDataFetcher
        from ihsg_analysis.modules.technical_indicators import TechnicalIndicators
        from ihsg_analysis.modules.fundamental_analysis import FundamentalAnalysis
        from ihsg_analysis.modules.recommendation_engine import RecommendationEngine
        
        print("✅ All modules imported successfully!")
        
        # Test basic technical indicators
        print("\n🔧 Testing Technical Indicators...")
        
        # Create sample data
        np.random.seed(42)
        prices = pd.Series([1000, 1020, 1010, 1030, 1050, 1040, 1060, 1080, 1070, 1090])
        
        indicators = TechnicalIndicators()
        
        # Test RSI
        rsi = indicators.rsi(prices)
        print(f"   RSI: {rsi.iloc[-1]:.2f}")
        
        # Test Moving Averages
        ma = indicators.moving_averages(prices, 5, 8)
        print(f"   MA Short: {ma['MA_Short'].iloc[-1]:.2f}")
        print(f"   MA Long: {ma['MA_Long'].iloc[-1]:.2f}")
        
        # Test MACD
        macd = indicators.macd(prices)
        print(f"   MACD: {macd['MACD'].iloc[-1]:.4f}")
        print(f"   Signal: {macd['Signal'].iloc[-1]:.4f}")
        
        print("✅ Technical indicators working!")
        
        # Test fundamental analysis
        print("\n📊 Testing Fundamental Analysis...")
        
        fundamental = FundamentalAnalysis()
        
        # Sample company data
        company_info = {
            'name': 'Test Company',
            'sector': 'Banking',
            'industry': 'Finance',
            'pe_ratio': 15.5,
            'pb_ratio': 2.2,
            'roe': 18.5,
            'debt_to_equity': 0.8
        }
        
        # Test valuation analysis
        valuation = fundamental.analyze_valuation_ratios(company_info)
        print(f"   P/E Status: {valuation['pe_analysis']['status']}")
        print(f"   P/B Status: {valuation['pb_analysis']['status']}")
        
        print("✅ Fundamental analysis working!")
        
        # Test recommendation engine
        print("\n🎯 Testing Recommendation Engine...")
        
        engine = RecommendationEngine()
        
        # Sample analysis data
        tech_analysis = {
            'signal_analysis': {'signal': 'BUY', 'confidence': 75},
            'trend_analysis': {'trend': 'BULLISH', 'strength': 80}
        }
        
        fund_analysis = {
            'fundamental_score': {'total_score': 85},
            'fundamental_recommendation': {'recommendation': 'BUY'}
        }
        
        recommendation = engine.generate_comprehensive_recommendation(
            tech_analysis, fund_analysis, 'moderate'
        )
        
        print(f"   Recommendation: {recommendation['recommendation']['action']}")
        print(f"   Confidence: {recommendation['recommendation']['confidence']}%")
        
        print("✅ Recommendation engine working!")
        
        print("\n🎉 All components tested successfully!")
        print("\n🌟 Key Features:")
        print("   • Technical analysis with 15+ indicators")
        print("   • Fundamental analysis with industry benchmarks")
        print("   • Risk-adjusted recommendations")
        print("   • Support for different risk profiles")
        print("   • Portfolio optimization")
        
        print("\n🚀 To run the full application:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run: streamlit run app.py")
        print("   3. Open browser to http://localhost:8501")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = demo_basic_functionality()
    sys.exit(0 if success else 1)