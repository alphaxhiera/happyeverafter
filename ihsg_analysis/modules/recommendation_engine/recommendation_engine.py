import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

class RecommendationEngine:
    """Module for generating investment recommendations and actionable insights"""
    
    def __init__(self):
        self.risk_profiles = {
            'conservative': {
                'max_position_size': 0.05,  # 5% per stock
                'stop_loss': 0.08,         # 8% stop loss
                'take_profit': 0.15,       # 15% take profit
                'max_portfolio_risk': 0.10, # 10% max portfolio risk
                'min_score': 70            # Minimum fundamental score
            },
            'moderate': {
                'max_position_size': 0.08,  # 8% per stock
                'stop_loss': 0.10,         # 10% stop loss
                'take_profit': 0.20,       # 20% take profit
                'max_portfolio_risk': 0.15, # 15% max portfolio risk
                'min_score': 60            # Minimum fundamental score
            },
            'aggressive': {
                'max_position_size': 0.12,  # 12% per stock
                'stop_loss': 0.15,         # 15% stop loss
                'take_profit': 0.30,       # 30% take profit
                'max_portfolio_risk': 0.20, # 20% max portfolio risk
                'min_score': 50            # Minimum fundamental score
            }
        }
    
    def generate_comprehensive_recommendation(self, technical_analysis: Dict, 
                                            fundamental_analysis: Dict,
                                            risk_profile: str = 'moderate') -> Dict:
        """
        Generate comprehensive investment recommendation
        
        Args:
            technical_analysis: Technical analysis results
            fundamental_analysis: Fundamental analysis results
            risk_profile: Risk profile ('conservative', 'moderate', 'aggressive')
        
        Returns:
            Dictionary with comprehensive recommendation
        """
        # Get risk profile settings
        risk_settings = self.risk_profiles.get(risk_profile, self.risk_profiles['moderate'])
        
        # Extract key signals
        technical_signal = technical_analysis.get('signal_analysis', {}).get('signal', 'HOLD')
        technical_confidence = technical_analysis.get('signal_analysis', {}).get('confidence', 50)
        trend = technical_analysis.get('trend_analysis', {}).get('trend', 'NEUTRAL')
        
        fundamental_score = fundamental_analysis.get('fundamental_score', {}).get('total_score', 50)
        fundamental_recommendation = fundamental_analysis.get('fundamental_recommendation', {}).get('recommendation', 'HOLD')
        
        # Calculate combined score
        combined_score = self._calculate_combined_score(technical_analysis, fundamental_analysis)
        
        # Generate final recommendation
        final_recommendation = self._get_final_recommendation(
            technical_signal, fundamental_recommendation, combined_score, risk_settings
        )
        
        # Calculate position sizing and risk management
        risk_management = self._calculate_risk_management(
            technical_analysis, fundamental_analysis, risk_settings
        )
        
        # Generate actionable insights
        insights = self._generate_actionable_insights(
            technical_analysis, fundamental_analysis, final_recommendation
        )
        
        return {
            'recommendation': final_recommendation,
            'combined_score': combined_score,
            'technical_signal': technical_signal,
            'technical_confidence': technical_confidence,
            'fundamental_score': fundamental_score,
            'fundamental_recommendation': fundamental_recommendation,
            'trend': trend,
            'risk_management': risk_management,
            'actionable_insights': insights,
            'risk_profile': risk_profile,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _calculate_combined_score(self, technical_analysis: Dict, fundamental_analysis: Dict) -> Dict:
        """Calculate combined technical and fundamental score"""
        # Technical score (0-100)
        tech_signal = technical_analysis.get('signal_analysis', {}).get('signal', 'HOLD')
        tech_confidence = technical_analysis.get('signal_analysis', {}).get('confidence', 50)
        trend_strength = technical_analysis.get('trend_analysis', {}).get('strength', 50)
        
        # Convert signal to score
        if tech_signal == 'BUY':
            tech_signal_score = 75
        elif tech_signal == 'SELL':
            tech_signal_score = 25
        else:
            tech_signal_score = 50
        
        technical_score = (tech_signal_score + tech_confidence + trend_strength) / 3
        
        # Fundamental score (0-100)
        fundamental_score = fundamental_analysis.get('fundamental_score', {}).get('total_score', 50)
        
        # Weight the scores (fundamental gets higher weight for long-term decisions)
        combined_score = (technical_score * 0.4) + (fundamental_score * 0.6)
        
        return {
            'technical_score': round(technical_score, 2),
            'fundamental_score': round(fundamental_score, 2),
            'combined_score': round(combined_score, 2),
            'grade': self._get_score_grade(combined_score)
        }
    
    def _get_final_recommendation(self, technical_signal: str, fundamental_rec: str, 
                                combined_score: float, risk_settings: Dict) -> Dict:
        """Determine final recommendation based on all factors"""
        # Check minimum fundamental score requirement
        fundamental_score = combined_score  # Simplified for this example
        
        if fundamental_score < risk_settings['min_score']:
            return {
                'action': 'AVOID',
                'reason': 'Fundamental quality below minimum threshold',
                'confidence': 90,
                'time_horizon': 'N/A'
            }
        
        # Determine recommendation based on combined analysis
        if combined_score >= 80:
            action = 'STRONG_BUY'
            reason = 'Excellent technical and fundamental indicators'
            confidence = min(95, combined_score)
            time_horizon = '6-12 months'
        elif combined_score >= 70:
            action = 'BUY'
            reason = 'Good technical and fundamental indicators'
            confidence = min(85, combined_score + 10)
            time_horizon = '3-6 months'
        elif combined_score >= 60:
            action = 'HOLD'
            reason = 'Average indicators, maintain current position'
            confidence = 70
            time_horizon = '1-3 months'
        elif combined_score >= 40:
            action = 'WEAK_HOLD'
            reason = 'Below average indicators, consider reducing'
            confidence = 60
            time_horizon = '1 month'
        else:
            action = 'SELL'
            reason = 'Poor indicators, consider exiting'
            confidence = min(85, 100 - combined_score + 10)
            time_horizon = 'Immediate'
        
        # Adjust based on signal alignment
        if (technical_signal == 'BUY' and fundamental_rec in ['BUY', 'STRONG_BUY']) or \
           (technical_signal == 'SELL' and fundamental_rec == 'SELL'):
            confidence = min(95, confidence + 10)
        elif (technical_signal == 'BUY' and fundamental_rec == 'SELL') or \
             (technical_signal == 'SELL' and fundamental_rec in ['BUY', 'STRONG_BUY']):
            confidence = max(40, confidence - 15)
            reason += ' (Conflicting signals detected)'
        
        return {
            'action': action,
            'reason': reason,
            'confidence': round(confidence, 1),
            'time_horizon': time_horizon
        }
    
    def _calculate_risk_management(self, technical_analysis: Dict, 
                                  fundamental_analysis: Dict, 
                                  risk_settings: Dict) -> Dict:
        """Calculate risk management parameters"""
        # Get current price and targets from technical analysis
        price_targets = technical_analysis.get('price_targets', {})
        current_price = price_targets.get('current_price', 0)
        
        if current_price == 0:
            return {}
        
        # Calculate stop loss and take profit levels
        atr = price_targets.get('atr', current_price * 0.02)
        
        stop_loss = current_price * (1 - risk_settings['stop_loss'])
        take_profit = current_price * (1 + risk_settings['take_profit'])
        
        # Use technical levels if available
        if 'stop_loss' in price_targets:
            stop_loss = max(stop_loss, price_targets['stop_loss'])
        
        if 'take_profit_1' in price_targets:
            take_profit = min(take_profit, price_targets['take_profit_1'])
        
        # Calculate position size
        max_position_value = risk_settings['max_position_size']
        
        # Risk/reward ratio
        risk_amount = current_price - stop_loss
        reward_amount = take_profit - current_price
        risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0
        
        return {
            'entry_price': current_price,
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'max_position_size': f"{max_position_value * 100:.1f}%",
            'risk_amount': round(risk_amount, 2),
            'reward_amount': round(reward_amount, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'atr': round(atr, 2),
            'position_sizing': self._calculate_position_sizing(risk_settings, risk_reward_ratio)
        }
    
    def _calculate_position_sizing(self, risk_settings: Dict, risk_reward_ratio: float) -> Dict:
        """Calculate recommended position sizing"""
        base_size = risk_settings['max_position_size']
        
        # Adjust position size based on risk/reward ratio
        if risk_reward_ratio >= 3:
            size_multiplier = 1.2  # Increase position for excellent R/R
        elif risk_reward_ratio >= 2:
            size_multiplier = 1.0  # Normal position
        elif risk_reward_ratio >= 1.5:
            size_multiplier = 0.8  # Reduce position for marginal R/R
        else:
            size_multiplier = 0.5  # Significantly reduce for poor R/R
        
        recommended_size = base_size * size_multiplier
        
        return {
            'recommended_size': f"{recommended_size * 100:.1f}%",
            'size_multiplier': size_multiplier,
            'reasoning': self._get_position_sizing_reasoning(risk_reward_ratio)
        }
    
    def _get_position_sizing_reasoning(self, risk_reward_ratio: float) -> str:
        """Get reasoning for position sizing"""
        if risk_reward_ratio >= 3:
            return "Excellent risk/reward ratio justifies larger position"
        elif risk_reward_ratio >= 2:
            return "Good risk/reward ratio supports normal position size"
        elif risk_reward_ratio >= 1.5:
            return "Moderate risk/reward ratio suggests smaller position"
        else:
            return "Poor risk/reward ratio requires significantly reduced position"
    
    def _generate_actionable_insights(self, technical_analysis: Dict, 
                                    fundamental_analysis: Dict,
                                    recommendation: Dict) -> List[Dict]:
        """Generate actionable insights and recommendations"""
        insights = []
        
        # Technical insights
        trend_analysis = technical_analysis.get('trend_analysis', {})
        signal_analysis = technical_analysis.get('signal_analysis', {})
        sr_levels = technical_analysis.get('support_resistance', {})
        
        # Trend insights
        trend = trend_analysis.get('trend', 'NEUTRAL')
        if trend == 'BULLISH':
            insights.append({
                'type': 'TECHNICAL',
                'insight': 'Uptrend detected with positive momentum',
                'action': 'Consider buying on dips',
                'priority': 'HIGH'
            })
        elif trend == 'BEARISH':
            insights.append({
                'type': 'TECHNICAL',
                'insight': 'Downtrend detected with negative momentum',
                'action': 'Consider selling on rallies or avoid',
                'priority': 'HIGH'
            })
        
        # Signal insights
        signals = signal_analysis.get('signals', [])
        if 'RSI_OVERSOLD' in signals:
            insights.append({
                'type': 'TECHNICAL',
                'insight': 'RSI indicates oversold conditions',
                'action': 'Potential reversal opportunity',
                'priority': 'MEDIUM'
            })
        elif 'RSI_OVERBOUGHT' in signals:
            insights.append({
                'type': 'TECHNICAL',
                'insight': 'RSI indicates overbought conditions',
                'action': 'Consider taking profits',
                'priority': 'MEDIUM'
            })
        
        # Support/Resistance insights
        if sr_levels.get('nearest_resistance'):
            insights.append({
                'type': 'TECHNICAL',
                'insight': f"Nearest resistance at {sr_levels['nearest_resistance']}",
                'action': 'Watch for potential reversal at resistance',
                'priority': 'MEDIUM'
            })
        
        if sr_levels.get('nearest_support'):
            insights.append({
                'type': 'TECHNICAL',
                'insight': f"Nearest support at {sr_levels['nearest_support']}",
                'action': 'Consider buying near support levels',
                'priority': 'MEDIUM'
            })
        
        # Fundamental insights
        valuation = fundamental_analysis.get('valuation_analysis', {})
        profitability = fundamental_analysis.get('profitability_analysis', {})
        financial_health = fundamental_analysis.get('financial_health_analysis', {})
        
        # Valuation insights
        overall_valuation = valuation.get('overall_valuation', {})
        if overall_valuation.get('status') == 'ATTRACTIVE':
            insights.append({
                'type': 'FUNDAMENTAL',
                'insight': 'Stock appears attractively valued',
                'action': 'Good entry point for long-term investors',
                'priority': 'HIGH'
            })
        elif overall_valuation.get('status') == 'EXPENSIVE':
            insights.append({
                'type': 'FUNDAMENTAL',
                'insight': 'Stock appears expensive',
                'action': 'Wait for better entry price',
                'priority': 'MEDIUM'
            })
        
        # Profitability insights
        overall_profitability = profitability.get('overall_profitability', {})
        if overall_profitability.get('status') == 'EXCELLENT':
            insights.append({
                'type': 'FUNDAMENTAL',
                'insight': 'Company has excellent profitability',
                'action': 'Strong candidate for long-term holding',
                'priority': 'HIGH'
            })
        
        # Financial health insights
        overall_health = financial_health.get('overall_financial_health', {})
        if overall_health.get('status') == 'EXCELLENT':
            insights.append({
                'type': 'FUNDAMENTAL',
                'insight': 'Company has excellent financial health',
                'action': 'Lower risk profile suitable for conservative investors',
                'priority': 'HIGH'
            })
        elif overall_health.get('status') == 'POOR':
            insights.append({
                'type': 'FUNDAMENTAL',
                'insight': 'Company has poor financial health',
                'action': 'Higher risk, requires careful monitoring',
                'priority': 'HIGH'
            })
        
        # Recommendation-specific insights
        action = recommendation.get('action', 'HOLD')
        if action in ['BUY', 'STRONG_BUY']:
            insights.append({
                'type': 'RECOMMENDATION',
                'insight': 'Analysis supports buying opportunity',
                'action': f"Consider position sizing based on {recommendation.get('risk_profile', 'moderate')} risk profile",
                'priority': 'HIGH'
            })
        elif action == 'SELL':
            insights.append({
                'type': 'RECOMMENDATION',
                'insight': 'Analysis suggests selling',
                'action': 'Consider reducing or exiting position',
                'priority': 'HIGH'
            })
        
        return insights
    
    def _get_score_grade(self, score: float) -> str:
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
    
    def generate_portfolio_recommendations(self, stocks_analysis: List[Dict], 
                                        total_capital: float,
                                        risk_profile: str = 'moderate') -> Dict:
        """
        Generate portfolio-level recommendations
        
        Args:
            stocks_analysis: List of individual stock analyses
            total_capital: Total investment capital
            risk_profile: Risk profile
        
        Returns:
            Dictionary with portfolio recommendations
        """
        risk_settings = self.risk_profiles.get(risk_profile, self.risk_profiles['moderate'])
        
        # Filter stocks based on minimum score
        qualified_stocks = [
            stock for stock in stocks_analysis 
            if stock.get('combined_score', {}).get('combined_score', 0) >= risk_settings['min_score']
        ]
        
        # Sort by combined score
        qualified_stocks.sort(key=lambda x: x.get('combined_score', {}).get('combined_score', 0), reverse=True)
        
        # Calculate portfolio allocations
        portfolio_recommendations = []
        remaining_capital = total_capital
        
        for stock in qualified_stocks:
            if remaining_capital <= 0:
                break
            
            # Calculate position size
            max_position = total_capital * risk_settings['max_position_size']
            position_size = min(max_position, remaining_capital)
            
            if position_size > 0:
                portfolio_recommendations.append({
                    'ticker': stock.get('ticker', 'UNKNOWN'),
                    'recommendation': stock.get('recommendation', {}),
                    'position_size': position_size,
                    'position_percentage': (position_size / total_capital) * 100,
                    'combined_score': stock.get('combined_score', {}).get('combined_score', 0)
                })
                remaining_capital -= position_size
        
        return {
            'portfolio_recommendations': portfolio_recommendations,
            'total_allocated': total_capital - remaining_capital,
            'remaining_capital': remaining_capital,
            'number_of_positions': len(portfolio_recommendations),
            'risk_profile': risk_profile,
            'diversification_score': self._calculate_diversification_score(portfolio_recommendations)
        }
    
    def _calculate_diversification_score(self, portfolio_recommendations: List[Dict]) -> Dict:
        """Calculate portfolio diversification metrics"""
        if not portfolio_recommendations:
            return {'score': 0, 'status': 'No positions'}
        
        # Calculate concentration
        max_position = max(rec['position_percentage'] for rec in portfolio_recommendations)
        number_of_positions = len(portfolio_recommendations)
        
        # Diversification score (0-100)
        if max_position <= 5 and number_of_positions >= 15:
            score = 100
            status = 'Excellent'
        elif max_position <= 8 and number_of_positions >= 10:
            score = 80
            status = 'Good'
        elif max_position <= 12 and number_of_positions >= 7:
            score = 60
            status = 'Moderate'
        elif max_position <= 15 and number_of_positions >= 5:
            score = 40
            status = 'Poor'
        else:
            score = 20
            status = 'Very Poor'
        
        return {
            'score': score,
            'status': status,
            'max_position': max_position,
            'number_of_positions': number_of_positions,
            'recommendation': 'Consider adding more positions' if number_of_positions < 10 else 'Good diversification'
        }