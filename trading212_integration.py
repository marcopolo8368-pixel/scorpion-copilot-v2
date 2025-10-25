"""
Trading212 Portfolio Integration
Handles importing portfolio data from Trading212 CSV exports
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import yfinance as yf

class Trading212Integration:
    def __init__(self):
        self.portfolio_data = {}
        self.last_update = None
    
    def import_from_csv(self, csv_file_path: str) -> Dict:
        """
        Import portfolio data from Trading212 CSV export
        
        Args:
            csv_file_path: Path to the Trading212 CSV file
            
        Returns:
            Dict containing processed portfolio data
        """
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file_path)
            
            # Trading212 CSV columns vary, but typically include:
            # 'Instrument', 'Quantity', 'Average price', 'Current price', 'P&L', etc.
            
            portfolio = {
                'positions': [],
                'total_value': 0,
                'total_pnl': 0,
                'last_update': datetime.now().isoformat(),
                'source': 'Trading212'
            }
            
            for _, row in df.iterrows():
                try:
                    # Extract position data (column names may vary)
                    instrument = self._extract_instrument(row)
                    quantity = self._extract_quantity(row)
                    avg_price = self._extract_avg_price(row)
                    current_price = self._extract_current_price(row)
                    pnl = self._extract_pnl(row)
                    
                    if instrument and quantity and avg_price:
                        position = {
                            'ticker': instrument,
                            'shares': float(quantity),
                            'avg_price': float(avg_price),
                            'current_price': float(current_price) if current_price else None,
                            'pnl': float(pnl) if pnl else 0,
                            'value': float(quantity) * float(current_price) if current_price else 0,
                            'weight': 0  # Will be calculated later
                        }
                        
                        portfolio['positions'].append(position)
                        portfolio['total_value'] += position['value']
                        portfolio['total_pnl'] += position['pnl']
                
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue
            
            # Calculate weights
            for position in portfolio['positions']:
                if portfolio['total_value'] > 0:
                    position['weight'] = (position['value'] / portfolio['total_value']) * 100
            
            # Get current prices for positions without them
            self._update_current_prices(portfolio)
            
            self.portfolio_data = portfolio
            self.last_update = datetime.now()
            
            return portfolio
            
        except Exception as e:
            print(f"Error importing Trading212 CSV: {e}")
            return {}
    
    def _extract_instrument(self, row) -> Optional[str]:
        """Extract instrument/ticker from row"""
        # Try different possible column names
        for col in ['Instrument', 'Symbol', 'Ticker', 'Name']:
            if col in row and pd.notna(row[col]):
                return str(row[col]).strip()
        return None
    
    def _extract_quantity(self, row) -> Optional[float]:
        """Extract quantity from row"""
        for col in ['Quantity', 'Shares', 'Units', 'Size']:
            if col in row and pd.notna(row[col]):
                try:
                    return float(row[col])
                except:
                    continue
        return None
    
    def _extract_avg_price(self, row) -> Optional[float]:
        """Extract average price from row"""
        for col in ['Average price', 'Avg Price', 'Entry Price', 'Cost per share']:
            if col in row and pd.notna(row[col]):
                try:
                    return float(row[col])
                except:
                    continue
        return None
    
    def _extract_current_price(self, row) -> Optional[float]:
        """Extract current price from row"""
        for col in ['Current price', 'Current Price', 'Market Price', 'Last Price']:
            if col in row and pd.notna(row[col]):
                try:
                    return float(row[col])
                except:
                    continue
        return None
    
    def _extract_pnl(self, row) -> Optional[float]:
        """Extract P&L from row"""
        for col in ['P&L', 'Profit/Loss', 'Unrealized P&L', 'Gain/Loss']:
            if col in row and pd.notna(row[col]):
                try:
                    return float(row[col])
                except:
                    continue
        return None
    
    def _update_current_prices(self, portfolio: Dict):
        """Update current prices using yfinance"""
        for position in portfolio['positions']:
            if not position['current_price']:
                try:
                    ticker = yf.Ticker(position['ticker'])
                    hist = ticker.history(period='1d')
                    if not hist.empty:
                        position['current_price'] = float(hist['Close'].iloc[-1])
                        position['value'] = position['shares'] * position['current_price']
                except Exception as e:
                    print(f"Error getting price for {position['ticker']}: {e}")
    
    def export_to_json(self, file_path: str = 'trading212_portfolio.json'):
        """Export portfolio data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.portfolio_data, f, indent=2)
            print(f"Portfolio exported to {file_path}")
        except Exception as e:
            print(f"Error exporting portfolio: {e}")
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary statistics"""
        if not self.portfolio_data:
            return {}
        
        positions = self.portfolio_data['positions']
        
        # Calculate additional metrics
        total_cost = sum(pos['shares'] * pos['avg_price'] for pos in positions)
        total_value = self.portfolio_data['total_value']
        total_pnl = self.portfolio_data['total_pnl']
        
        return {
            'total_positions': len(positions),
            'total_cost': total_cost,
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_return_pct': ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            'last_update': self.portfolio_data['last_update'],
            'source': 'Trading212'
        }
    
    def get_top_positions(self, limit: int = 10) -> List[Dict]:
        """Get top positions by value"""
        if not self.portfolio_data:
            return []
        
        positions = sorted(
            self.portfolio_data['positions'], 
            key=lambda x: x['value'], 
            reverse=True
        )
        
        return positions[:limit]

def create_trading212_import_page():
    """Create HTML page for Trading212 import"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading212 Import - Trading Intelligence Pro</title>
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
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .header h1 {
            font-size: 3rem;
            background: linear-gradient(to right, #60a5fa, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .import-section {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            margin-bottom: 2rem;
        }

        .import-section h2 {
            color: #60a5fa;
            margin-bottom: 1.5rem;
        }

        .instructions {
            background: rgba(59, 130, 246, 0.1);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }

        .instructions h3 {
            color: #60a5fa;
            margin-bottom: 1rem;
        }

        .instructions ol {
            color: #94a3b8;
            line-height: 1.6;
            padding-left: 1.5rem;
        }

        .instructions li {
            margin-bottom: 0.5rem;
        }

        .file-input {
            background: rgba(15, 23, 42, 0.8);
            border: 2px dashed rgba(59, 130, 246, 0.3);
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            transition: all 0.3s;
        }

        .file-input:hover {
            border-color: rgba(59, 130, 246, 0.6);
            background: rgba(59, 130, 246, 0.05);
        }

        .file-input input[type="file"] {
            display: none;
        }

        .file-input label {
            color: #60a5fa;
            cursor: pointer;
            font-weight: bold;
            font-size: 1.1rem;
        }

        .import-btn {
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            font-size: 1.1rem;
        }

        .import-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(96, 165, 250, 0.4);
        }

        .import-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .results {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            margin-top: 2rem;
            display: none;
        }

        .results h2 {
            color: #60a5fa;
            margin-bottom: 1.5rem;
        }

        .position-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            border-bottom: 1px solid rgba(59, 130, 246, 0.1);
        }

        .position-item:last-child {
            border-bottom: none;
        }

        .position-ticker {
            font-weight: bold;
            color: #e2e8f0;
        }

        .position-details {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .position-value {
            font-weight: bold;
            color: #60a5fa;
        }

        .position-pnl {
            font-weight: bold;
        }

        .position-pnl.positive {
            color: #22c55e;
        }

        .position-pnl.negative {
            color: #ef4444;
        }

        .back-btn {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            margin-top: 2rem;
        }

        .back-btn:hover {
            background: rgba(59, 130, 246, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Trading212 Import</h1>
            <p style="color: #94a3b8; font-size: 1.1rem;">
                Import your Trading212 portfolio automatically
            </p>
        </div>

        <div class="import-section">
            <h2>📊 How to Export from Trading212</h2>
            <div class="instructions">
                <h3>Step-by-Step Instructions:</h3>
                <ol>
                    <li>Log into your Trading212 account</li>
                    <li>Go to your Portfolio page</li>
                    <li>Click on the "Export" or "Download" button</li>
                    <li>Select "CSV" format</li>
                    <li>Download the file to your computer</li>
                    <li>Upload the CSV file below</li>
                </ol>
            </div>

            <div class="file-input">
                <input type="file" id="csvFile" accept=".csv" />
                <label for="csvFile">
                    📁 Click to select your Trading212 CSV file
                </label>
            </div>

            <button class="import-btn" onclick="importPortfolio()" id="importBtn">
                Import Portfolio
            </button>
        </div>

        <div class="results" id="results">
            <h2>📈 Imported Portfolio</h2>
            <div id="portfolioSummary"></div>
            <div id="portfolioPositions"></div>
            <a href="portfolio.html" class="back-btn">View in Portfolio Page</a>
        </div>
    </div>

    <script>
        let portfolioData = null;

        function importPortfolio() {
            const fileInput = document.getElementById('csvFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a CSV file first');
                return;
            }

            const btn = document.getElementById('importBtn');
            btn.disabled = true;
            btn.textContent = 'Importing...';

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const csv = e.target.result;
                    portfolioData = parseCSV(csv);
                    displayResults(portfolioData);
                } catch (error) {
                    alert('Error parsing CSV file: ' + error.message);
                } finally {
                    btn.disabled = false;
                    btn.textContent = 'Import Portfolio';
                }
            };
            reader.readAsText(file);
        }

        function parseCSV(csv) {
            const lines = csv.split('\\n');
            const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
            
            const positions = [];
            let totalValue = 0;
            let totalPnl = 0;

            for (let i = 1; i < lines.length; i++) {
                if (lines[i].trim()) {
                    const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
                    const row = {};
                    
                    headers.forEach((header, index) => {
                        row[header] = values[index] || '';
                    });

                    // Extract position data
                    const instrument = row['Instrument'] || row['Symbol'] || row['Name'];
                    const quantity = parseFloat(row['Quantity'] || row['Shares'] || row['Units']);
                    const avgPrice = parseFloat(row['Average price'] || row['Avg Price'] || row['Entry Price']);
                    const currentPrice = parseFloat(row['Current price'] || row['Current Price'] || row['Market Price']);
                    const pnl = parseFloat(row['P&L'] || row['Profit/Loss'] || row['Unrealized P&L'] || 0);

                    if (instrument && quantity && avgPrice) {
                        const value = quantity * (currentPrice || avgPrice);
                        const position = {
                            ticker: instrument,
                            shares: quantity,
                            avgPrice: avgPrice,
                            currentPrice: currentPrice || avgPrice,
                            pnl: pnl,
                            value: value,
                            weight: 0
                        };
                        
                        positions.push(position);
                        totalValue += value;
                        totalPnl += pnl;
                    }
                }
            }

            // Calculate weights
            positions.forEach(pos => {
                pos.weight = totalValue > 0 ? (pos.value / totalValue) * 100 : 0;
            });

            return {
                positions: positions,
                totalValue: totalValue,
                totalPnl: totalPnl,
                totalPositions: positions.length,
                lastUpdate: new Date().toISOString()
            };
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            const summaryDiv = document.getElementById('portfolioSummary');
            const positionsDiv = document.getElementById('portfolioPositions');

            // Display summary
            summaryDiv.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #60a5fa;">${data.totalPositions}</div>
                        <div style="color: #94a3b8;">Positions</div>
                    </div>
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #60a5fa;">$${data.totalValue.toLocaleString()}</div>
                        <div style="color: #94a3b8;">Total Value</div>
                    </div>
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: ${data.totalPnl >= 0 ? '#22c55e' : '#ef4444'};">$${data.totalPnl.toLocaleString()}</div>
                        <div style="color: #94a3b8;">Total P&L</div>
                    </div>
                </div>
            `;

            // Display positions
            positionsDiv.innerHTML = data.positions.map(pos => `
                <div class="position-item">
                    <div>
                        <div class="position-ticker">${pos.ticker}</div>
                        <div class="position-details">${pos.shares} shares @ $${pos.avgPrice.toFixed(2)} avg</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="position-value">$${pos.value.toLocaleString()}</div>
                        <div class="position-pnl ${pos.pnl >= 0 ? 'positive' : 'negative'}">
                            ${pos.pnl >= 0 ? '+' : ''}$${pos.pnl.toFixed(2)}
                        </div>
                    </div>
                </div>
            `).join('');

            resultsDiv.style.display = 'block';

            // Store data for use in portfolio page
            localStorage.setItem('trading212Portfolio', JSON.stringify(data));
        }
    </script>
</body>
</html>
    """
    
    with open('trading212-import.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Trading212 import page created: trading212-import.html")

if __name__ == "__main__":
    # Example usage
    integration = Trading212Integration()
    
    # Create the import page
    create_trading212_import_page()
    
    print("Trading212 integration module created!")
    print("To use:")
    print("1. Export your portfolio from Trading212 as CSV")
    print("2. Open trading212-import.html in your browser")
    print("3. Upload the CSV file to import your portfolio")
    print("4. The portfolio will be available in the Portfolio page")

