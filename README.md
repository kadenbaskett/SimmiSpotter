# SimmiSpotter

The engine of a trading bot designed to automate trading strategies and send out notifications for trading actions. The engine leverages various technologies and APIs to provide real-time trading data, visualize strategies' performances, and execute trades.

# Features

- Pricing Data: Utilizes Polygon API to fetch real-time and historical market data for accurate and up-to-date information.
- Visualization: Implements TradingView Lightweight Charts library for Python to visualize trading strategies and performance, enabling users to see historical data and strategy outcomes.
- Text Notifications: Sends text notifications when the bot is buying or selling a ticker you have subscribed to.
- Crypto Trading: Fully automates cryptocurrency trades using the Robinhood Crypto API, enabling seamless execution of trading strategies without manual intervention.

# Setup

pip install -r requirements.txt

# Run

python server.py

# Docker

docker build -t simmi-spotter .

docker run -p 5000:5000 simmi-spotter
