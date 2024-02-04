from datetime import datetime, timedelta
import pricing
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to SimmiSpotter API!"

@app.route('/healthCheck')
def healthCheck():
    return "Server is healthy!"

#http://127.0.0.1:5000/pricing/getCandles?ticker=pypl&interval=60&afterTimestamp=2023-11-11&beforeTimestamp=2024-02-02
@app.route('/pricing/getCandles', methods=['GET'])
def getIntradayCandles():
    ticker = request.args.get('ticker')
    interval = request.args.get('interval')
    afterTimestamp = request.args.get('afterTimestamp')
    beforeTimestamp = request.args.get('beforeTimestamp')


    if ticker is None:
        abort(400, "No ticker provided")

    if interval is None:
        abort(400, "No interval provided")

    if afterTimestamp is None:
        abort(400, "No afterTimestamp provided")

    if beforeTimestamp is None:
        print("No beforeTimestamp provided.")

    candles = pricing.getCandles(ticker.upper(), interval, afterTimestamp, beforeTimestamp)
    return jsonify(candles)

if __name__ == '__main__':
    app.run(debug=True)
