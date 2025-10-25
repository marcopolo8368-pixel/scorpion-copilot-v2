#!/bin/bash

echo "========================================"
echo "  Trading Intelligence Pro Startup"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

python3 --version

echo
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "Generating initial data..."
python3 live_trading_backend.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to generate market data"
    exit 1
fi

echo
echo "Creating standalone dashboard..."
python3 create_standalone_dashboard.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create dashboard"
    exit 1
fi

echo
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo
echo "Choose your preferred option:"
echo
echo "1. Open Standalone Dashboard (No server required)"
echo "2. Start Web Server (Full API + Multi-page site)"
echo "3. Exit"
echo
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo
        echo "Opening standalone dashboard..."
        if command -v xdg-open &> /dev/null; then
            xdg-open TradingIntelligence_Dashboard.html
        elif command -v open &> /dev/null; then
            open TradingIntelligence_Dashboard.html
        else
            echo "Please open TradingIntelligence_Dashboard.html in your browser"
        fi
        echo "Dashboard opened in your default browser"
        echo
        echo "To update data, run: python3 live_trading_backend.py"
        echo "Then run: python3 create_standalone_dashboard.py"
        ;;
    2)
        echo
        echo "Starting web server..."
        echo "Server will be available at: http://localhost:5000"
        echo "Multi-page site available at: index.html"
        echo
        echo "Press Ctrl+C to stop the server"
        python3 app.py
        ;;
    3)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo
read -p "Press Enter to continue..."


