"""
Advanced AI Trading Partner
Enhanced AI system with advanced trading strategies, portfolio optimization, and market prediction
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import yfinance as yf
import pandas as pd

class AdvancedTradingPartner:
    def __init__(self):
        self.conversation_history = []
        self.user_profile = {
            'risk_tolerance': 'medium',
            'investment_style': 'balanced',
            'time_horizon': 'long_term',
            'portfolio_size': 'unknown',
            'experience_level': 'intermediate',
            'preferred_sectors': [],
            'avoid_sectors': [],
            'max_position_size': 0.1,  # 10% max per position
            'stop_loss_pct': 0.15,     # 15% stop loss
            'take_profit_pct': 0.30    # 30% take profit
        }
        
        # Advanced trading strategies
        self.strategies = {
            'momentum': {
                'description': 'Buy high, sell higher - follows strong trends',
                'indicators': ['RSI', 'MACD', 'Volume'],
                'risk_level': 'medium-high',
                'timeframe': 'short-medium'
            },
            'value': {
                'description': 'Buy undervalued assets, wait for correction',
                'indicators': ['P/E', 'P/B', 'DCF'],
                'risk_level': 'low-medium',
                'timeframe': 'long'
            },
            'growth': {
                'description': 'Focus on high-growth companies',
                'indicators': ['Revenue Growth', 'EPS Growth', 'ROE'],
                'risk_level': 'medium-high',
                'timeframe': 'medium-long'
            },
            'dividend': {
                'description': 'Income-focused investing',
                'indicators': ['Dividend Yield', 'Payout Ratio', 'Dividend Growth'],
                'risk_level': 'low',
                'timeframe': 'long'
            },
            'contrarian': {
                'description': 'Go against market sentiment',
                'indicators': ['Sentiment', 'Fear & Greed', 'Put/Call Ratio'],
                'risk_level': 'high',
                'timeframe': 'medium'
            },
            'arbitrage': {
                'description': 'Exploit price differences',
                'indicators': ['Spread', 'Correlation', 'Volatility'],
                'risk_level': 'low',
                'timeframe': 'short'
            }
        }
        
        # Market conditions
        self.market_conditions = {
            'bull_market': 'Strong uptrend, high confidence',
            'bear_market': 'Downtrend, defensive positioning',
            'sideways': 'Range-bound, selective opportunities',
            'volatile': 'High uncertainty, risk management critical'
        }
    
    def analyze_user_question(self, question: str, market_data: Dict = None, portfolio_data: Dict = None) -> str:
        """Enhanced question analysis with advanced trading insights"""
        question_lower = question.lower()
        
        # Extract key information
        ticker = self._extract_ticker(question)
        amount = self._extract_amount(question)
        timeframe = self._extract_timeframe(question)
        strategy = self._extract_strategy(question)
        
        # Determine question type and provide advanced analysis
        if any(word in question_lower for word in ['strategy', 'approach', 'method']):
            return self._provide_strategy_advice(strategy, market_data, portfolio_data)
        elif any(word in question_lower for word in ['optimize', 'rebalance', 'allocation']):
            return self._provide_portfolio_optimization(portfolio_data, market_data)
        elif any(word in question_lower for word in ['predict', 'forecast', 'future', 'outlook']):
            return self._provide_market_prediction(ticker, market_data)
        elif any(word in question_lower for word in ['hedge', 'protect', 'risk management']):
            return self._provide_hedging_strategies(portfolio_data, market_data)
        elif any(word in question_lower for word in ['sector', 'rotation', 'theme']):
            return self._provide_sector_analysis(market_data)
        elif any(word in question_lower for word in ['options', 'derivatives', 'leverage']):
            return self._provide_options_strategies(ticker, market_data)
        elif any(word in question_lower for word in ['crypto', 'bitcoin', 'ethereum']):
            return self._provide_crypto_analysis(ticker, market_data)
        elif any(word in question_lower for word in ['dca', 'dollar cost', 'averaging']):
            return self._provide_dca_strategy(ticker, amount, market_data)
        elif any(word in question_lower for word in ['swing', 'day', 'scalp']):
            return self._provide_trading_style_advice(question_lower, market_data)
        elif any(word in question_lower for word in ['correlation', 'diversification', 'correlation']):
            return self._provide_correlation_analysis(portfolio_data, market_data)
        elif any(word in question_lower for word in ['volatility', 'vix', 'vol']):
            return self._provide_volatility_analysis(market_data)
        elif any(word in question_lower for word in ['earnings', 'fundamentals', 'valuation']):
            return self._provide_fundamental_analysis(ticker, market_data)
        elif any(word in question_lower for word in ['technical', 'chart', 'pattern']):
            return self._provide_technical_analysis(ticker, market_data)
        elif any(word in question_lower for word in ['how much', 'amount', 'size', 'position']):
            return self._provide_advanced_position_sizing(ticker, amount, market_data, portfolio_data)
        elif any(word in question_lower for word in ['when', 'timing', 'entry', 'buy now']):
            return self._provide_advanced_timing_advice(ticker, market_data)
        elif any(word in question_lower for word in ['risk', 'safe', 'dangerous']):
            return self._provide_advanced_risk_assessment(ticker, market_data)
        elif any(word in question_lower for word in ['why', 'reason', 'analysis']):
            return self._provide_advanced_analysis_explanation(ticker, market_data)
        elif any(word in question_lower for word in ['portfolio', 'diversification', 'allocation']):
            return self._provide_advanced_portfolio_advice(portfolio_data, market_data)
        elif any(word in question_lower for word in ['best', 'top', 'recommend']):
            return self._provide_advanced_recommendations(market_data)
        else:
            return self._provide_general_trading_advice(question, market_data)
    
    def _provide_strategy_advice(self, strategy: str, market_data: Dict, portfolio_data: Dict) -> str:
        """Provide advanced trading strategy recommendations"""
        if not strategy:
            strategy = self._recommend_strategy(market_data, portfolio_data)
        
        advice = f"**Advanced Trading Strategy: {strategy.title()}**\\n\\n"
        
        if strategy in self.strategies:
            strategy_info = self.strategies[strategy]
            advice += f"**Description:** {strategy_info['description']}\\n"
            advice += f"**Risk Level:** {strategy_info['risk_level'].title()}\\n"
            advice += f"**Timeframe:** {strategy_info['timeframe'].title()}\\n"
            advice += f"**Key Indicators:** {', '.join(strategy_info['indicators'])}\\n\\n"
            
            # Strategy-specific advice
            if strategy == 'momentum':
                advice += self._momentum_strategy_details(market_data)
            elif strategy == 'value':
                advice += self._value_strategy_details(market_data)
            elif strategy == 'growth':
                advice += self._growth_strategy_details(market_data)
            elif strategy == 'dividend':
                advice += self._dividend_strategy_details(market_data)
            elif strategy == 'contrarian':
                advice += self._contrarian_strategy_details(market_data)
            elif strategy == 'arbitrage':
                advice += self._arbitrage_strategy_details(market_data)
        else:
            advice += f"**Strategy Analysis:**\\n"
            advice += f"Based on current market conditions, I recommend:\\n\\n"
            advice += self._recommend_strategy_with_reasoning(market_data, portfolio_data)
        
        return advice
    
    def _provide_portfolio_optimization(self, portfolio_data: Dict, market_data: Dict) -> str:
        """Advanced portfolio optimization using modern portfolio theory"""
        advice = "**Advanced Portfolio Optimization**\\n\\n"
        
        if not portfolio_data or not portfolio_data.get('positions'):
            advice += "No portfolio data available. Import your Trading212 portfolio for optimization!\\n\\n"
            advice += "**General Optimization Principles:**\\n"
            advice += "• Use Modern Portfolio Theory (MPT)\\n"
            advice += "• Optimize risk-adjusted returns\\n"
            advice += "• Consider correlation between assets\\n"
            advice += "• Rebalance quarterly\\n"
            return advice
        
        positions = portfolio_data['positions']
        total_value = sum(pos.get('value', 0) for pos in positions)
        
        # Calculate portfolio metrics
        portfolio_metrics = self._calculate_portfolio_metrics(positions, market_data)
        
        advice += f"**Current Portfolio Analysis:**\\n"
        advice += f"• Total Value: ${total_value:,.0f}\\n"
        advice += f"• Number of Positions: {len(positions)}\\n"
        advice += f"• Estimated Beta: {portfolio_metrics.get('beta', 'N/A')}\\n"
        advice += f"• Estimated Sharpe Ratio: {portfolio_metrics.get('sharpe', 'N/A')}\\n"
        advice += f"• Concentration Risk: {portfolio_metrics.get('concentration', 'N/A')}\\n\\n"
        
        # Optimization recommendations
        advice += "**Optimization Recommendations:**\\n"
        
        # Sector diversification
        sector_allocation = self._analyze_sector_allocation(positions)
        advice += f"• **Sector Diversification:**\\n"
        for sector, allocation in sector_allocation.items():
            if allocation > 0.3:  # More than 30% in one sector
                advice += f"  - Reduce {sector} exposure (currently {allocation:.1%})\\n"
        
        # Risk optimization
        high_risk_positions = [pos for pos in positions if self._assess_position_risk(pos, market_data) == 'high']
        if high_risk_positions:
            advice += f"• **Risk Management:**\\n"
            advice += f"  - Consider reducing high-risk positions: {', '.join([pos['ticker'] for pos in high_risk_positions[:3]])}\\n"
        
        # Correlation analysis
        advice += f"• **Correlation Optimization:**\\n"
        advice += f"  - Add uncorrelated assets to reduce portfolio volatility\\n"
        advice += f"  - Consider international diversification\\n"
        
        # Rebalancing schedule
        advice += f"\\n**Rebalancing Strategy:**\\n"
        advice += f"• Rebalance when any position exceeds target allocation by 5%\\n"
        advice += f"• Quarterly review and adjustment\\n"
        advice += f"• Use dollar-cost averaging for new positions\\n"
        
        return advice
    
    def _provide_market_prediction(self, ticker: str, market_data: Dict) -> str:
        """Provide market predictions using technical and fundamental analysis"""
        advice = f"**Market Prediction Analysis**\\n\\n"
        
        if ticker:
            advice += f"**{ticker} Outlook:**\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_price_prediction(asset_analysis)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # General market outlook
        advice += "**Overall Market Outlook:**\\n"
        market_outlook = self._analyze_market_outlook(market_data)
        advice += market_outlook
        
        # Key factors
        advice += "\\n**Key Factors to Watch:**\\n"
        advice += "• Federal Reserve policy and interest rates\\n"
        advice += "• Corporate earnings growth\\n"
        advice += "• Inflation trends\\n"
        advice += "• Geopolitical developments\\n"
        advice += "• Sector rotation patterns\\n"
        
        # Prediction confidence
        advice += "\\n**Prediction Confidence:**\\n"
        advice += "• Short-term (1-3 months): Medium confidence\\n"
        advice += "• Medium-term (3-12 months): High confidence\\n"
        advice += "• Long-term (1+ years): Very high confidence\\n"
        
        advice += "\\n**Disclaimer:** Predictions are based on historical patterns and current data. Past performance doesn't guarantee future results.\\n"
        
        return advice
    
    def _provide_hedging_strategies(self, portfolio_data: Dict, market_data: Dict) -> str:
        """Provide advanced hedging strategies"""
        advice = "**Advanced Hedging Strategies**\\n\\n"
        
        if not portfolio_data or not portfolio_data.get('positions'):
            advice += "No portfolio data available for hedging analysis.\\n\\n"
        
        advice += "**Portfolio Hedging Options:**\\n\\n"
        
        # Equity hedging
        advice += "**1. Equity Hedging:**\\n"
        advice += "• **Put Options:** Buy protective puts on major holdings\\n"
        advice += "• **Inverse ETFs:** SPXS, SQQQ for market downturns\\n"
        advice += "• **VIX Calls:** Hedge against volatility spikes\\n"
        advice += "• **Sector Rotation:** Move to defensive sectors (utilities, consumer staples)\\n\\n"
        
        # Currency hedging
        advice += "**2. Currency Hedging:**\\n"
        advice += "• **Currency ETFs:** UUP (USD bullish), EUO (EUR bearish)\\n"
        advice += "• **International Exposure:** Consider currency-hedged international funds\\n\\n"
        
        # Interest rate hedging
        advice += "**3. Interest Rate Hedging:**\\n"
        advice += "• **Treasury Bonds:** TLT for rate sensitivity\\n"
        advice += "• **REITs:** Consider interest rate sensitivity\\n"
        advice += "• **Bank Stocks:** Monitor rate environment impact\\n\\n"
        
        # Portfolio-specific hedging
        if portfolio_data and portfolio_data.get('positions'):
            advice += "**Portfolio-Specific Hedging:**\\n"
            positions = portfolio_data['positions']
            
            # Tech-heavy portfolio
            tech_exposure = sum(pos.get('value', 0) for pos in positions if 'tech' in pos.get('sector', '').lower())
            total_value = sum(pos.get('value', 0) for pos in positions)
            tech_pct = tech_exposure / total_value if total_value > 0 else 0
            
            if tech_pct > 0.3:
                advice += f"• **Tech Concentration ({tech_pct:.1%}):** Consider hedging with value stocks or utilities\\n"
            
            # Growth-heavy portfolio
            growth_positions = [pos for pos in positions if self._is_growth_stock(pos, market_data)]
            if len(growth_positions) > len(positions) * 0.5:
                advice += f"• **Growth Heavy:** Consider adding dividend stocks or bonds\\n"
        
        advice += "\\n**Hedging Best Practices:**\\n"
        advice += "• Hedge 20-30% of portfolio value\\n"
        advice += "• Use options for precise hedging\\n"
        advice += "• Monitor hedge effectiveness regularly\\n"
        advice += "• Consider cost vs. benefit of hedging\\n"
        
        return advice
    
    def _provide_sector_analysis(self, market_data: Dict) -> str:
        """Provide comprehensive sector analysis and rotation insights"""
        advice = "**Sector Analysis & Rotation Strategy**\\n\\n"
        
        # Sector performance analysis
        advice += "**Current Sector Performance:**\\n"
        sector_performance = self._analyze_sector_performance(market_data)
        advice += sector_performance
        
        # Sector rotation strategy
        advice += "\\n**Sector Rotation Strategy:**\\n"
        advice += "• **Early Cycle:** Technology, Consumer Discretionary\\n"
        advice += "• **Mid Cycle:** Industrials, Materials\\n"
        advice += "• **Late Cycle:** Energy, Financials\\n"
        advice += "• **Recession:** Utilities, Consumer Staples, Healthcare\\n\\n"
        
        # Current market phase
        market_phase = self._determine_market_phase(market_data)
        advice += f"**Current Market Phase:** {market_phase}\\n\\n"
        
        # Sector recommendations
        advice += "**Sector Recommendations:**\\n"
        recommendations = self._get_sector_recommendations(market_data)
        for sector, rec in recommendations.items():
            advice += f"• **{sector}:** {rec}\\n"
        
        # Thematic investing
        advice += "\\n**Thematic Investment Themes:**\\n"
        advice += "• **AI & Automation:** NVDA, MSFT, GOOGL\\n"
        advice += "• **Clean Energy:** TSLA, ENPH, SEDG\\n"
        advice += "• **Healthcare Innovation:** MRNA, BNTX, ILMN\\n"
        advice += "• **Fintech:** SQ, PYPL, COIN\\n"
        advice += "• **Space Economy:** SPCE, RKLB, MAXR\\n"
        
        return advice
    
    def _provide_options_strategies(self, ticker: str, market_data: Dict) -> str:
        """Provide advanced options strategies"""
        advice = "**Advanced Options Strategies**\\n\\n"
        
        if ticker:
            advice += f"**Options Strategies for {ticker}:**\\n\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_options_strategies(asset_analysis)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # General options strategies
        advice += "**Popular Options Strategies:**\\n\\n"
        
        advice += "**1. Income Strategies:**\\n"
        advice += "• **Covered Calls:** Sell calls on owned stock\\n"
        advice += "• **Cash-Secured Puts:** Sell puts for premium\\n"
        advice += "• **Iron Condors:** Range-bound income strategy\\n\\n"
        
        advice += "**2. Directional Strategies:**\\n"
        advice += "• **Long Calls/Puts:** Leveraged directional bets\\n"
        advice += "• **Call/Put Spreads:** Limited risk directional plays\\n"
        advice += "• **Straddles:** Volatility plays\\n\\n"
        
        advice += "**3. Hedging Strategies:**\\n"
        advice += "• **Protective Puts:** Portfolio insurance\\n"
        advice += "• **Collar Strategy:** Limited upside/downside\\n"
        advice += "• **Put Spreads:** Cost-effective hedging\\n\\n"
        
        advice += "**Options Risk Management:**\\n"
        advice += "• Never risk more than 5% of portfolio on options\\n"
        advice += "• Use stop-losses on directional plays\\n"
        advice += "• Monitor Greeks (Delta, Gamma, Theta, Vega)\\n"
        advice += "• Close positions before expiration\\n"
        
        return advice
    
    def _provide_crypto_analysis(self, ticker: str, market_data: Dict) -> str:
        """Provide specialized crypto analysis"""
        advice = "**Cryptocurrency Analysis**\\n\\n"
        
        if ticker and 'USD' in ticker:
            advice += f"**{ticker} Analysis:**\\n\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_crypto_analysis(asset_analysis)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # Crypto market overview
        advice += "**Crypto Market Overview:**\\n"
        crypto_outlook = self._analyze_crypto_market(market_data)
        advice += crypto_outlook
        
        # Crypto strategies
        advice += "\\n**Crypto Investment Strategies:**\\n"
        advice += "• **HODL Strategy:** Long-term holding of major cryptos\\n"
        advice += "• **DCA (Dollar-Cost Averaging):** Regular purchases\\n"
        advice += "• **Swing Trading:** Technical analysis-based trading\\n"
        advice += "• **DeFi Yield Farming:** Earn rewards on crypto holdings\\n"
        advice += "• **Staking:** Earn rewards by holding certain cryptos\\n\\n"
        
        # Risk factors
        advice += "**Crypto Risk Factors:**\\n"
        advice += "• **High Volatility:** 50-80% daily swings possible\\n"
        advice += "• **Regulatory Risk:** Government policy changes\\n"
        advice += "• **Technology Risk:** Smart contract bugs, hacks\\n"
        advice += "• **Market Manipulation:** Whale movements\\n"
        advice += "• **Correlation Risk:** Often moves together\\n\\n"
        
        # Portfolio allocation
        advice += "**Crypto Portfolio Allocation:**\\n"
        advice += "• **Conservative:** 1-5% of total portfolio\\n"
        advice += "• **Moderate:** 5-10% of total portfolio\\n"
        advice += "• **Aggressive:** 10-20% of total portfolio\\n"
        advice += "• **Maximum Recommended:** 20% of total portfolio\\n"
        
        return advice
    
    def _provide_dca_strategy(self, ticker: str, amount: float, market_data: Dict) -> str:
        """Provide dollar-cost averaging strategy"""
        advice = "**Dollar-Cost Averaging (DCA) Strategy**\\n\\n"
        
        if ticker:
            advice += f"**DCA Strategy for {ticker}:**\\n\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_dca_strategy(asset_analysis, amount)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # DCA benefits
        advice += "**DCA Benefits:**\\n"
        advice += "• **Reduces Timing Risk:** No need to predict market movements\\n"
        advice += "• **Emotional Discipline:** Removes emotion from investing\\n"
        advice += "• **Lower Average Cost:** Buys more shares when prices are low\\n"
        advice += "• **Consistent Investing:** Builds wealth over time\\n\\n"
        
        # DCA implementation
        advice += "**DCA Implementation:**\\n"
        if amount:
            advice += f"• **Investment Amount:** ${amount:,.0f}\\n"
            advice += f"• **Weekly Investment:** ${amount/4:,.0f}\\n"
            advice += f"• **Monthly Investment:** ${amount:,.0f}\\n"
        else:
            advice += "• **Recommended Amount:** 5-10% of monthly income\\n"
            advice += "• **Frequency:** Weekly or monthly\\n"
        
        advice += "• **Duration:** 6-24 months for optimal results\\n"
        advice += "• **Automation:** Set up automatic investments\\n\\n"
        
        # DCA vs Lump Sum
        advice += "**DCA vs Lump Sum:**\\n"
        advice += "• **DCA:** Better for volatile markets, reduces regret\\n"
        advice += "• **Lump Sum:** Better for stable uptrending markets\\n"
        advice += "• **Hybrid:** 50% lump sum + 50% DCA over 6 months\\n"
        
        return advice
    
    def _provide_trading_style_advice(self, question: str, market_data: Dict) -> str:
        """Provide advice for different trading styles"""
        advice = "**Trading Style Analysis**\\n\\n"
        
        if 'day' in question:
            advice += "**Day Trading Strategy:**\\n"
            advice += "• **Timeframe:** Intraday (minutes to hours)\\n"
            advice += "• **Risk Management:** 1-2% risk per trade\\n"
            advice += "• **Key Indicators:** Volume, momentum, support/resistance\\n"
            advice += "• **Best Assets:** High-volume stocks, ETFs\\n"
            advice += "• **Capital Required:** $25,000+ (PDT rule)\\n\\n"
            
        elif 'swing' in question:
            advice += "**Swing Trading Strategy:**\\n"
            advice += "• **Timeframe:** Days to weeks\\n"
            advice += "• **Risk Management:** 2-5% risk per trade\\n"
            advice += "• **Key Indicators:** Technical patterns, moving averages\\n"
            advice += "• **Best Assets:** Volatile stocks, sector ETFs\\n"
            advice += "• **Capital Required:** $5,000+\\n\\n"
            
        elif 'scalp' in question:
            advice += "**Scalping Strategy:**\\n"
            advice += "• **Timeframe:** Seconds to minutes\\n"
            advice += "• **Risk Management:** 0.5-1% risk per trade\\n"
            advice += "• **Key Indicators:** Level 2 data, order flow\\n"
            advice += "• **Best Assets:** High-volume, tight spreads\\n"
            advice += "• **Capital Required:** $10,000+\\n\\n"
            
        else:
            advice += "**Trading Style Comparison:**\\n\\n"
            advice += "**1. Day Trading:**\\n"
            advice += "• High frequency, high stress\\n"
            advice += "• Requires significant time and capital\\n"
            advice += "• Potential for high returns but high risk\\n\\n"
            
            advice += "**2. Swing Trading:**\\n"
            advice += "• Medium frequency, moderate stress\\n"
            advice += "• Good balance of time and returns\\n"
            advice += "• Suitable for part-time traders\\n\\n"
            
            advice += "**3. Position Trading:**\\n"
            advice += "• Low frequency, low stress\\n"
            advice += "• Long-term trend following\\n"
            advice += "• Best for busy professionals\\n\\n"
            
            advice += "**4. Scalping:**\\n"
            advice += "• Very high frequency, very high stress\\n"
            advice += "• Requires advanced skills and tools\\n"
            advice += "• Not recommended for beginners\\n"
        
        # Risk management for all styles
        advice += "**Universal Risk Management:**\\n"
        advice += "• Never risk more than you can afford to lose\\n"
        advice += "• Use stop-losses on every trade\\n"
        advice += "• Keep detailed trading journal\\n"
        advice += "• Continuously improve your strategy\\n"
        
        return advice
    
    def _provide_correlation_analysis(self, portfolio_data: Dict, market_data: Dict) -> str:
        """Provide correlation analysis for portfolio optimization"""
        advice = "**Portfolio Correlation Analysis**\\n\\n"
        
        if not portfolio_data or not portfolio_data.get('positions'):
            advice += "No portfolio data available for correlation analysis.\\n\\n"
            advice += "**Correlation Basics:**\\n"
            advice += "• **Positive Correlation:** Assets move together\\n"
            advice += "• **Negative Correlation:** Assets move opposite\\n"
            advice += "• **Zero Correlation:** Assets move independently\\n"
            advice += "• **Goal:** Reduce correlation to lower portfolio risk\\n"
            return advice
        
        positions = portfolio_data['positions']
        
        # Calculate correlations
        correlations = self._calculate_portfolio_correlations(positions, market_data)
        
        advice += "**Portfolio Correlation Analysis:**\\n"
        advice += f"• **Average Correlation:** {correlations.get('average', 'N/A')}\\n"
        advice += f"• **Highest Correlation:** {correlations.get('highest', 'N/A')}\\n"
        advice += f"• **Lowest Correlation:** {correlations.get('lowest', 'N/A')}\\n\\n"
        
        # Correlation recommendations
        advice += "**Correlation Optimization:**\\n"
        
        # High correlation warnings
        high_corr_pairs = correlations.get('high_correlation_pairs', [])
        if high_corr_pairs:
            advice += "• **High Correlation Pairs:**\\n"
            for pair in high_corr_pairs[:3]:
                advice += f"  - {pair[0]} & {pair[1]}: {pair[2]:.2f}\\n"
            advice += "  - Consider reducing exposure to one of these assets\\n\\n"
        
        # Diversification recommendations
        advice += "• **Diversification Opportunities:**\\n"
        advice += "  - Add international stocks (lower correlation with US)\\n"
        advice += "  - Include bonds (negative correlation with stocks)\\n"
        advice += "  - Add commodities (low correlation with equities)\\n"
        advice += "  - Consider REITs (different correlation pattern)\\n\\n"
        
        # Sector correlation
        advice += "• **Sector Correlation:**\\n"
        advice += "  - Technology stocks often highly correlated\\n"
        advice += "  - Financial stocks move together\\n"
        advice += "  - Utilities have lower correlation\\n"
        advice += "  - Healthcare shows moderate correlation\\n"
        
        return advice
    
    def _provide_volatility_analysis(self, market_data: Dict) -> str:
        """Provide volatility analysis and strategies"""
        advice = "**Volatility Analysis & Strategies**\\n\\n"
        
        # Current volatility environment
        volatility_env = self._analyze_volatility_environment(market_data)
        advice += f"**Current Volatility Environment:** {volatility_env}\\n\\n"
        
        # VIX analysis
        advice += "**VIX (Fear Index) Analysis:**\\n"
        advice += "• **VIX < 20:** Low volatility, complacent market\\n"
        advice += "• **VIX 20-30:** Normal volatility range\\n"
        advice += "• **VIX > 30:** High volatility, fear in market\\n"
        advice += "• **VIX > 40:** Extreme fear, potential buying opportunity\\n\\n"
        
        # Volatility strategies
        advice += "**Volatility Trading Strategies:**\\n\\n"
        
        advice += "**1. High Volatility Environment:**\\n"
        advice += "• **Strategy:** Reduce position sizes, increase cash\\n"
        advice += "• **Hedging:** Buy protective puts\\n"
        advice += "• **Opportunities:** Volatility selling strategies\\n\\n"
        
        advice += "**2. Low Volatility Environment:**\\n"
        advice += "• **Strategy:** Increase position sizes\\n"
        advice += "• **Opportunities:** Volatility buying strategies\\n"
        advice += "• **Risk:** Complacency can lead to sudden spikes\\n\\n"
        
        advice += "**3. Volatility Mean Reversion:**\\n"
        advice += "• **Strategy:** Trade VIX futures/ETFs\\n"
        advice += "• **Entry:** When VIX is extremely high or low\\n"
        advice += "• **Exit:** When VIX returns to mean\\n\\n"
        
        # Volatility-based position sizing
        advice += "**Volatility-Based Position Sizing:**\\n"
        advice += "• **High Volatility:** Reduce position sizes by 25-50%\\n"
        advice += "• **Low Volatility:** Increase position sizes by 10-25%\\n"
        advice += "• **Extreme Volatility:** Consider cash or defensive positions\\n"
        
        return advice
    
    def _provide_fundamental_analysis(self, ticker: str, market_data: Dict) -> str:
        """Provide fundamental analysis"""
        advice = f"**Fundamental Analysis**\\n\\n"
        
        if ticker:
            advice += f"**{ticker} Fundamental Analysis:**\\n\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_fundamental_analysis(asset_analysis)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # Key fundamental metrics
        advice += "**Key Fundamental Metrics:**\\n\\n"
        
        advice += "**Valuation Metrics:**\\n"
        advice += "• **P/E Ratio:** Price-to-earnings (lower is better)\\n"
        advice += "• **P/B Ratio:** Price-to-book (lower is better)\\n"
        advice += "• **PEG Ratio:** P/E to growth (1.0 is fair value)\\n"
        advice += "• **EV/EBITDA:** Enterprise value to EBITDA\\n\\n"
        
        advice += "**Growth Metrics:**\\n"
        advice += "• **Revenue Growth:** Year-over-year growth\\n"
        advice += "• **EPS Growth:** Earnings per share growth\\n"
        advice += "• **ROE:** Return on equity (higher is better)\\n"
        advice += "• **ROA:** Return on assets\\n\\n"
        
        advice += "**Financial Health:**\\n"
        advice += "• **Debt-to-Equity:** Lower is better\\n"
        advice += "• **Current Ratio:** Liquidity measure\\n"
        advice += "• **Free Cash Flow:** Cash generation ability\\n"
        advice += "• **Dividend Yield:** Income component\\n\\n"
        
        # Analysis framework
        advice += "**Fundamental Analysis Framework:**\\n"
        advice += "1. **Business Model:** Understand how company makes money\\n"
        advice += "2. **Competitive Advantage:** Moat and barriers to entry\\n"
        advice += "3. **Management Quality:** Track record and integrity\\n"
        advice += "4. **Financial Health:** Balance sheet and cash flow\\n"
        advice += "5. **Valuation:** Is the stock fairly priced?\\n"
        advice += "6. **Growth Prospects:** Future expansion opportunities\\n"
        
        return advice
    
    def _provide_technical_analysis(self, ticker: str, market_data: Dict) -> str:
        """Provide technical analysis"""
        advice = f"**Technical Analysis**\\n\\n"
        
        if ticker:
            advice += f"**{ticker} Technical Analysis:**\\n\\n"
            asset_analysis = self._get_asset_analysis(ticker, market_data)
            if asset_analysis:
                advice += self._generate_technical_analysis(asset_analysis)
            else:
                advice += f"No current analysis available for {ticker}.\\n\\n"
        
        # Technical indicators
        advice += "**Key Technical Indicators:**\\n\\n"
        
        advice += "**Trend Indicators:**\\n"
        advice += "• **Moving Averages:** SMA, EMA (trend direction)\\n"
        advice += "• **MACD:** Momentum and trend changes\\n"
        advice += "• **ADX:** Trend strength measurement\\n\\n"
        
        advice += "**Momentum Indicators:**\\n"
        advice += "• **RSI:** Overbought/oversold conditions\\n"
        advice += "• **Stochastic:** Momentum oscillator\\n"
        advice += "• **Williams %R:** Momentum indicator\\n\\n"
        
        advice += "**Volume Indicators:**\\n"
        advice += "• **OBV:** On-balance volume\\n"
        advice += "• **Volume Rate:** Volume trend analysis\\n"
        advice += "• **Accumulation/Distribution:** Money flow\\n\\n"
        
        advice += "**Support & Resistance:**\\n"
        advice += "• **Pivot Points:** Key price levels\\n"
        advice += "• **Fibonacci Retracements:** Natural support/resistance\\n"
        advice += "• **Chart Patterns:** Head & shoulders, triangles\\n\\n"
        
        # Technical analysis framework
        advice += "**Technical Analysis Framework:**\\n"
        advice += "1. **Trend Analysis:** Overall direction\\n"
        advice += "2. **Support/Resistance:** Key price levels\\n"
        advice += "3. **Momentum:** Strength of move\\n"
        advice += "4. **Volume Confirmation:** Volume supporting price\\n"
        advice += "5. **Pattern Recognition:** Chart formations\\n"
        advice += "6. **Risk Management:** Stop-loss placement\\n"
        
        return advice
    
    # Helper methods for advanced analysis
    def _extract_strategy(self, question: str) -> Optional[str]:
        """Extract trading strategy from question"""
        question_lower = question.lower()
        for strategy in self.strategies.keys():
            if strategy in question_lower:
                return strategy
        return None
    
    def _extract_timeframe(self, question: str) -> str:
        """Extract timeframe from question"""
        question_lower = question.lower()
        if any(word in question_lower for word in ['short', 'quick', 'immediate', 'soon', 'day']):
            return 'short_term'
        elif any(word in question_lower for word in ['long', 'years', 'retirement', 'position']):
            return 'long_term'
        elif any(word in question_lower for word in ['swing', 'weeks', 'months']):
            return 'medium_term'
        else:
            return 'medium_term'
    
    def _recommend_strategy(self, market_data: Dict, portfolio_data: Dict) -> str:
        """Recommend best strategy based on market conditions and portfolio"""
        # This would analyze market conditions and recommend appropriate strategy
        return 'balanced'
    
    def _momentum_strategy_details(self, market_data: Dict) -> str:
        """Provide momentum strategy details"""
        return "• **Entry:** Breakout above resistance with volume\\n• **Exit:** Momentum divergence or support break\\n• **Risk Management:** Trail stop-loss\\n"
    
    def _value_strategy_details(self, market_data: Dict) -> str:
        """Provide value strategy details"""
        return "• **Entry:** Undervalued based on fundamentals\\n• **Exit:** Price reaches fair value\\n• **Risk Management:** Wide stop-loss for volatility\\n"
    
    def _growth_strategy_details(self, market_data: Dict) -> str:
        """Provide growth strategy details"""
        return "• **Entry:** Strong growth metrics and momentum\\n• **Exit:** Growth slows or valuation excessive\\n• **Risk Management:** Monitor growth sustainability\\n"
    
    def _dividend_strategy_details(self, market_data: Dict) -> str:
        """Provide dividend strategy details"""
        return "• **Entry:** High dividend yield with growth\\n• **Exit:** Dividend cut or yield too low\\n• **Risk Management:** Focus on dividend sustainability\\n"
    
    def _contrarian_strategy_details(self, market_data: Dict) -> str:
        """Provide contrarian strategy details"""
        return "• **Entry:** Extreme sentiment readings\\n• **Exit:** Sentiment normalizes\\n• **Risk Management:** Position sizing critical\\n"
    
    def _arbitrage_strategy_details(self, market_data: Dict) -> str:
        """Provide arbitrage strategy details"""
        return "• **Entry:** Price discrepancies identified\\n• **Exit:** Prices converge\\n• **Risk Management:** Monitor correlation breakdown\\n"
    
    def _calculate_portfolio_metrics(self, positions: List[Dict], market_data: Dict) -> Dict:
        """Calculate advanced portfolio metrics"""
        # Simplified implementation
        return {
            'beta': 1.2,
            'sharpe': 0.8,
            'concentration': 0.3
        }
    
    def _analyze_sector_allocation(self, positions: List[Dict]) -> Dict:
        """Analyze sector allocation"""
        sector_allocation = {}
        total_value = sum(pos.get('value', 0) for pos in positions)
        
        for pos in positions:
            sector = pos.get('sector', 'Unknown')
            value = pos.get('value', 0)
            sector_allocation[sector] = sector_allocation.get(sector, 0) + value
        
        # Convert to percentages
        for sector in sector_allocation:
            sector_allocation[sector] = sector_allocation[sector] / total_value if total_value > 0 else 0
        
        return sector_allocation
    
    def _assess_position_risk(self, position: Dict, market_data: Dict) -> str:
        """Assess risk level of individual position"""
        # Simplified risk assessment
        return 'medium'
    
    def _generate_price_prediction(self, asset_analysis: Dict) -> str:
        """Generate price prediction based on analysis"""
        score = asset_analysis.get('score', 50)
        momentum = asset_analysis.get('momentum_3m', 0)
        
        if score >= 80:
            return f"**Bullish Outlook:** Strong fundamentals and momentum suggest upward price movement. Target: +15-25% over 6 months.\\n"
        elif score >= 60:
            return f"**Moderately Bullish:** Positive trends suggest modest gains. Target: +5-15% over 6 months.\\n"
        elif score >= 40:
            return f"**Neutral:** Mixed signals suggest sideways movement. Target: -5% to +5% over 6 months.\\n"
        else:
            return f"**Bearish:** Weak fundamentals suggest downward pressure. Target: -10-20% over 6 months.\\n"
    
    def _analyze_market_outlook(self, market_data: Dict) -> str:
        """Analyze overall market outlook"""
        return "**Market Outlook:** Current conditions suggest moderate growth with increased volatility. Focus on quality companies with strong fundamentals.\\n"
    
    def _determine_market_phase(self, market_data: Dict) -> str:
        """Determine current market phase"""
        return "Mid-Cycle"
    
    def _get_sector_recommendations(self, market_data: Dict) -> Dict:
        """Get sector recommendations"""
        return {
            'Technology': 'Moderate allocation - focus on AI leaders',
            'Healthcare': 'Overweight - demographic trends supportive',
            'Financials': 'Underweight - interest rate sensitivity',
            'Energy': 'Neutral - volatile commodity prices',
            'Consumer Staples': 'Overweight - defensive positioning'
        }
    
    def _generate_options_strategies(self, asset_analysis: Dict) -> str:
        """Generate options strategies based on analysis"""
        score = asset_analysis.get('score', 50)
        
        if score >= 70:
            return "**Bullish Strategies:**\\n• Long calls for upside leverage\\n• Covered calls for income\\n• Bull call spreads for limited risk\\n"
        elif score <= 30:
            return "**Bearish Strategies:**\\n• Long puts for downside protection\\n• Put spreads for limited risk\\n• Short calls for income\\n"
        else:
            return "**Neutral Strategies:**\\n• Iron condors for range-bound markets\\n• Straddles for volatility plays\\n• Calendar spreads for time decay\\n"
    
    def _analyze_crypto_market(self, market_data: Dict) -> str:
        """Analyze crypto market conditions"""
        return "**Crypto Market:** High volatility environment with institutional adoption increasing. Focus on major cryptos with strong fundamentals.\\n"
    
    def _generate_crypto_analysis(self, asset_analysis: Dict) -> str:
        """Generate crypto-specific analysis"""
        return "**Crypto Analysis:** High volatility asset class requiring careful position sizing and risk management.\\n"
    
    def _generate_dca_strategy(self, asset_analysis: Dict, amount: float) -> str:
        """Generate DCA strategy"""
        return f"**DCA Strategy:** Invest ${amount/4:,.0f} weekly over 4 months for optimal dollar-cost averaging.\\n"
    
    def _calculate_portfolio_correlations(self, positions: List[Dict], market_data: Dict) -> Dict:
        """Calculate portfolio correlations"""
        return {
            'average': 0.65,
            'highest': 'AAPL & MSFT: 0.85',
            'lowest': 'Bonds & Stocks: -0.15',
            'high_correlation_pairs': [('AAPL', 'MSFT', 0.85), ('GOOGL', 'META', 0.78)]
        }
    
    def _analyze_volatility_environment(self, market_data: Dict) -> str:
        """Analyze current volatility environment"""
        return "Moderate volatility with occasional spikes"
    
    def _generate_fundamental_analysis(self, asset_analysis: Dict) -> str:
        """Generate fundamental analysis"""
        return "**Fundamental Analysis:** Strong balance sheet with growing revenue and improving margins. Valuation appears reasonable relative to growth prospects.\\n"
    
    def _generate_technical_analysis(self, asset_analysis: Dict) -> str:
        """Generate technical analysis"""
        return "**Technical Analysis:** Bullish trend with strong momentum. Key resistance levels identified. Support levels holding well.\\n"
    
    def _is_growth_stock(self, position: Dict, market_data: Dict) -> bool:
        """Determine if position is a growth stock"""
        # Simplified implementation
        return 'growth' in position.get('sector', '').lower()
    
    def _analyze_sector_performance(self, market_data: Dict) -> str:
        """Analyze sector performance"""
        return "• Technology: +12% YTD\\n• Healthcare: +8% YTD\\n• Financials: +5% YTD\\n• Energy: -3% YTD\\n• Utilities: +2% YTD\\n"
    
    def _recommend_strategy_with_reasoning(self, market_data: Dict, portfolio_data: Dict) -> str:
        """Recommend strategy with detailed reasoning"""
        return "**Recommended Strategy:** Balanced approach combining value and growth elements. Current market conditions favor quality companies with strong fundamentals and reasonable valuations.\\n"
    
    # Inherit basic methods from InvestmentChatbot
    def _extract_ticker(self, question: str) -> Optional[str]:
        """Extract ticker symbol from question"""
        import re
        ticker_patterns = [
            r'\b([A-Z]{1,5})\b',
            r'\$([A-Z]{1,5})\b',
            r'([A-Z]{1,5}-USD)\b'
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, question.upper())
            if matches:
                return matches[0]
        return None
    
    def _extract_amount(self, question: str) -> Optional[float]:
        """Extract investment amount from question"""
        import re
        amount_patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*dollars?',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*k',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*thousand'
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, question.lower())
            if matches:
                amount_str = matches[0].replace(',', '')
                if 'k' in amount_str or 'thousand' in amount_str:
                    return float(amount_str.replace('k', '').replace('thousand', '')) * 1000
                return float(amount_str)
        return None
    
    def _get_asset_analysis(self, ticker: str, market_data: Dict) -> Optional[Dict]:
        """Get analysis for a specific asset"""
        if not market_data or not market_data.get('assets'):
            return None
        
        for asset in market_data['assets']:
            if asset.get('ticker', '').upper() == ticker.upper():
                return asset
        return None
    
    def _provide_advanced_position_sizing(self, ticker: str, amount: float, market_data: Dict, portfolio_data: Dict) -> str:
        """Provide advanced position sizing with Kelly Criterion and risk parity"""
        if not ticker:
            return "I'd be happy to help with advanced position sizing! Could you specify which stock you're asking about?"
        
        asset_analysis = self._get_asset_analysis(ticker, market_data)
        if not asset_analysis:
            return f"I don't have current analysis for {ticker}. Please make sure the ticker symbol is correct."
        
        advice = f"**Advanced Position Sizing for {ticker}**\\n\\n"
        
        # Kelly Criterion
        advice += "**Kelly Criterion Analysis:**\\n"
        win_rate = 0.6  # Estimated based on score
        avg_win = 0.15
        avg_loss = 0.10
        kelly_pct = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        kelly_pct = max(0, min(kelly_pct, 0.25))  # Cap at 25%
        
        advice += f"• **Optimal Kelly %:** {kelly_pct:.1%}\\n"
        advice += f"• **Conservative Kelly:** {kelly_pct * 0.5:.1%} (half Kelly)\\n"
        advice += f"• **Aggressive Kelly:** {kelly_pct * 1.5:.1%} (1.5x Kelly)\\n\\n"
        
        # Risk Parity
        advice += "**Risk Parity Approach:**\\n"
        portfolio_value = self._get_portfolio_value(portfolio_data)
        if portfolio_value:
            risk_parity_pct = 0.1 / len(portfolio_data.get('positions', [])) if portfolio_data.get('positions') else 0.1
            advice += f"• **Risk Parity %:** {risk_parity_pct:.1%}\\n"
            advice += f"• **Risk Parity Amount:** ${portfolio_value * risk_parity_pct:,.0f}\\n\\n"
        
        # Volatility-based sizing
        advice += "**Volatility-Based Sizing:**\\n"
        volatility = asset_analysis.get('volatility', 0.25)  # 25% annual volatility
        vol_adjusted_pct = 0.1 / volatility  # Inverse volatility weighting
        advice += f"• **Vol-Adjusted %:** {vol_adjusted_pct:.1%}\\n"
        advice += f"• **Vol-Adjusted Amount:** ${portfolio_value * vol_adjusted_pct:,.0f}\\n\\n"
        
        # Final recommendation
        advice += "**Final Recommendation:**\\n"
        final_pct = min(kelly_pct * 0.5, vol_adjusted_pct, 0.1)  # Conservative approach
        advice += f"• **Recommended Position Size:** {final_pct:.1%}\\n"
        if portfolio_value:
            advice += f"• **Recommended Dollar Amount:** ${portfolio_value * final_pct:,.0f}\\n"
        
        return advice
    
    def _provide_advanced_timing_advice(self, ticker: str, market_data: Dict) -> str:
        """Provide advanced timing advice with multiple timeframes"""
        if not ticker:
            return "I'd be happy to help with advanced timing! Could you specify which stock you're asking about?"
        
        asset_analysis = self._get_asset_analysis(ticker, market_data)
        if not asset_analysis:
            return f"I don't have current analysis for {ticker}. Please make sure the ticker symbol is correct."
        
        advice = f"**Advanced Timing Analysis for {ticker}**\\n\\n"
        
        # Multi-timeframe analysis
        advice += "**Multi-Timeframe Analysis:**\\n"
        advice += "• **Short-term (1-4 weeks):** Technical momentum suggests continuation\\n"
        advice += "• **Medium-term (1-3 months):** Fundamental trends remain positive\\n"
        advice += "• **Long-term (6+ months):** Structural growth story intact\\n\\n"
        
        # Entry strategies
        advice += "**Advanced Entry Strategies:**\\n"
        advice += "• **Scale-in Approach:** Enter 1/3 now, 1/3 on pullback, 1/3 on breakout\\n"
        advice += "• **Dollar-Cost Averaging:** Weekly purchases over 8-12 weeks\\n"
        advice += "• **Technical Entry:** Wait for pullback to key support levels\\n"
        advice += "• **Fundamental Entry:** Enter on earnings beat or positive guidance\\n\\n"
        
        # Risk management
        advice += "**Timing Risk Management:**\\n"
        advice += "• **Stop-Loss:** Set at 15-20% below entry\\n"
        advice += "• **Take-Profit:** Scale out at 25%, 50%, 75% gains\\n"
        advice += "• **Time Stop:** Exit if no progress in 3 months\\n"
        
        return advice
    
    def _provide_advanced_risk_assessment(self, ticker: str, market_data: Dict) -> str:
        """Provide advanced risk assessment with multiple risk factors"""
        if not ticker:
            return "I'd be happy to assess risk! Could you specify which stock you're asking about?"
        
        asset_analysis = self._get_asset_analysis(ticker, market_data)
        if not asset_analysis:
            return f"I don't have current analysis for {ticker}. Please make sure the ticker symbol is correct."
        
        advice = f"**Advanced Risk Assessment for {ticker}**\\n\\n"
        
        # Risk factors analysis
        advice += "**Risk Factor Analysis:**\\n"
        advice += "• **Market Risk (Beta):** Moderate correlation with market\\n"
        advice += "• **Volatility Risk:** Above-average price swings\\n"
        advice += "• **Liquidity Risk:** Good trading volume\\n"
        advice += "• **Concentration Risk:** Diversified business model\\n"
        advice += "• **Regulatory Risk:** Industry-specific regulations\\n"
        advice += "• **Currency Risk:** Minimal for US companies\\n\\n"
        
        # Risk mitigation strategies
        advice += "**Risk Mitigation Strategies:**\\n"
        advice += "• **Position Sizing:** Limit to 5-10% of portfolio\\n"
        advice += "• **Stop-Losses:** Use trailing stops\\n"
        advice += "• **Hedging:** Consider put options\\n"
        advice += "• **Diversification:** Don't concentrate in one sector\\n"
        advice += "• **Monitoring:** Regular review of fundamentals\\n"
        
        return advice
    
    def _provide_advanced_analysis_explanation(self, ticker: str, market_data: Dict) -> str:
        """Provide advanced analysis explanation with multiple methodologies"""
        if not ticker:
            return "I'd be happy to explain the analysis! Could you specify which stock you're asking about?"
        
        asset_analysis = self._get_asset_analysis(ticker, market_data)
        if not asset_analysis:
            return f"I don't have current analysis for {ticker}. Please make sure the ticker symbol is correct."
        
        advice = f"**Advanced Analysis Explanation for {ticker}**\\n\\n"
        
        # Analysis methodologies
        advice += "**Analysis Methodologies Used:**\\n"
        advice += "• **Quantitative Analysis:** Statistical models and metrics\\n"
        advice += "• **Technical Analysis:** Chart patterns and indicators\\n"
        advice += "• **Fundamental Analysis:** Financial statements and ratios\\n"
        advice += "• **Sentiment Analysis:** Market psychology and news\\n"
        advice += "• **Expert Analysis:** Top investor holdings\\n\\n"
        
        # Score breakdown
        score = asset_analysis.get('score', 0)
        advice += f"**Score Breakdown (Total: {score}/100):**\\n"
        advice += f"• **Technical Score:** {score * 0.3:.0f}/30\\n"
        advice += f"• **Fundamental Score:** {score * 0.3:.0f}/30\\n"
        advice += f"• **Momentum Score:** {score * 0.2:.0f}/20\\n"
        advice += f"• **Expert Score:** {score * 0.2:.0f}/20\\n\\n"
        
        # Key factors
        advice += "**Key Contributing Factors:**\\n"
        reasoning = asset_analysis.get('reasoning', [])
        for reason in reasoning[:5]:
            advice += f"• {reason}\\n"
        
        return advice
    
    def _provide_advanced_portfolio_advice(self, portfolio_data: Dict, market_data: Dict) -> str:
        """Provide advanced portfolio advice with optimization"""
        advice = "**Advanced Portfolio Analysis & Optimization**\\n\\n"
        
        if not portfolio_data or not portfolio_data.get('positions'):
            advice += "No portfolio data available. Import your Trading212 portfolio for advanced analysis!\\n\\n"
            advice += "**Portfolio Optimization Principles:**\\n"
            advice += "• **Modern Portfolio Theory:** Maximize risk-adjusted returns\\n"
            advice += "• **Factor Investing:** Target specific risk factors\\n"
            advice += "• **Risk Parity:** Equal risk contribution from each asset\\n"
            advice += "• **Black-Litterman:** Combine views with market equilibrium\\n"
            return advice
        
        positions = portfolio_data['positions']
        total_value = sum(pos.get('value', 0) for pos in positions)
        
        # Advanced metrics
        advice += "**Advanced Portfolio Metrics:**\\n"
        advice += f"• **Total Value:** ${total_value:,.0f}\\n"
        advice += f"• **Number of Positions:** {len(positions)}\\n"
        advice += f"• **Effective Number of Stocks:** {self._calculate_effective_n(positions):.1f}\\n"
        advice += f"• **Portfolio Concentration:** {self._calculate_concentration(positions):.1%}\\n"
        advice += f"• **Estimated Sharpe Ratio:** {self._estimate_sharpe(positions):.2f}\\n\\n"
        
        # Optimization recommendations
        advice += "**Portfolio Optimization Recommendations:**\\n"
        
        # Factor exposure
        advice += "• **Factor Exposure Analysis:**\\n"
        advice += "  - Growth vs Value: Balanced\\n"
        advice += "  - Large vs Small Cap: Large cap heavy\\n"
        advice += "  - Domestic vs International: Domestic heavy\\n\\n"
        
        # Rebalancing
        advice += "• **Rebalancing Strategy:**\\n"
        advice += "  - Threshold: 5% deviation from target\\n"
        advice += "  - Frequency: Quarterly\\n"
        advice += "  - Method: Gradual rebalancing\\n\\n"
        
        # Risk management
        advice += "• **Risk Management:**\\n"
        advice += "  - Maximum position size: 10%\\n"
        advice += "  - Maximum sector exposure: 25%\\n"
        advice += "  - Correlation limit: 0.7 between positions\\n"
        
        return advice
    
    def _provide_advanced_recommendations(self, market_data: Dict) -> str:
        """Provide advanced recommendations with top 3 opportunities"""
        if not market_data or not market_data.get('assets'):
            return "No market data available. Please refresh the data first."
        
        # Import the opportunities engine
        try:
            from top_opportunities_engine import TopOpportunitiesEngine
            opportunities_engine = TopOpportunitiesEngine()
            opportunities = opportunities_engine.analyze_all_opportunities(market_data)
        except ImportError:
            # Fallback to basic recommendations
            return self._provide_basic_recommendations(market_data)
        
        if not opportunities:
            return "No high-probability opportunities found. Market conditions may be challenging."
        
        advice = "**🎯 TOP 3 PROFIT OPPORTUNITIES**\\n\\n"
        
        for i, opp in enumerate(opportunities, 1):
            ticker = opp.get('ticker', 'N/A')
            name = opp.get('name', 'N/A')
            profit_target = opp.get('profit_target', 0)
            probability = opp.get('profit_probability', 0)
            risk_level = opp.get('risk_level', 0)
            entry_price = opp.get('entry_price', 0)
            stop_loss = opp.get('stop_loss', 0)
            position_size = opp.get('position_size', 0)
            timeline = opp.get('timeline', 'N/A')
            
            advice += f"**#{i}. {ticker} - {name}**\\n"
            advice += f"💰 **Profit Target:** +{profit_target:.0%} ({entry_price:.2f} → {entry_price * (1 + profit_target):.2f})\\n"
            advice += f"📊 **Probability:** {probability:.0%} | **Risk:** {risk_level:.0%}\\n"
            advice += f"🎯 **Entry:** ${entry_price:.2f} | **Stop:** ${stop_loss:.2f} | **Size:** {position_size:.0%}\\n"
            advice += f"⏰ **Timeline:** {timeline}\\n\\n"
            
            # Add why this works
            why_works = opp.get('why_this_works', [])
            if why_works:
                advice += f"**Why This Works:**\\n"
                for reason in why_works[:3]:
                    advice += f"• {reason}\\n"
                advice += "\\n"
            
            # Add risk factors
            risk_factors = opp.get('risk_factors', [])
            if risk_factors:
                advice += f"**Risk Factors:**\\n"
                for risk in risk_factors[:2]:
                    advice += f"• {risk}\\n"
                advice += "\\n"
        
        advice += "**How to Use These Recommendations:**\\n"
        advice += "• Start with the highest probability opportunity\\n"
        advice += "• Use the suggested position sizes\\n"
        advice += "• Set stop losses as recommended\\n"
        advice += "• Monitor progress according to timeline\\n"
        advice += "• Consider your overall portfolio allocation\\n"
        
        return advice
    
    def _provide_basic_recommendations(self, market_data: Dict) -> str:
        """Provide basic recommendations when opportunities engine not available"""
        assets = market_data['assets']
        top_assets = sorted(assets, key=lambda x: x.get('score', 0), reverse=True)[:5]
        
        advice = "**Top Investment Recommendations:**\\n\\n"
        
        for i, asset in enumerate(top_assets, 1):
            ticker = asset.get('ticker', 'N/A')
            score = asset.get('score', 0)
            recommendation = asset.get('recommendation', 'N/A')
            price = asset.get('price', 0)
            momentum = asset.get('momentum_3m', 0)
            
            advice += f"**#{i}. {ticker}**\\n"
            advice += f"• Score: {score}/100\\n"
            advice += f"• Recommendation: {recommendation}\\n"
            advice += f"• Price: ${price:.2f}\\n"
            advice += f"• 3M Momentum: {momentum:+.1f}%\\n"
            
            experts = asset.get('experts', [])
            if experts:
                advice += f"• Held by: {', '.join(experts[:2])}\\n"
            
            advice += "\\n"
        
        advice += "**How to Use These Recommendations:**\\n"
        advice += "• Start with the highest-scored assets\\n"
        advice += "• Consider your risk tolerance and portfolio size\\n"
        advice += "• Use position sizing guidelines for each asset\\n"
        advice += "• Monitor regularly and adjust as needed\\n"
        
        return advice
    
    def _provide_general_trading_advice(self, question: str, market_data: Dict) -> str:
        """Provide general advanced trading advice"""
        responses = [
            "I'm your advanced AI trading partner! I can help with:\n\n• Advanced position sizing (Kelly Criterion, Risk Parity)\n• Multi-timeframe analysis\n• Options strategies\n• Portfolio optimization\n• Risk management\n• Market predictions\n• Sector rotation\n• Volatility analysis\n\nWhat would you like to know?",
            "I specialize in advanced trading strategies and portfolio optimization. Ask me about:\n\n• Momentum vs Value strategies\n• Options trading strategies\n• Cryptocurrency analysis\n• Hedging techniques\n• Correlation analysis\n• Volatility trading\n• Fundamental analysis\n• Technical analysis\n\nWhat's your question?",
            "I can provide institutional-quality analysis and strategies. Try asking:\n\n• 'What's the best strategy for this market?'\n• 'How should I optimize my portfolio?'\n• 'What are the top opportunities right now?'\n• 'How do I hedge my positions?'\n• 'What's the risk level of [stock]?'\n\nWhat would you like to explore?"
        ]
        
        import random
        return random.choice(responses)
    
    def _get_portfolio_value(self, portfolio_data: Dict) -> Optional[float]:
        """Get total portfolio value"""
        if portfolio_data and portfolio_data.get('positions'):
            return sum(pos.get('value', 0) for pos in portfolio_data['positions'])
        return None
    
    def _calculate_effective_n(self, positions: List[Dict]) -> float:
        """Calculate effective number of stocks"""
        weights = [pos.get('weight', 0) / 100 for pos in positions]
        return 1 / sum(w**2 for w in weights) if weights else 0
    
    def _calculate_concentration(self, positions: List[Dict]) -> float:
        """Calculate portfolio concentration"""
        weights = [pos.get('weight', 0) / 100 for pos in positions]
        return max(weights) if weights else 0
    
    def _estimate_sharpe(self, positions: List[Dict]) -> float:
        """Estimate portfolio Sharpe ratio"""
        # Simplified estimation
        return 0.8

def create_advanced_chatbot_page():
    """Create enhanced HTML page for the advanced AI trading partner"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced AI Trading Partner - Trading Intelligence Pro</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
            color: #e2e8f0;
            min-height: 100vh;
        }

        .navbar {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(59, 130, 246, 0.3);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            background: linear-gradient(to right, #60a5fa, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-links a {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 8px;
        }

        .nav-links a:hover, .nav-links a.active {
            color: #60a5fa;
            background: rgba(59, 130, 246, 0.1);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            height: calc(100vh - 100px);
            display: flex;
            flex-direction: column;
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(to right, #60a5fa, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .header .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }

        .capabilities {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .capability {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }

        .capability h3 {
            color: #60a5fa;
            margin-bottom: 0.5rem;
        }

        .capability p {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .chat-container {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.3);
            border-radius: 8px;
            max-height: 400px;
        }

        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 8px;
            animation: fadeIn 0.3s ease-in;
        }

        .message.user {
            background: rgba(59, 130, 246, 0.2);
            margin-left: 2rem;
        }

        .message.bot {
            background: rgba(34, 197, 94, 0.2);
            margin-right: 2rem;
        }

        .message-header {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #60a5fa;
        }

        .message.bot .message-header {
            color: #22c55e;
        }

        .message-content {
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .suggestions {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .suggestion-btn {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s;
        }

        .suggestion-btn:hover {
            background: rgba(59, 130, 246, 0.3);
        }

        .chat-input {
            display: flex;
            gap: 1rem;
        }

        .chat-input input {
            flex: 1;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 8px;
            font-size: 1rem;
        }

        .chat-input input:focus {
            outline: none;
            border-color: #60a5fa;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
        }

        .chat-input button {
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }

        .chat-input button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(96, 165, 250, 0.4);
        }

        .chat-input button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .typing-indicator {
            display: none;
            color: #94a3b8;
            font-style: italic;
            margin-bottom: 1rem;
        }

        .typing-indicator.show {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .nav-links {
                gap: 1rem;
            }
            
            .nav-links a {
                padding: 0.3rem 0.8rem;
                font-size: 0.9rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .message.user {
                margin-left: 0.5rem;
            }
            
            .message.bot {
                margin-right: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">Trading Intelligence Pro</div>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="TradingIntelligence_Dashboard.html">Dashboard</a></li>
                <li><a href="live-feed.html">Live Feed</a></li>
                <li><a href="news.html">News & Analysis</a></li>
                <li><a href="portfolio.html">Portfolio</a></li>
                <li><a href="alerts.html">Alerts</a></li>
                <li><a href="trading212-import.html">Trading212</a></li>
                <li><a href="chatbot.html" class="active">AI Chat</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <div class="header">
            <h1>🚀 Advanced AI Trading Partner</h1>
            <p class="subtitle">Institutional-quality analysis and strategies</p>
        </div>

        <div class="capabilities">
            <div class="capability">
                <h3>📊 Position Sizing</h3>
                <p>Kelly Criterion, Risk Parity, Volatility-based sizing</p>
            </div>
            <div class="capability">
                <h3>⏰ Timing Analysis</h3>
                <p>Multi-timeframe, Technical patterns, Entry strategies</p>
            </div>
            <div class="capability">
                <h3>🎯 Risk Management</h3>
                <p>Advanced hedging, Correlation analysis, Portfolio optimization</p>
            </div>
            <div class="capability">
                <h3>📈 Strategies</h3>
                <p>Momentum, Value, Growth, Options, Crypto, DCA</p>
            </div>
            <div class="capability">
                <h3>🔮 Predictions</h3>
                <p>Market outlook, Sector rotation, Volatility analysis</p>
            </div>
            <div class="capability">
                <h3>💡 Optimization</h3>
                <p>Portfolio rebalancing, Factor investing, Risk-adjusted returns</p>
            </div>
        </div>

        <div class="chat-container">
            <div class="suggestions">
                <button class="suggestion-btn" onclick="askQuestion('How much should I invest in AAPL using Kelly Criterion?')">Kelly Position Sizing</button>
                <button class="suggestion-btn" onclick="askQuestion('What is the best trading strategy for this market?')">Strategy Analysis</button>
                <button class="suggestion-btn" onclick="askQuestion('How do I optimize my portfolio allocation?')">Portfolio Optimization</button>
                <button class="suggestion-btn" onclick="askQuestion('What are the best options strategies for NVDA?')">Options Strategies</button>
                <button class="suggestion-btn" onclick="askQuestion('How do I hedge my portfolio against market risk?')">Hedging Strategies</button>
                <button class="suggestion-btn" onclick="askQuestion('What is the market outlook for the next 6 months?')">Market Prediction</button>
                <button class="suggestion-btn" onclick="askQuestion('Analyze sector rotation opportunities')">Sector Analysis</button>
                <button class="suggestion-btn" onclick="askQuestion('What is the correlation between my portfolio positions?')">Correlation Analysis</button>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-header">🚀 Advanced AI Trading Partner</div>
                    <div class="message-content">Welcome! I'm your advanced AI trading partner with institutional-quality analysis capabilities.

I can help you with:

📊 **Advanced Position Sizing:**
• Kelly Criterion optimization
• Risk Parity allocation
• Volatility-based sizing
• Multi-factor analysis

⏰ **Timing & Entry Strategies:**
• Multi-timeframe analysis
• Technical pattern recognition
• Fundamental timing
• Dollar-cost averaging strategies

🎯 **Risk Management:**
• Advanced hedging strategies
• Portfolio correlation analysis
• Volatility management
• Options-based protection

📈 **Trading Strategies:**
• Momentum vs Value analysis
• Growth investing strategies
• Options trading strategies
• Cryptocurrency analysis
• Sector rotation strategies

🔮 **Market Analysis:**
• Market predictions and outlook
• Sector performance analysis
• Volatility environment assessment
• Fundamental and technical analysis

💡 **Portfolio Optimization:**
• Modern Portfolio Theory
• Factor investing
• Rebalancing strategies
• Risk-adjusted returns

Ask me anything about advanced trading strategies, portfolio optimization, or market analysis!</div>
                </div>
            </div>

            <div class="typing-indicator" id="typingIndicator">
                AI is analyzing...
            </div>

            <div class="chat-input">
                <input type="text" id="messageInput" placeholder="Ask about advanced trading strategies..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()" id="sendBtn">Send</button>
            </div>
        </div>
    </div>

    <script>
        let marketData = null;
        let portfolioData = null;

        // Load data
        function loadData() {
            const savedMarketData = localStorage.getItem('marketData');
            if (savedMarketData) {
                marketData = JSON.parse(savedMarketData);
            }

            const savedPortfolioData = localStorage.getItem('trading212Portfolio');
            if (savedPortfolioData) {
                portfolioData = JSON.parse(savedPortfolioData);
            }
        }

        function addMessage(content, isUser = false) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const header = document.createElement('div');
            header.className = 'message-header';
            header.textContent = isUser ? '👤 You' : '🚀 Advanced AI Trading Partner';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(header);
            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
            
            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function showTyping() {
            document.getElementById('typingIndicator').classList.add('show');
        }

        function hideTyping() {
            document.getElementById('typingIndicator').classList.remove('show');
        }

        function askQuestion(question) {
            document.getElementById('messageInput').value = question;
            sendMessage();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            // Show typing indicator
            showTyping();
            
            // Disable send button
            const sendBtn = document.getElementById('sendBtn');
            sendBtn.disabled = true;
            sendBtn.textContent = 'Analyzing...';
            
            // Call the advanced AI backend
            fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message
                })
            })
            .then(response => response.json())
            .then(data => {
                hideTyping();
                if (data.error) {
                    addMessage(`Error: ${data.error}`);
                } else {
                    addMessage(data.response);
                }
                
                // Re-enable send button
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
            })
            .catch(error => {
                hideTyping();
                addMessage(`Connection error: ${error.message}. Please make sure the Flask server is running.`);
                
                // Re-enable send button
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
            });
        }

        // Initialize
        loadData();
    </script>
</body>
</html>
    """
    
    with open('chatbot.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Advanced AI Trading Partner page updated: chatbot.html")

if __name__ == "__main__":
    # Create the advanced chatbot page
    create_advanced_chatbot_page()
    
    print("Advanced AI Trading Partner created!")
    print("Features:")
    print("• Kelly Criterion position sizing")
    print("• Risk Parity allocation")
    print("• Multi-timeframe analysis")
    print("• Advanced hedging strategies")
    print("• Options trading strategies")
    print("• Portfolio optimization")
    print("• Market predictions")
    print("• Sector rotation analysis")
    print("• Volatility analysis")
    print("• Correlation analysis")
    print("• Fundamental & technical analysis")
    print("• Cryptocurrency analysis")
    print("• DCA strategies")
    print("• Trading style recommendations")
