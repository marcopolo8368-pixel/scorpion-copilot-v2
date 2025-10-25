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
    """Background task to update market data every 5 minutes"""
    global market_data, news_data
    
    while True:
        try:
            print("Updating market data...")
            
            # Run analysis on a sample of assets for performance
            sample_size = min(100, len(ALL_TICKERS))
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
            
        except Exception as e:
            print(f"Error updating market data: {e}")
        
        # Wait 5 minutes before next update
        time.sleep(300)

def start_background_tasks():
    """Start background data update tasks"""
    update_thread = threading.Thread(target=update_market_data, daemon=True)
    update_thread.start()

# API Routes

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the main Scorpion Copilot dashboard"""
    return send_from_directory('.', 'ScorpionCopilot_Dashboard.html')

@app.route('/TradingIntelligence_Dashboard.html')
def trading_dashboard():
    """Serve the Trading Intelligence dashboard"""
    return send_from_directory('.', 'TradingIntelligence_Dashboard.html')

@app.route('/<path:filename>')
def serve_html(filename):
    """Serve HTML files"""
    return send_from_directory('.', filename)

@app.route('/api/market-data')
def get_market_data():
    """Get current market data"""
    if not market_data:
        return jsonify({'error': 'No data available'}), 404
    
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
    """Get detailed REAL-TIME analysis for a specific asset"""
    try:
        import yfinance as yf
        
        # Fetch REAL-TIME current price
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        real_time_price = None
        
        if info:
            real_time_price = (
                info.get('regularMarketPrice') or 
                info.get('currentPrice') or 
                info.get('regularMarketPreviousClose') or
                info.get('previousClose')
            )
        
        # Run complete analysis
        analysis = analyze_asset(ticker)
        
        if analysis:
            # Update with REAL-TIME price
            if real_time_price:
                analysis['price'] = real_time_price
                analysis['technical_score'] = real_time_price
            
            # Add metadata
            analysis['last_updated'] = datetime.now().isoformat()
            analysis['data_source'] = 'yfinance_live'
            
            return jsonify(analysis)
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/<ticker>')
def get_chart_data(ticker):
    """Get REAL-TIME chart data for a specific asset"""
    timeframe = request.args.get('timeframe', '1m')
    
    try:
        import yfinance as yf
        
        # Get REAL-TIME price and update chart data
        chart_data = fetch_chart_data(ticker, timeframe)
        
        if chart_data:
            # Fetch the absolute latest price
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            
            if info:
                real_time_price = (
                    info.get('regularMarketPrice') or 
                    info.get('currentPrice') or 
                    info.get('regularMarketPreviousClose') or
                    info.get('previousClose')
                )
                
                if real_time_price:
                    # Update the current price in chart data
                    chart_data['current_price'] = real_time_price
                    
                    # Recalculate change and change_percent based on real-time price
                    if 'data' in chart_data and len(chart_data['data']) > 0:
                        first_open = chart_data['data'][0]['open']
                        chart_data['change'] = round(real_time_price - first_open, 2)
                        chart_data['change_percent'] = round(((real_time_price / first_open) - 1) * 100, 2)
            
            chart_data['last_updated'] = datetime.now().isoformat()
            chart_data['data_source'] = 'yfinance_live'
            
            return jsonify(chart_data)
        else:
            return jsonify({'error': 'Chart data not available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ticker/<ticker>')
def get_ticker_data(ticker):
    """Get complete REAL-TIME data for a specific ticker"""
    try:
        from scorpion_backend import analyze_asset
        import yfinance as yf
        
        # Fetch REAL-TIME current price directly from yfinance
        stock = yf.Ticker(ticker.upper())
        
        # Get the absolute latest price info
        info = stock.info
        real_time_price = None
        
        if info:
            # Try multiple fields to get the absolute latest price
            real_time_price = (
                info.get('regularMarketPrice') or 
                info.get('currentPrice') or 
                info.get('regularMarketPreviousClose') or
                info.get('previousClose')
            )
        
        # Run complete analysis
        data = analyze_asset(ticker.upper())
        
        if data:
            # Update with the REAL-TIME price if we got one
            if real_time_price:
                data['price'] = real_time_price
                # Also update the technical score to reflect the new price
                data['technical_score'] = real_time_price
            
            # Add metadata about data freshness
            data['last_updated'] = datetime.now().isoformat()
            data['data_source'] = 'yfinance_live'
            
            return jsonify(data)
        else:
            return jsonify({'error': 'Ticker not found'}), 404
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
        # Run a quick analysis
        results = run_live_analysis(sample_size=50)
        market_data['assets'] = results
        market_data['timestamp'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': f'Refreshed {len(results)} assets',
            'timestamp': market_data['timestamp']
        })
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


