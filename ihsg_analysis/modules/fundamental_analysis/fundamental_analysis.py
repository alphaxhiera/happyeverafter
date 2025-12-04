import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class FundamentalAnalysis:
    """Module for performing fundamental analysis of stocks"""
    
    def __init__(self):
        self.industry_benchmarks = {
            'banking': {
                'pe_ratio': (8, 15),
                'pb_ratio': (1, 2),
                'roe': (10, 20),
                'roe_avg': 15,
                'debt_to_equity': (0, 10),
                'nim': (4, 6),
                'npl': (0, 3)
            },
            'consumer': {
                'pe_ratio': (15, 25),
                'pb_ratio': (2, 5),
                'roe': (15, 25),
                'roe_avg': 20,
                'debt_to_equity': (0, 1),
                'revenue_growth': (10, 20)
            },
            'infrastructure': {
                'pe_ratio': (12, 20),
                'pb_ratio': (1.5, 3),
                'roe': (12, 18),
                'roe_avg': 15,
                'debt_to_equity': (0, 2),
                'ebitda_margin': (15, 25)
            },
            'mining': {
                'pe_ratio': (10, 20),
                'pb_ratio': (1, 3),
                'roe': (10, 20),
                'roe_avg': 15,
                'debt_to_equity': (0, 1.5),
                'roe': (8, 15)
            },
            'telecommunication': {
                'pe_ratio': (15, 25),
                'pb_ratio': (2, 4),
                'roe': (15, 25),
                'roe_avg': 20,
                'debt_to_equity': (0, 1.5),
                'ebitda_margin': (30, 45)
            },
            'default': {
                'pe_ratio': (10, 20),
                'pb_ratio': (1, 3),
                'roe': (10, 20),
                'roe_avg': 15,
                'debt_to_equity': (0, 1.5)
            }
        }
    
    def analyze_valuation_ratios(self, company_info: Dict) -> Dict:
        """
        Analyze valuation ratios (P/E, P/B, etc.)
        
        Args:
            company_info: Dictionary with company financial information
        
        Returns:
            Dictionary with valuation analysis
        """
        pe_ratio = company_info.get('pe_ratio', 0)
        pb_ratio = company_info.get('pb_ratio', 0)
        market_cap = company_info.get('market_cap', 0)
        
        # Get industry benchmarks
        industry = company_info.get('industry', '').lower()
        sector = company_info.get('sector', '').lower()
        
        benchmark_key = 'default'
        for key in self.industry_benchmarks.keys():
            if key in industry or key in sector:
                benchmark_key = key
                break
        
        benchmarks = self.industry_benchmarks[benchmark_key]
        
        # Analyze P/E ratio
        pe_analysis = {
            'current': pe_ratio,
            'industry_low': benchmarks['pe_ratio'][0],
            'industry_high': benchmarks['pe_ratio'][1],
            'status': 'FAIR'
        }
        
        if pe_ratio < benchmarks['pe_ratio'][0]:
            pe_analysis['status'] = 'UNDervalued'
            pe_analysis['interpretation'] = 'Stock appears undervalued compared to industry'
        elif pe_ratio > benchmarks['pe_ratio'][1]:
            pe_analysis['status'] = 'OVERvalued'
            pe_analysis['interpretation'] = 'Stock appears overvalued compared to industry'
        else:
            pe_analysis['interpretation'] = 'P/E ratio is within industry range'
        
        # Analyze P/B ratio
        pb_analysis = {
            'current': pb_ratio,
            'industry_low': benchmarks['pb_ratio'][0],
            'industry_high': benchmarks['pb_ratio'][1],
            'status': 'FAIR'
        }
        
        if pb_ratio < benchmarks['pb_ratio'][0]:
            pb_analysis['status'] = 'UNDervalued'
            pb_analysis['interpretation'] = 'Stock appears undervalued based on book value'
        elif pb_ratio > benchmarks['pb_ratio'][1]:
            pb_analysis['status'] = 'OVERvalued'
            pb_analysis['interpretation'] = 'Stock appears overvalued based on book value'
        else:
            pb_analysis['interpretation'] = 'P/B ratio is within industry range'
        
        # Market cap classification
        if market_cap > 50_000_000_000:  # > 50T IDR
            market_cap_tier = 'Large Cap'
        elif market_cap > 10_000_000_000:  # > 10T IDR
            market_cap_tier = 'Mid Cap'
        else:
            market_cap_tier = 'Small Cap'
        
        return {
            'pe_analysis': pe_analysis,
            'pb_analysis': pb_analysis,
            'market_cap_tier': market_cap_tier,
            'overall_valuation': self._calculate_overall_valuation(pe_analysis, pb_analysis)
        }
    
    def analyze_profitability(self, company_info: Dict, financial_statements: Dict) -> Dict:
        """
        Analyze profitability metrics
        
        Args:
            company_info: Dictionary with company information
            financial_statements: Dictionary with financial statements
        
        Returns:
            Dictionary with profitability analysis
        """
        roe = company_info.get('roe', 0)
        revenue = company_info.get('revenue', 0)
        net_income = company_info.get('net_income', 0)
        
        # Get industry benchmarks
        industry = company_info.get('industry', '').lower()
        sector = company_info.get('sector', '').lower()
        
        benchmark_key = 'default'
        for key in self.industry_benchmarks.keys():
            if key in industry or key in sector:
                benchmark_key = key
                break
        
        benchmarks = self.industry_benchmarks[benchmark_key]
        
        # ROE Analysis
        roe_analysis = {
            'current': roe,
            'industry_average': benchmarks.get('roe_avg', 15),
            'status': 'AVERAGE'
        }
        
        if roe > benchmarks.get('roe_avg', 15):
            roe_analysis['status'] = 'EXCELLENT'
            roe_analysis['interpretation'] = 'Company generates excellent returns for shareholders'
        elif roe > 10:
            roe_analysis['status'] = 'GOOD'
            roe_analysis['interpretation'] = 'Company generates good returns for shareholders'
        elif roe > 5:
            roe_analysis['status'] = 'AVERAGE'
            roe_analysis['interpretation'] = 'Company generates average returns for shareholders'
        else:
            roe_analysis['status'] = 'POOR'
            roe_analysis['interpretation'] = 'Company generates poor returns for shareholders'
        
        # Profit Margin Analysis
        profit_margin = 0
        if revenue > 0:
            profit_margin = (net_income / revenue) * 100
        
        profit_margin_analysis = {
            'current': profit_margin,
            'status': 'AVERAGE'
        }
        
        if profit_margin > 20:
            profit_margin_analysis['status'] = 'EXCELLENT'
            profit_margin_analysis['interpretation'] = 'Company has excellent profit margins'
        elif profit_margin > 10:
            profit_margin_analysis['status'] = 'GOOD'
            profit_margin_analysis['interpretation'] = 'Company has good profit margins'
        elif profit_margin > 5:
            profit_margin_analysis['status'] = 'AVERAGE'
            profit_margin_analysis['interpretation'] = 'Company has average profit margins'
        else:
            profit_margin_analysis['status'] = 'POOR'
            profit_margin_analysis['interpretation'] = 'Company has low profit margins'
        
        return {
            'roe_analysis': roe_analysis,
            'profit_margin_analysis': profit_margin_analysis,
            'overall_profitability': self._calculate_overall_profitability(roe_analysis, profit_margin_analysis)
        }
    
    def analyze_financial_health(self, company_info: Dict) -> Dict:
        """
        Analyze financial health and solvency
        
        Args:
            company_info: Dictionary with company information
        
        Returns:
            Dictionary with financial health analysis
        """
        debt_to_equity = company_info.get('debt_to_equity', 0)
        beta = company_info.get('beta', 1)
        
        # Get industry benchmarks
        industry = company_info.get('industry', '').lower()
        sector = company_info.get('sector', '').lower()
        
        benchmark_key = 'default'
        for key in self.industry_benchmarks.keys():
            if key in industry or key in sector:
                benchmark_key = key
                break
        
        benchmarks = self.industry_benchmarks[benchmark_key]
        
        # Debt to Equity Analysis
        dte_analysis = {
            'current': debt_to_equity,
            'industry_max': benchmarks.get('debt_to_equity', (0, 1.5))[1],
            'status': 'HEALTHY'
        }
        
        if debt_to_equity < 0.5:
            dte_analysis['status'] = 'VERY_HEALTHY'
            dte_analysis['interpretation'] = 'Company has very low debt levels'
        elif debt_to_equity < benchmarks.get('debt_to_equity', (0, 1.5))[1]:
            dte_analysis['status'] = 'HEALTHY'
            dte_analysis['interpretation'] = 'Company has manageable debt levels'
        elif debt_to_equity < 2:
            dte_analysis['status'] = 'MODERATE'
            dte_analysis['interpretation'] = 'Company has moderate debt levels'
        else:
            dte_analysis['status'] = 'HIGH_RISK'
            dte_analysis['interpretation'] = 'Company has high debt levels'
        
        # Beta Analysis (Risk)
        beta_analysis = {
            'current': beta,
            'status': 'AVERAGE'
        }
        
        if beta < 0.8:
            beta_analysis['status'] = 'LOW_RISK'
            beta_analysis['interpretation'] = 'Stock has lower volatility than market'
        elif beta < 1.2:
            beta_analysis['status'] = 'AVERAGE'
            beta_analysis['interpretation'] = 'Stock has average volatility similar to market'
        elif beta < 1.5:
            beta_analysis['status'] = 'HIGH_RISK'
            beta_analysis['interpretation'] = 'Stock has higher volatility than market'
        else:
            beta_analysis['status'] = 'VERY_HIGH_RISK'
            beta_analysis['interpretation'] = 'Stock has very high volatility'
        
        return {
            'debt_analysis': dte_analysis,
            'risk_analysis': beta_analysis,
            'overall_financial_health': self._calculate_overall_financial_health(dte_analysis, beta_analysis)
        }
    
    def analyze_dividend(self, company_info: Dict) -> Dict:
        """
        Analyze dividend sustainability and yield
        
        Args:
            company_info: Dictionary with company information
        
        Returns:
            Dictionary with dividend analysis
        """
        dividend_yield = company_info.get('dividend_yield', 0)
        
        dividend_analysis = {
            'current_yield': dividend_yield,
            'status': 'AVERAGE'
        }
        
        if dividend_yield > 6:
            dividend_analysis['status'] = 'HIGH_YIELD'
            dividend_analysis['interpretation'] = 'Stock offers high dividend yield'
        elif dividend_yield > 3:
            dividend_analysis['status'] = 'GOOD_YIELD'
            dividend_analysis['interpretation'] = 'Stock offers good dividend yield'
        elif dividend_yield > 1:
            dividend_analysis['status'] = 'MODERATE_YIELD'
            dividend_analysis['interpretation'] = 'Stock offers moderate dividend yield'
        elif dividend_yield > 0:
            dividend_analysis['status'] = 'LOW_YIELD'
            dividend_analysis['interpretation'] = 'Stock offers low dividend yield'
        else:
            dividend_analysis['status'] = 'NO_DIVIDEND'
            dividend_analysis['interpretation'] = 'Company does not pay dividends'
        
        return dividend_analysis
    
    def calculate_intrinsic_value(self, company_info: Dict, financial_statements: Dict) -> Dict:
        """
        Calculate intrinsic value using various methods
        
        Args:
            company_info: Dictionary with company information
            financial_statements: Dictionary with financial statements
        
        Returns:
            Dictionary with intrinsic value calculations
        """
        eps = company_info.get('eps', 0)
        book_value = company_info.get('book_value', 0)
        pe_ratio = company_info.get('pe_ratio', 0)
        pb_ratio = company_info.get('pb_ratio', 0)
        
        intrinsic_values = {}
        
        # Graham Number (Value investing formula)
        if eps > 0 and book_value > 0:
            graham_number = np.sqrt(22.5 * eps * book_value)
            intrinsic_values['graham_number'] = graham_number
        
        # Average P/E Method
        if eps > 0:
            industry_pe = 15  # Default industry P/E
            intrinsic_values['pe_method'] = eps * industry_pe
        
        # Book Value Method
        if book_value > 0:
            intrinsic_values['book_value_method'] = book_value * 1.5  # 1.5x book value
        
        # Discounted Cash Flow (simplified)
        if financial_statements.get('cash_flow') is not None:
            try:
                cf = financial_statements['cash_flow']
                if not cf.empty:
                    # Get operating cash flow for the most recent year
                    ocf = cf.iloc[0, 0] if len(cf) > 0 else 0
                    if ocf > 0:
                        # Simplified DCF with 10% discount rate and 3% growth
                        intrinsic_values['dcf_method'] = ocf * (1 + 0.03) / (0.10 - 0.03)
            except:
                pass
        
        return intrinsic_values
    
    def comprehensive_fundamental_analysis(self, company_info: Dict, financial_statements: Dict = None) -> Dict:
        """
        Perform comprehensive fundamental analysis
        
        Args:
            company_info: Dictionary with company information
            financial_statements: Dictionary with financial statements
        
        Returns:
            Dictionary with complete fundamental analysis
        """
        if financial_statements is None:
            financial_statements = {}
        
        analysis = {
            'company_info': company_info,
            'valuation_analysis': self.analyze_valuation_ratios(company_info),
            'profitability_analysis': self.analyze_profitability(company_info, financial_statements),
            'financial_health_analysis': self.analyze_financial_health(company_info),
            'dividend_analysis': self.analyze_dividend(company_info),
            'intrinsic_value_analysis': self.calculate_intrinsic_value(company_info, financial_statements)
        }
        
        # Calculate overall fundamental score
        analysis['fundamental_score'] = self._calculate_fundamental_score(analysis)
        analysis['fundamental_recommendation'] = self._get_fundamental_recommendation(analysis)
        
        return analysis
    
    def _calculate_overall_valuation(self, pe_analysis: Dict, pb_analysis: Dict) -> Dict:
        """Calculate overall valuation assessment"""
        pe_score = 1 if pe_analysis['status'] == 'UNDervalued' else 0 if pe_analysis['status'] == 'FAIR' else -1
        pb_score = 1 if pb_analysis['status'] == 'UNDervalued' else 0 if pb_analysis['status'] == 'FAIR' else -1
        
        total_score = pe_score + pb_score
        
        if total_score >= 1:
            return {'status': 'ATTRACTIVE', 'interpretation': 'Stock appears attractively valued'}
        elif total_score <= -1:
            return {'status': 'EXPENSIVE', 'interpretation': 'Stock appears expensive'}
        else:
            return {'status': 'FAIR', 'interpretation': 'Stock appears fairly valued'}
    
    def _calculate_overall_profitability(self, roe_analysis: Dict, profit_margin_analysis: Dict) -> Dict:
        """Calculate overall profitability assessment"""
        roe_score = 2 if roe_analysis['status'] == 'EXCELLENT' else 1 if roe_analysis['status'] == 'GOOD' else 0
        margin_score = 2 if profit_margin_analysis['status'] == 'EXCELLENT' else 1 if profit_margin_analysis['status'] == 'GOOD' else 0
        
        total_score = roe_score + margin_score
        
        if total_score >= 3:
            return {'status': 'EXCELLENT', 'interpretation': 'Company has excellent profitability'}
        elif total_score >= 2:
            return {'status': 'GOOD', 'interpretation': 'Company has good profitability'}
        elif total_score >= 1:
            return {'status': 'AVERAGE', 'interpretation': 'Company has average profitability'}
        else:
            return {'status': 'POOR', 'interpretation': 'Company has poor profitability'}
    
    def _calculate_overall_financial_health(self, dte_analysis: Dict, beta_analysis: Dict) -> Dict:
        """Calculate overall financial health assessment"""
        dte_score = 2 if dte_analysis['status'] == 'VERY_HEALTHY' else 1 if dte_analysis['status'] == 'HEALTHY' else 0
        risk_score = 2 if beta_analysis['status'] == 'LOW_RISK' else 1 if beta_analysis['status'] == 'AVERAGE' else 0
        
        total_score = dte_score + risk_score
        
        if total_score >= 3:
            return {'status': 'EXCELLENT', 'interpretation': 'Company has excellent financial health'}
        elif total_score >= 2:
            return {'status': 'GOOD', 'interpretation': 'Company has good financial health'}
        elif total_score >= 1:
            return {'status': 'AVERAGE', 'interpretation': 'Company has average financial health'}
        else:
            return {'status': 'POOR', 'interpretation': 'Company has poor financial health'}
    
    def _calculate_fundamental_score(self, analysis: Dict) -> Dict:
        """Calculate overall fundamental score (0-100)"""
        scores = []
        
        # Valuation score (0-25)
        valuation_status = analysis['valuation_analysis']['overall_valuation']['status']
        if valuation_status == 'ATTRACTIVE':
            scores.append(25)
        elif valuation_status == 'FAIR':
            scores.append(15)
        else:
            scores.append(5)
        
        # Profitability score (0-25)
        profitability_status = analysis['profitability_analysis']['overall_profitability']['status']
        if profitability_status == 'EXCELLENT':
            scores.append(25)
        elif profitability_status == 'GOOD':
            scores.append(20)
        elif profitability_status == 'AVERAGE':
            scores.append(15)
        else:
            scores.append(5)
        
        # Financial health score (0-25)
        health_status = analysis['financial_health_analysis']['overall_financial_health']['status']
        if health_status == 'EXCELLENT':
            scores.append(25)
        elif health_status == 'GOOD':
            scores.append(20)
        elif health_status == 'AVERAGE':
            scores.append(15)
        else:
            scores.append(5)
        
        # Dividend score (0-25)
        dividend_status = analysis['dividend_analysis']['status']
        if dividend_status in ['HIGH_YIELD', 'GOOD_YIELD']:
            scores.append(20)
        elif dividend_status == 'MODERATE_YIELD':
            scores.append(15)
        elif dividend_status == 'LOW_YIELD':
            scores.append(10)
        else:
            scores.append(5)
        
        total_score = sum(scores)
        
        return {
            'total_score': total_score,
            'grade': self._get_grade(total_score),
            'breakdown': {
                'valuation': scores[0],
                'profitability': scores[1],
                'financial_health': scores[2],
                'dividend': scores[3]
            }
        }
    
    def _get_grade(self, score: int) -> str:
        """Get letter grade based on score"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B+'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C+'
        elif score >= 40:
            return 'C'
        elif score >= 30:
            return 'D'
        else:
            return 'F'
    
    def _get_fundamental_recommendation(self, analysis: Dict) -> Dict:
        """Get fundamental recommendation based on analysis"""
        score = analysis['fundamental_score']['total_score']
        
        if score >= 80:
            recommendation = 'STRONG_BUY'
            reasoning = 'Excellent fundamentals with strong financial health and attractive valuation'
        elif score >= 70:
            recommendation = 'BUY'
            reasoning = 'Good fundamentals with solid financial metrics'
        elif score >= 60:
            recommendation = 'HOLD'
            reasoning = 'Average fundamentals, suitable for existing positions'
        elif score >= 40:
            recommendation = 'WEAK_HOLD'
            reasoning = 'Below average fundamentals, monitor closely'
        else:
            recommendation = 'SELL'
            reasoning = 'Poor fundamentals, consider reducing exposure'
        
        return {
            'recommendation': recommendation,
            'reasoning': reasoning,
            'score': score,
            'confidence': min(95, max(50, score))
        }