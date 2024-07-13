# import pricing
from flask import Flask #, abort, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to SimmiSpotter Server!"

@app.route('/health')
def healthCheck():
    return "Server is healthy!"

#http://127.0.0.1:5000/pricing/getCandles?ticker=pypl&interval=60&afterTimestamp=2023-11-11&beforeTimestamp=2024-02-02
# @app.route('/pricing/getCandles', methods=['GET'])
# def getIntradayCandles():
#     ticker = request.args.get('ticker')
#     interval = request.args.get('interval')
#     afterTimestamp = request.args.get('afterTimestamp')
#     beforeTimestamp = request.args.get('beforeTimestamp')
#     groupBy = request.args.get('groupBy')

#     if ticker is None:
#         abort(400, "No ticker provided")

#     if interval is None:
#         abort(400, "No interval provided")

#     if afterTimestamp is None:
#         abort(400, "No afterTimestamp provided")

#     if beforeTimestamp is None:
#         abort(400, "No afterTimestamp provided")

#     if groupBy is None:
#         groupBy = 'day'

#     try:
#         candles = pricing.getCandles(ticker, interval, afterTimestamp, beforeTimestamp, groupBy)
#         return jsonify(candles)
#     except pricing.RateLimitError as rate_limit_err:
#         return jsonify({"error": str(rate_limit_err)}), 429 
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
