# Vercel Python serverless function - FULL API with Yahoo Finance integration
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import json

# Try to import yfinance for real data
try:
    import yfinance as yf
    import pandas as pd
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    pd = None

app = Flask(__name__, static_folder='../', static_url_path='')
CORS(app)

# ============================================================================
# HTML FILE SERVING
# ============================================================================

@app.route('/')
def index():
    """Serve the main index.html page"""
    try:
        return send_from_directory('../', 'index.html')
    except:
        return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/<path:filename>')
def serve_files(filename):
    """Serve HTML files and other static files"""
    if filename.endswith('.html'):
        try:
            return send_from_directory('../', filename)
        except:
            pass
    return jsonify({'error': 'File not found'}), 404

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api')
def api_root():
    """API information"""
    return jsonify({
        'status': 'ok',
        'service': 'Scorpion Copilot API',
        'yfinance': 'available' if YFINANCE_AVAILABLE else 'not available',
        'endpoints': {
            '/api/stats': 'Platform statistics',
            '/api/news': 'Latest market news',
            '/api/urgent-signals': 'Urgent investment signals',
            '/api/ticker/<ticker>': 'Get ticker data',
            '/api/top-opportunities': 'Top investment opportunities',
            '/api/alerts': 'User alerts'
        }
    })

@app.route('/api/stats')
def stats():
    """Get platform statistics"""
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'total_assets': 0,
            'total_universe': 2076,
            'strong_buys': 0,
            'buys': 0,
            'last_update': datetime.now().isoformat()
        })
    
    try:
        # Get real-time stats by analyzing top tickers
        top_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX']
        strong_buys = 0
        buys = 0
        
        for ticker in top_tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                if info and 'recommendationMean' in info:
                    rec = info['recommendationMean']
                    if rec <= 1.5:
                        strong_buys += 1
                    elif rec <= 2.5:
                        buys += 1
            except:
                continue
        
        return jsonify({
            'total_assets': len(top_tickers),
            'total_universe': 2076,
            'strong_buys': strong_buys,
            'buys': buys,
            'last_update': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'total_assets': 100,
            'total_universe': 2076,
            'strong_buys': 15,
            'buys': 30,
            'last_update': datetime.now().isoformat(),
            'error': str(e)
        })

