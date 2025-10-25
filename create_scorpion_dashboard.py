"""
Convert JSON data to JavaScript for direct embedding in HTML
This avoids the need for an HTTP server and includes ALL enhanced features
"""

import json
import os
from datetime import datetime

def create_embedded_dashboard():
    """Create a dashboard with embedded data including charts and AI features"""
    
    # Load the JSON data
    if not os.path.exists('live_trading_signals.json'):
        print("ERROR: live_trading_signals.json not found!")
        print("Please run: python live_trading_backend.py first")
        return False
    
    with open('live_trading_signals.json', 'r') as f:
        data = json.load(f)
    
    # Read the enhanced dashboard HTML
    with open('TradingIntelligence_Dashboard.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace the loadData function with embedded data
    embedded_script = f"""
        var allAssets = {json.dumps(data['assets'])};
        var currentFilter = 'all';
        var dataTimestamp = '{data['timestamp']}';
        var totalAnalyzed = {data['total_analyzed']};
        var currentChart = null;

        function loadData() {{
            // Data is already loaded
            document.getElementById('lastUpdate').textContent = 
                `Last updated: ${{new Date(dataTimestamp).toLocaleString()}} | ${{totalAnalyzed}} assets analyzed`;
            
            displayStats({{assets: allAssets, total_analyzed: totalAnalyzed}});
            displayAssets(allAssets);
        }}

        function displayStats(data) {{
            const strongBuys = data.assets.filter(a => a.recommendation === 'STRONG BUY').length;
            const buys = data.assets.filter(a => a.recommendation.includes('BUY')).length;
            const sells = data.assets.filter(a => a.recommendation.includes('SELL')).length;
            const avgScore = (data.assets.reduce((sum, a) => sum + a.score, 0) / data.assets.length).toFixed(1);

            document.getElementById('statsGrid').innerHTML = `
                <div class="stat-card">
                    <div class="label">Total Assets</div>
                    <div class="value">${{data.total_analyzed}}</div>
                </div>
                <div class="stat-card">
                    <div class="label">Strong Buy Signals</div>
                    <div class="value" style="color: #4ade80">${{strongBuys}}</div>
                </div>
                <div class="stat-card">
                    <div class="label">Buy Signals</div>
                    <div class="value" style="color: #60a5fa">${{buys}}</div>
                </div>
                <div class="stat-card">
                    <div class="label">Average Score</div>
                    <div class="value" style="color: #a78bfa">${{avgScore}}</div>
                </div>
            `;
        }}

        function displayAssets(assets) {{
            const grid = document.getElementById('assetsGrid');
            
            if (assets.length === 0) {{
                grid.innerHTML = '<div class="loading">No assets match your filters</div>';
                return;
            }}

            grid.innerHTML = assets.map((asset, index) => `
                <div class="asset-card">
                    <div class="asset-header">
                        <div class="asset-info">
                            <h3>#${{index + 1}}. ${{asset.ticker}}</h3>
                            <div class="sector">${{asset.sector}}</div>
                        </div>
                        <div class="score-badge">
                            <div class="score">${{asset.score.toFixed(1)}}</div>
                            <div class="score-label">SCORE</div>
                        </div>
                    </div>

                    <div class="recommendation ${{asset.recommendation.toLowerCase().replace(/ /g, '-')}}">
                        ${{asset.recommendation}}
                    </div>

                    <div class="asset-details">
                        <div class="detail-item">
                            <div class="label">Price</div>
                            <div class="value">$${{asset.price.toFixed(2)}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="label">3M Momentum</div>
                            <div class="value ${{asset.momentum_3m >= 0 ? 'positive' : 'negative'}}">
                                ${{asset.momentum_3m >= 0 ? '+' : ''}}${{asset.momentum_3m.toFixed(1)}}%
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="label">RSI</div>
                            <div class="value">${{asset.rsi.toFixed(0)}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="label">Confidence</div>
                            <div class="value" style="color: #c084fc; font-size: 1em;">${{asset.confidence}}</div>
                        </div>
                    </div>

                    ${{asset.news_sentiment ? `
                        <div class="news-sentiment">
                            <div class="label">📰 AI News Sentiment</div>
                            <div class="sentiment-score ${{asset.news_sentiment.sentiment}}">
                                ${{asset.news_sentiment.sentiment.toUpperCase()}} (${{asset.news_sentiment.score}})
                            </div>
                            <div class="news-headlines">
                                <ul>
                                    ${{asset.news_sentiment.headlines.map(headline => `<li>${{headline}}</li>`).join('')}}
                                </ul>
                            </div>
                        </div>
                    ` : ''}}

                    ${{asset.experts.length > 0 ? `
                        <div class="experts">
                            <div class="label">👥 Expert Holders (${{asset.num_experts}})</div>
                            <div class="expert-badges">
                                ${{asset.experts.map(expert => `
                                    <span class="expert-badge">⭐ ${{expert}}</span>
                                `).join('')}}
                            </div>
                        </div>
                    ` : ''}}

                    <div class="reasoning">
                        <div class="label">📊 AI Analysis</div>
                        <ul>
                            ${{asset.reasoning.slice(0, 4).map(reason => `
                                <li>${{reason}}</li>
                            `).join('')}}
                        </ul>
                    </div>

                    <div style="text-align: center; margin-top: 16px;">
                        <button class="chart-btn" onclick="event.stopPropagation(); openAssetModal('${{asset.ticker}}')">
                            📈 View Interactive Chart & Analysis
                        </button>
                    </div>
                </div>
            `).join('');
        }}

        function openAssetModal(ticker) {{
            const asset = allAssets.find(a => a.ticker === ticker);
            if (!asset) return;

            const modal = document.getElementById('assetModal');
            const modalContent = document.getElementById('modalContent');
            
            modalContent.innerHTML = `
                <h2 style="color: #60a5fa; margin-bottom: 20px;">${{asset.ticker}} - ${{asset.sector}}</h2>
                
                <div class="chart-container">
                    <div class="chart-controls">
                        <button class="timeframe-btn active" onclick="updateChart('${{ticker}}', '1d')">1 Day</button>
                        <button class="timeframe-btn" onclick="updateChart('${{ticker}}', '1w')">1 Week</button>
                        <button class="timeframe-btn" onclick="updateChart('${{ticker}}', '1m')">1 Month</button>
                        <button class="timeframe-btn" onclick="updateChart('${{ticker}}', '3m')">3 Months</button>
                    </div>
                    <canvas id="assetChart" width="400" height="200"></canvas>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div>
                        <h3 style="color: #60a5fa; margin-bottom: 15px;">Technical Indicators</h3>
                        <div class="asset-details">
                            <div class="detail-item">
                                <div class="label">SMA 20</div>
                                <div class="value">$${{asset.technical_indicators.sma_20.toFixed(2)}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="label">SMA 50</div>
                                <div class="value">$${{asset.technical_indicators.sma_50.toFixed(2)}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="label">MACD</div>
                                <div class="value">${{asset.technical_indicators.macd.toFixed(3)}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="label">MACD Signal</div>
                                <div class="value">${{asset.technical_indicators.macd_signal.toFixed(3)}}</div>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h3 style="color: #60a5fa; margin-bottom: 15px;">Performance</h3>
                        <div class="asset-details">
                            <div class="detail-item">
                                <div class="label">1 Week</div>
                                <div class="value ${{asset.momentum_1w >= 0 ? 'positive' : 'negative'}}">
                                    ${{asset.momentum_1w >= 0 ? '+' : ''}}${{asset.momentum_1w.toFixed(1)}}%
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="label">1 Month</div>
                                <div class="value ${{asset.momentum_1m >= 0 ? 'positive' : 'negative'}}">
                                    ${{asset.momentum_1m >= 0 ? '+' : ''}}${{asset.momentum_1m.toFixed(1)}}%
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="label">3 Months</div>
                                <div class="value ${{asset.momentum_3m >= 0 ? 'positive' : 'negative'}}">
                                    ${{asset.momentum_3m >= 0 ? '+' : ''}}${{asset.momentum_3m.toFixed(1)}}%
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="label">Volume Ratio</div>
                                <div class="value">${{asset.volume_ratio.toFixed(2)}}x</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            modal.style.display = 'block';
            
            // Initialize chart with 1 month data
            setTimeout(() => updateChart(ticker, '1m'), 100);
        }}

        function updateChart(ticker, timeframe) {{
            const asset = allAssets.find(a => a.ticker === ticker);
            if (!asset || !asset.chart_data || !asset.chart_data[timeframe]) return;

            // Update active button
            document.querySelectorAll('.timeframe-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            const chartData = asset.chart_data[timeframe];
            const ctx = document.getElementById('assetChart').getContext('2d');

            if (currentChart) {{
                currentChart.destroy();
            }}

            const labels = chartData.data.map(d => d.date);
            const prices = chartData.data.map(d => d.close);

            currentChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Price',
                        data: prices,
                        borderColor: '#60a5fa',
                        backgroundColor: 'rgba(96, 165, 250, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{
                                color: '#e2e8f0'
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            ticks: {{
                                color: '#94a3b8'
                            }},
                            grid: {{
                                color: 'rgba(148, 163, 184, 0.1)'
                            }}
                        }},
                        y: {{
                            type: 'linear',
                            display: true,
                            position: 'left',
                            ticks: {{
                                color: '#94a3b8'
                            }},
                            grid: {{
                                color: 'rgba(148, 163, 184, 0.1)'
                            }}
                        }}
                    }}
                }}
            }});
        }}

        // Filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                currentFilter = this.dataset.filter;
                applyFilters();
            }});
        }});

        // Search functionality
        document.getElementById('searchBox').addEventListener('input', function() {{
            applyFilters();
        }});

        function applyFilters() {{
            let filtered = allAssets;

            // Apply recommendation filter
            if (currentFilter !== 'all') {{
                filtered = filtered.filter(asset => 
                    asset.recommendation.includes(currentFilter)
                );
            }}

            // Apply search filter
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            if (searchTerm) {{
                filtered = filtered.filter(asset =>
                    asset.ticker.toLowerCase().includes(searchTerm) ||
                    asset.name.toLowerCase().includes(searchTerm) ||
                    asset.sector.toLowerCase().includes(searchTerm)
                );
            }}

            displayAssets(filtered);
        }}

        // Modal functionality
        document.querySelector('.close').addEventListener('click', function() {{
            document.getElementById('assetModal').style.display = 'none';
            if (currentChart) {{
                currentChart.destroy();
                currentChart = null;
            }}
        }});

        window.addEventListener('click', function(event) {{
            const modal = document.getElementById('assetModal');
            if (event.target === modal) {{
                modal.style.display = 'none';
                if (currentChart) {{
                    currentChart.destroy();
                    currentChart = null;
                }}
            }}
        }});

        // Load data on page load
        loadData();
    """
    
    # Replace the script section in the HTML
    start_marker = '<script>'
    end_marker = '</script>'
    
    start_idx = html_content.find(start_marker)
    end_idx = html_content.rfind(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_html = html_content[:start_idx + len(start_marker)] + embedded_script + html_content[end_idx:]
        
        # Write the new dashboard
        with open('TradingIntelligence_Dashboard.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print("SUCCESS: Created TradingIntelligence_Dashboard.html with ALL enhanced features")
        print(f"Embedded {len(data['assets'])} assets with charts and AI analysis")
        print(f"Data timestamp: {data['timestamp']}")
        return True
    else:
        print("ERROR: Could not find script section in TradingIntelligence_Dashboard.html")
        return False

if __name__ == "__main__":
    create_embedded_dashboard()