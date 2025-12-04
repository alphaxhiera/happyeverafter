#!/usr/bin/env python3
"""
Simple test script for IHSG Analysis modules
"""

import warnings
warnings.filterwarnings("ignore")

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

def main():
    """Main test function"""
    print("🚀 IHSG Analysis Module Tests")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    print("\n✅ All tests passed! The application is ready to run.")
    print("\n🌐 To start the application, run:")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)