@app.route('/api/news')
def news():
    """Get real news from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': []
        })
    
    try:
        news_items = []
        top_tickers = ['SPY', 'QQQ', 'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX']
        
        for ticker in top_tickers[:8]:
            try:
                stock = yf.Ticker(ticker)
                stock_news = stock.news
                
                if stock_news:
                    for article in stock_news[:3]:  # Get top 3 per ticker
                        pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                        
                        # Determine sentiment from title
                        title = article.get('title', '').lower()
                        summary = article.get('summary', '').lower()
                        impact = 'neutral'
                        if any(word in title or word in summary for word in ['surge', 'jump', 'up', 'gain', 'rally', 'rise', 'soar']):
                            impact = 'positive'
                        elif any(word in title or word in summary for word in ['drop', 'fall', 'down', 'crash', 'plunge', 'decline', 'dip']):
                            impact = 'negative'
                        
                        news_items.append({
                            'title': article.get('title', 'No title'),
                            'summary': article.get('summary', article.get('title', '')),
                            'impact': impact,
                            'timestamp': pub_time.isoformat(),
                            'source': article.get('publisher', 'Unknown'),
                            'tickers': [ticker],
                            'url': article.get('link', ''),
                            'category': 'market'
                        })
            except Exception as e:
                continue
        
        # Sort by timestamp and remove duplicates
        seen_titles = set()
        unique_news = []
        for item in news_items:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)
        
        # Sort by timestamp
        unique_news.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': unique_news[:30]  # Return top 30
        })
    except Exception as e:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': [],
            'error': str(e)
        })

@app.route('/api/urgent-signals')
def urgent_signals():
    """Get urgent trading signals based on real-time data"""
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'signals': [],
            'count': 0
        })
    
    try:
        signals = []
        # Track major movers
        tickers_to_check = ['NVDA', 'AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX', 'AMD', 'INTC']
        
        for ticker in tickers_to_check:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if not info:
                    continue
                
                # Get current price and change
                current_price = info.get('regularMarketPrice') or info.get('currentPrice') or 0
                change = info.get('regularMarketChange', 0)
                change_percent = info.get('regularMarketChangePercent', 0)
                
                # Only flag significant moves (>2% change)
                if abs(change_percent) > 2:
                    signal_type = 'Buy' if change > 0 else 'Sell'
                    priority = 'High' if abs(change_percent) > 5 else 'Medium'
                    
                    signals.append({
                        'ticker': ticker,
                        'type': signal_type,
                        'price': round(current_price, 2),
                        'change': f"{'+' if change >= 0 else ''}{round(change, 2)}",
                        'changePercent': f"{'+' if change_percent >= 0 else ''}{round(change_percent, 2)}%",
                        'signalTime': 'Just now',
                        'reason': f"Significant {signal_type.lower()} signal due to {abs(change_percent):.1f}% price movement",
                        'priority': priority
                    })
            except:
                continue
        
        # Sort by absolute change percentage
        signals.sort(key=lambda x: abs(float(x['changePercent'].replace('%', '').replace('+', ''))), reverse=True)
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'signals': signals[:10],
            'count': len(signals)
        })
    except Exception as e:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'signals': [],
            'count': 0,
            'error': str(e)
        })

@app.route('/api/ticker/<ticker>')
def ticker_data(ticker):
    """Get real-time ticker data"""
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'error': 'yfinance not available',
            'ticker': ticker.upper()
        }), 503
    
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        
        if not info:
            return jsonify({
                'error': 'Ticker not found',
                'ticker': ticker.upper()
            }), 404
        
        # Get real-time price
        price = (
            info.get('regularMarketPrice') or 
            info.get('currentPrice') or 
            info.get('previousClose')
        )
        
        return jsonify({
            'ticker': ticker.upper(),
            'name': info.get('longName', ticker.upper()),
            'price': price,
            'change': info.get('regularMarketChange', 0),
            'change_percent': info.get('regularMarketChangePercent', 0),
            'volume': info.get('volume', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'ticker': ticker.upper()
        }), 500

@app.route('/api/top-opportunities')
def top_opportunities():
    """Get top investment opportunities"""
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'opportunities': []
        })
    
    try:
        opportunities = []
        top_tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMD', 'NFLX', 'CRM']
        
        for ticker in top_tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if not info:
                    continue
                
                price = info.get('regularMarketPrice') or info.get('currentPrice') or 0
                change_percent = info.get('regularMarketChangePercent', 0)
                recommendation = info.get('recommendationMean', 3.0)
                
                # Calculate opportunity score
                opportunity_score = 0
                if recommendation <= 2.0:
                    opportunity_score += 30
                if change_percent > 0:
                    opportunity_score += abs(change_percent) * 2
                
                opportunities.append({
                    'ticker': ticker,
                    'name': info.get('longName', ticker),
                    'price': price,
                    'change_percent': round(change_percent, 2),
                    'opportunity_score': round(opportunity_score, 1),
                    'recommendation': 'Strong Buy' if recommendation <= 1.5 else 'Buy' if recommendation <= 2.5 else 'Hold'
                })
            except:
                continue
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'opportunities': opportunities[:5]
        })
    except Exception as e:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'opportunities': [],
            'error': str(e)
        })

@app.route('/api/alerts')
def alerts():
    """Get user alerts (placeholder)"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'alerts': []
    })

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create a new alert (placeholder)"""
    return jsonify({
        'status': 'success',
        'message': 'Alert created',
        'timestamp': datetime.now().isoformat()
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
