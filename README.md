# SimmiSpotter
Server for indicators to assist in navigating manipulated financial markets.

# Setup
pip install -r requirements.txt

# Run
python server.py

Example requests are commented above endpoint declarations in server.py

# Docker
docker build -t your-image-name .
docker run -p 5000:5000 your-image-name
