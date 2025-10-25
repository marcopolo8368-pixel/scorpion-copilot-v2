"""
Flask Backend API for Scorpion Copilot
Provides real-time data updates, alerts, and portfolio management
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List
import threading
import time

app = Flask(__name__)
CORS(app)

# Import our existing trading intelligence backend
try:
    from scorpion_backend import (
        UNIVERSE, ALL_TICKERS, analyze_asset, run_live_analysis,
        get_urgent_signals, get_news_feed, fetch_chart_data
    )
except ImportError:
    # Fallback if scorpion_backend doesn't exist
    UNIVERSE = {}
    ALL_TICKERS = []
    def analyze_asset(ticker): return {}
    def run_live_analysis(): return {}
    def get_urgent_signals(): return []
    def get_news_feed(): return []
    def fetch_chart_data(ticker): return {}

# Import AI chatbot
try:
    from advanced_ai_trading_partner import AdvancedTradingPartner
    from top_opportunities_engine import TopOpportunitiesEngine
    chatbot = AdvancedTradingPartner()
    opportunities_engine = TopOpportunitiesEngine()
except ImportError:
    # Fallback if modules don't exist
    class AdvancedTradingPartner:
        def analyze_user_question(self, question, market_data, portfolio_data):
            return "AI chatbot not available. Please check the installation."
    
    class TopOpportunitiesEngine:
        def analyze_all_opportunities(self, market_data):
            return []
    
    chatbot = AdvancedTradingPartner()
    opportunities_engine = TopOpportunitiesEngine()

# Global data storage
market_data = {}
portfolio_data = {}
alerts_data = []
news_data = []

def update_market_data():
    """Update market data (called on-demand for Vercel)"""
    global market_data, news_data
    
    try:
        print("Updating market data...")
        
        # Run analysis on a larger sample for better coverage
        sample_size = min(200, len(ALL_TICKERS))
        results = run_live_analysis(sample_size=sample_size)
        
        # Store the results
        market_data = {
            'timestamp': datetime.now().isoformat(),
            'assets': results,
            'total_analyzed': len(results)
        }
        
        # Update news data
        news_data = get_news_feed()
        
        # Save to file for the standalone dashboard
        with open('live_trading_signals.json', 'w') as f:
            json.dump(market_data, f, indent=2)
        
        print(f"Updated {len(results)} assets")
        return True
        
    except Exception as e:
        print(f"Error updating market data: {e}")
        return False

def start_background_tasks():
    """Start background data update tasks (disabled for Vercel)"""
    # Background tasks disabled for Vercel deployment
    # Data will be updated on-demand via API calls
    pass

# API Routes

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/api/market-data')
def get_market_data():
    """Get current market data"""
    global market_data
    
    # If no data available, try to load from file or initialize
    if not market_data:
        try:
            # Try to load from file first
            with open('live_trading_signals.json', 'r') as f:
                market_data = json.load(f)
        except:
            # If no file, initialize with empty data
            market_data = {
                'timestamp': datetime.now().isoformat(),
                'assets': [],
                'total_analyzed': 0
            }
    
    return jsonify(market_data)

@app.route('/api/urgent-signals')
def get_urgent_signals_api():
    """Get urgent investment signals"""
    if not market_data:
        return jsonify({'error': 'No data available'}), 404
    
    threshold = request.args.get('threshold', 85, type=float)
    urgent = get_urgent_signals(market_data['assets'], threshold)
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'signals': urgent,
        'count': len(urgent)
    })

@app.route('/api/news')
def get_news_api():
    """Get latest market news"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'news': news_data
    })

@app.route('/api/asset/<ticker>')
def get_asset_details(ticker):
    """Get detailed analysis for a specific asset"""
    try:
        analysis = analyze_asset(ticker)
        if analysis:
            return jsonify(analysis)
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/<ticker>')
def get_chart_data(ticker):
    """Get chart data for a specific asset"""
    timeframe = request.args.get('timeframe', '1m')
    
    try:
        chart_data = fetch_chart_data(ticker, timeframe)
        if chart_data:
            return jsonify(chart_data)
        else:
            return jsonify({'error': 'Chart data not available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET', 'POST'])
def portfolio_api():
    """Portfolio management API"""
    global portfolio_data
    
    if request.method == 'GET':
        return jsonify(portfolio_data)
    
    elif request.method == 'POST':
        data = request.json
        action = data.get('action')
        
        if action == 'add_position':
            ticker = data.get('ticker')
            shares = data.get('shares')
            price = data.get('price')
            
            if not all([ticker, shares, price]):
                return jsonify({'error': 'Missing required fields'}), 400
            
            if 'positions' not in portfolio_data:
                portfolio_data['positions'] = []
            
            portfolio_data['positions'].append({
                'ticker': ticker,
                'shares': shares,
                'price': price,
                'added_at': datetime.now().isoformat()
            })
            
            return jsonify({'success': True, 'message': 'Position added'})
        
        elif action == 'remove_position':
            ticker = data.get('ticker')
            if 'positions' in portfolio_data:
                portfolio_data['positions'] = [
                    p for p in portfolio_data['positions'] 
                    if p['ticker'] != ticker
                ]
            
            return jsonify({'success': True, 'message': 'Position removed'})
        
        return jsonify({'error': 'Invalid action'}), 400

