#!/usr/bin/env python3
"""
Demo script to showcase IHSG Analysis functionality
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

def demo_technical_analysis():
    """Demonstrate technical analysis functionality"""
    print("🔍 Technical Analysis Demo")
    print("=" * 30)
    
    try:
        from ihsg_analysis.modules.technical_indicators import TechnicalIndicators, TechnicalAnalysis
        
        # Create sample price data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = []
        price = 1000
        
        for i in range(100):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            price *= (1 + change)
            prices.append(price)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Open': prices,
            'High': [p * 1.02 for p in prices],
            'Low': [p * 0.98 for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, 100)
        })
        
        df.set_index('Date', inplace=True)
        
        # Initialize technical analysis
        tech_analysis = TechnicalAnalysis()
        
        # Perform analysis
        results = tech_analysis.comprehensive_analysis(df)
        
        print(f"📈 Trading Signal: {results['signal_analysis']['signal']}")
        print(f"🎯 Confidence: {results['signal_analysis']['confidence']}%")
        print(f"📊 Trend: {results['trend_analysis']['trend']}")
        print(f"💪 Trend Strength: {results['trend_analysis']['strength']}%")
        
        # Show current indicator values
        if 'indicators' in results:
            indicators = results['indicators']
            print(f"\n📊 Current Indicators:")
            if indicators.get('rsi') and indicators['rsi'] is not None:
                print(f"   RSI: {indicators['rsi']:.2f}")
            if indicators.get('macd', {}).get('value') and indicators['macd']['value'] is not None:
                print(f"   MACD: {indicators['macd']['value']:.4f}")
            if indicators.get('moving_averages', {}).get('ma_20') and indicators['moving_averages']['ma_20'] is not None:
                print(f"   MA 20: {indicators['moving_averages']['ma_20']:.2f}")
            if indicators.get('moving_averages', {}).get('ma_50') and indicators['moving_averages']['ma_50'] is not None:
                print(f"   MA 50: {indicators['moving_averages']['ma_50']:.2f}")
        
        # Show support and resistance
        sr = results.get('support_resistance', {})
        if sr:
            print(f"\n🎚️ Support & Resistance:")
            if sr.get('nearest_support'):
                print(f"   Nearest Support: {sr['nearest_support']:.2f}")
            if sr.get('nearest_resistance'):
                print(f"   Nearest Resistance: {sr['nearest_resistance']:.2f}")
        
        # Show price targets
        targets = results.get('price_targets', {})
        if targets:
            print(f"\n🎯 Price Targets:")
            print(f"   Current Price: {targets.get('current_price', 0):.2f}")
            if targets.get('stop_loss'):
                print(f"   Stop Loss: {targets['stop_loss']:.2f}")
            if targets.get('take_profit_1'):
                print(f"   Take Profit: {targets['take_profit_1']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in technical analysis demo: {e}")
        return False

def demo_fundamental_analysis():
    """Demonstrate fundamental analysis functionality"""
    print("\n📊 Fundamental Analysis Demo")
    print("=" * 35)
    
    try:
        from ihsg_analysis.modules.fundamental_analysis import FundamentalAnalysis
        
        # Sample company data (BBCA-like)
        company_info = {
            'name': 'Bank Central Asia Tbk',
            'sector': 'Finance',
            'industry': 'Banking',
            'market_cap': 950000000000000,  # 950T IDR
            'pe_ratio': 18.5,
            'pb_ratio': 2.8,
            'dividend_yield': 3.2,
            'roe': 22.5,
            'debt_to_equity': 0.8,
            'revenue': 120000000000000,  # 120T IDR
            'net_income': 35000000000000,  # 35T IDR
            'book_value': 12000,
            'eps': 1500,
            'beta': 1.2,
            'description': 'Bank Central Asia is the largest private bank in Indonesia.',
            'website': 'https://www.bca.co.id',
            'employees': 25000
        }
        
        # Initialize fundamental analysis
        fund_analysis = FundamentalAnalysis()
        
        # Perform analysis
        results = fund_analysis.comprehensive_fundamental_analysis(company_info)
        
        print(f"🏦 Company: {company_info['name']}")
        print(f"📈 Fundamental Score: {results['fundamental_score']['total_score']}/100")
        print(f"🎓 Grade: {results['fundamental_score']['grade']}")
        print(f"💡 Recommendation: {results['fundamental_recommendation']['recommendation']}")
        
        # Show valuation analysis
        valuation = results.get('valuation_analysis', {})
        if valuation:
            print(f"\n💰 Valuation Analysis:")
            pe_analysis = valuation.get('pe_analysis', {})
            if pe_analysis:
                print(f"   P/E Ratio: {pe_analysis['current']:.2f} ({pe_analysis['status']})")
            pb_analysis = valuation.get('pb_analysis', {})
            if pb_analysis:
                print(f"   P/B Ratio: {pb_analysis['current']:.2f} ({pb_analysis['status']})")
        
        # Show profitability analysis
        profitability = results.get('profitability_analysis', {})
        if profitability:
            print(f"\n📊 Profitability Analysis:")
            roe_analysis = profitability.get('roe_analysis', {})
            if roe_analysis:
                print(f"   ROE: {roe_analysis['current']:.2f}% ({roe_analysis['status']})")
        
        # Show financial health
        health = results.get('financial_health_analysis', {})
        if health:
            print(f"\n🏥 Financial Health:")
            debt_analysis = health.get('debt_analysis', {})
            if debt_analysis:
                print(f"   Debt/Equity: {debt_analysis['current']:.2f} ({debt_analysis['status']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in fundamental analysis demo: {e}")
        return False

def demo_recommendation_engine():
    """Demonstrate recommendation engine functionality"""
    print("\n🎯 Recommendation Engine Demo")
    print("=" * 35)
    
    try:
        from ihsg_analysis.modules.recommendation_engine import RecommendationEngine
        
        # Sample technical analysis results
        technical_analysis = {
            'signal_analysis': {
                'signal': 'BUY',
                'confidence': 75,
                'signals': ['RSI_OVERSOLD', 'MACD_BULLISH_CROSS']
            },
            'trend_analysis': {
                'trend': 'BULLISH',
                'strength': 80
            },
            'price_targets': {
                'current_price': 8500,
                'stop_loss': 7650,
                'take_profit_1': 10200,
                'atr': 170
            }
        }
        
        # Sample fundamental analysis results
        fundamental_analysis = {
            'fundamental_score': {
                'total_score': 85,
                'grade': 'A'
            },
            'fundamental_recommendation': {
                'recommendation': 'BUY'
            }
        }
        
        # Initialize recommendation engine
        engine = RecommendationEngine()
        
        # Generate recommendation for different risk profiles
        for risk_profile in ['conservative', 'moderate', 'aggressive']:
            print(f"\n📊 Risk Profile: {risk_profile.upper()}")
            
            recommendation = engine.generate_comprehensive_recommendation(
                technical_analysis, fundamental_analysis, risk_profile
            )
            
            rec_data = recommendation.get('recommendation', {})
            print(f"   Action: {rec_data.get('action', 'HOLD')}")
            print(f"   Confidence: {rec_data.get('confidence', 0)}%")
            print(f"   Time Horizon: {rec_data.get('time_horizon', 'N/A')}")
            print(f"   Reasoning: {rec_data.get('reasoning', 'N/A')}")
            
            # Show risk management
            risk_mgmt = recommendation.get('risk_management', {})
            if risk_mgmt:
                print(f"   Entry Price: {risk_mgmt.get('entry_price', 0):,.2f}")
                print(f"   Stop Loss: {risk_mgmt.get('stop_loss', 0):,.2f}")
                print(f"   Take Profit: {risk_mgmt.get('take_profit', 0):,.2f}")
                print(f"   R/R Ratio: {risk_mgmt.get('risk_reward_ratio', 0):.2f}")
                
                position_sizing = risk_mgmt.get('position_sizing', {})
                if position_sizing:
                    print(f"   Position Size: {position_sizing.get('recommended_size', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in recommendation engine demo: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 IHSG Analysis Application Demo")
    print("=" * 40)
    print("This demo showcases the core functionality of the IHSG Analysis application.")
    print("The application provides comprehensive technical and fundamental analysis")
    print("for Indonesian Stock Market (IHSG) stocks with actionable recommendations.\n")
    
    # Demo technical analysis
    if not demo_technical_analysis():
        print("❌ Technical analysis demo failed!")
        return False
    
    # Demo fundamental analysis
    if not demo_fundamental_analysis():
        print("❌ Fundamental analysis demo failed!")
        return False
    
    # Demo recommendation engine
    if not demo_recommendation_engine():
        print("❌ Recommendation engine demo failed!")
        return False
    
    print("\n✅ All demos completed successfully!")
    print("\n🌟 Key Features Demonstrated:")
    print("   • Technical analysis with multiple indicators")
    print("   • Fundamental analysis with industry benchmarks")
    print("   • Risk-adjusted recommendations")
    print("   • Position sizing and risk management")
    print("   • Support for different risk profiles")
    
    print("\n🚀 To run the full application:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run: streamlit run app.py")
    print("   3. Open browser to http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)