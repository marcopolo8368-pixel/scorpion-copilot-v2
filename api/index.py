# Vercel Python serverless function
# Minimal import to avoid issues with complex dependencies
from flask import Flask, jsonify, request
import os
from datetime import datetime

# Try to import yfinance for real data
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

app = Flask(__name__)

# Health check endpoint
@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'service': 'Scorpion Copilot API',
        'message': 'Please use /api endpoints',
        'yfinance': 'available' if YFINANCE_AVAILABLE else 'not available'
    })

@app.route('/api')
def api_root():
    return jsonify({
        'status': 'ok',
        'endpoints': {
            '/api/stats': 'Get platform statistics',
            '/api/news': 'Get latest market news',
            '/api/urgent-signals': 'Get urgent investment signals',
            '/api/ticker/<ticker>': 'Get ticker data'
        }
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        'total_assets': 100,
        'total_universe': 2076,
        'strong_buys': 15,
        'buys': 30,
        'last_update': datetime.now().isoformat(),
        'message': 'Stats endpoint - backend loading'
    })

@app.route('/api/news')
def news():
    if not YFINANCE_AVAILABLE:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': [{
                'title': 'API Loading',
                'summary': 'Market data is being initialized',
                'impact': 'neutral',
                'timestamp': datetime.now().isoformat()
            }]
        })
    
    # Fetch real news from yfinance
    try:
        news_items = []
        # Get news from top tickers
        top_tickers = ['SPY', 'QQQ', 'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        
        for ticker in top_tickers[:5]:
            try:
                stock = yf.Ticker(ticker)
                stock_news = stock.news
                
                if stock_news:
                    for article in stock_news[:2]:  # Get first 2 articles per ticker
                        pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                        news_items.append({
                            'title': article.get('title', 'No title'),
                            'summary': article.get('summary', article.get('title', '')),
                            'impact': 'neutral',
                            'timestamp': pub_time.isoformat(),
                            'source': article.get('publisher', 'Unknown'),
                            'tickers': [ticker],
                            'url': article.get('link', '')
                        })
            except:
                continue
        
        # Sort by timestamp and limit
        news_items.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': news_items[:20]
        })
    except Exception as e:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'news': [],
            'error': str(e)
        })

@app.route('/api/urgent-signals')
def signals():
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'signals': [],
        'count': 0
    })

@app.route('/api/ticker/<ticker>')
def ticker_data(ticker):
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
            'name': info.get('longName', 'N/A'),
            'price': price,
            'change': info.get('regularMarketChange', 0),
            'change_percent': info.get('regularMarketChangePercent', 0),
            'volume': info.get('volume', 0),
            'market_cap': info.get('marketCap', 0),
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'ticker': ticker.upper()
        }), 500

# Export for Vercel
handler = app
