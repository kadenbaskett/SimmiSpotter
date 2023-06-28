from datetime import datetime, timedelta
import pricing
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to SimmiSpotter API!"

@app.route('/healthCheck')
def healthCheck():
    return "API server is healthy!"

#http://127.0.0.1:5000/pricing/getIntradayCandles?ticker=AMC&interval=60&afterTimestamp=1687749201000&beforeTimestamp=1687922001000
@app.route('/pricing/getMinuteCandles', methods=['GET'])
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

    pricingData = pricing.getMinuteCandles(ticker, interval, afterTimestamp, beforeTimestamp)
    return jsonify(pricingData["results"])

if __name__ == '__main__':
    app.run(debug=True)

# ticker = 'AMC'
# interval = 60

# # Get the current datetime
# current_datetime = datetime.now()

# # Subtract two days using timedelta
# two_days_ago = current_datetime - timedelta(days=2)

# # Convert the datetime to milliseconds timestamp
# twoDaysAgoTimestamp = int(two_days_ago.timestamp() * 1000)

# currentTimestamp = int(current_datetime.timestamp() * 1000)


# pricingData = pricing.getIntradayCandles(ticker, interval, twoDaysAgoTimestamp, currentTimestamp)
# print(pricingData["results"])

