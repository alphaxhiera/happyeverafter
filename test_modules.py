#!/usr/bin/env python3
"""
Test script for IHSG Analysis modules
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        # Test configuration
        from ihsg_analysis.config import Config
        print("✅ Config imported successfully")
        
        # Test data fetcher
        from ihsg_analysis.modules.data_fetcher import IHSGDataFetcher
        print("✅ Data fetcher imported successfully")
        
        # Test technical indicators
        from ihsg_analysis.modules.technical_indicators import TechnicalIndicators, TechnicalAnalysis
        print("✅ Technical indicators imported successfully")
        
        # Test fundamental analysis
        from ihsg_analysis.modules.fundamental_analysis import FundamentalAnalysis
        print("✅ Fundamental analysis imported successfully")
        
        # Test recommendation engine
        from ihsg_analysis.modules.recommendation_engine import RecommendationEngine
        print("✅ Recommendation engine imported successfully")
        
        # Test UI components
        from ihsg_analysis.modules.ui_components import UIComponents
        print("✅ UI components imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of modules"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        # Test data fetcher
        from ihsg_analysis.modules.data_fetcher import IHSGDataFetcher
        
        fetcher = IHSGDataFetcher()
        print("✅ Data fetcher initialized")
        
        # Test technical indicators
        from ihsg_analysis.modules.technical_indicators import TechnicalIndicators
        import pandas as pd
        import numpy as np
        
        # Create sample data
        sample_prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
        
        indicators = TechnicalIndicators()
        rsi = indicators.rsi(sample_prices)
        print(f"✅ RSI calculated: {rsi.iloc[-1]:.2f}")
        
        # Test fundamental analysis
        from ihsg_analysis.modules.fundamental_analysis import FundamentalAnalysis
        
        fundamental = FundamentalAnalysis()
        print("✅ Fundamental analysis initialized")
        
        # Test recommendation engine
        from ihsg_analysis.modules.recommendation_engine import RecommendationEngine
        
        engine = RecommendationEngine()
        print("✅ Recommendation engine initialized")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 IHSG Analysis Module Tests")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed!")
        return False
    
    print("\n✅ All tests passed! The application is ready to run.")
    print("\n🌐 To start the application, run:")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)