@app.route('/api/alerts', methods=['GET', 'POST', 'DELETE'])
def alerts_api():
    """Alerts management API"""
    global alerts_data
    
    if request.method == 'GET':
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'alerts': alerts_data
        })
    
    elif request.method == 'POST':
        data = request.json
        alert = {
            'id': len(alerts_data) + 1,
            'ticker': data.get('ticker'),
            'type': data.get('type'),
            'threshold': data.get('threshold'),
            'priority': data.get('priority', 'normal'),
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        alerts_data.append(alert)
        return jsonify({'success': True, 'alert': alert})
    
    elif request.method == 'DELETE':
        alert_id = request.args.get('id', type=int)
        alerts_data = [a for a in alerts_data if a['id'] != alert_id]
        return jsonify({'success': True, 'message': 'Alert deleted'})

@app.route('/api/search')
def search_assets():
    """Search for assets"""
    query = request.args.get('q', '').upper()
    if not query:
        return jsonify({'assets': []})
    
    # Search in our universe
    matching_assets = []
    for sector, tickers in UNIVERSE.items():
        for ticker in tickers:
            if query in ticker.upper():
                matching_assets.append({
                    'ticker': ticker,
                    'sector': sector.replace('_', ' ').title()
                })
    
    return jsonify({
        'query': query,
        'assets': matching_assets[:20]  # Limit to 20 results
    })

@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    if not market_data:
        return jsonify({'error': 'No data available'}), 404
    
    assets = market_data['assets']
    strong_buys = len([a for a in assets if a['recommendation'] == 'STRONG BUY'])
    buys = len([a for a in assets if 'BUY' in a['recommendation']])
    sells = len([a for a in assets if 'SELL' in a['recommendation']])
    
    return jsonify({
        'total_assets': len(assets),
        'total_universe': len(ALL_TICKERS),
        'strong_buys': strong_buys,
        'buys': buys,
        'sells': sells,
        'active_alerts': len([a for a in alerts_data if a.get('active', True)]),
        'last_update': market_data['timestamp']
    })

@app.route('/api/refresh')
def refresh_data():
    """Manually trigger data refresh"""
    try:
        # Update market data
        success = update_market_data()
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Refreshed {len(market_data.get("assets", []))} assets',
                'timestamp': market_data.get('timestamp', datetime.now().isoformat()),
                'total_analyzed': market_data.get('total_analyzed', 0)
            })
        else:
            return jsonify({'error': 'Failed to refresh data'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    """AI chatbot endpoint for investment advice"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Get AI response
        response = chatbot.analyze_user_question(
            question=question,
            market_data=market_data,
            portfolio_data=portfolio_data
        )
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-opportunities')
def top_opportunities_api():
    """Get top 3 profit opportunities"""
    try:
        # Analyze opportunities using the engine
        opportunities = opportunities_engine.analyze_all_opportunities(market_data)
        
        return jsonify({
            'opportunities': opportunities,
            'count': len(opportunities),
            'timestamp': datetime.now().isoformat(),
            'criteria': {
                'min_profit_probability': opportunities_engine.min_profit_probability,
                'min_profit_target': opportunities_engine.min_profit_target,
                'max_risk_level': opportunities_engine.max_risk_level
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Start background tasks
    start_background_tasks()
    
    # Run the Flask app
    print("Starting Scorpion Copilot API Server...")
    print("Available endpoints:")
    print("  GET  /api/market-data - Get current market analysis")
    print("  GET  /api/urgent-signals - Get urgent investment signals")
    print("  GET  /api/news - Get latest market news")
    print("  GET  /api/asset/<ticker> - Get asset details")
    print("  GET  /api/chart/<ticker> - Get chart data")
    print("  GET  /api/portfolio - Get portfolio data")
    print("  POST /api/portfolio - Add/remove positions")
    print("  GET  /api/alerts - Get alerts")
    print("  POST /api/alerts - Create alert")
    print("  GET  /api/search?q=<query> - Search assets")
    print("  GET  /api/stats - Get platform statistics")
    print("  GET  /api/refresh - Refresh data")
    print("  POST /api/chatbot - AI investment advice")
    print("  GET  /api/top-opportunities - Top 3 profit opportunities")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


