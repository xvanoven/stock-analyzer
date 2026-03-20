from flask import Flask, jsonify, render_template
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

PORTFOLIO = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/portfolio")
def get_portfolio():
    results = []
    for ticker in PORTFOLIO:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")

        results.append({
            "symbol": ticker,
            "name": info.get("longName") or info.get("shortName") or info.get("quoteType", ticker),
            "price": round(info.get("currentPrice", 0), 2),
            "change_pct": round(info.get("regularMarketChangePercent", 0), 2),
            "week_high": round(hist["High"].max(), 2),
            "week_low": round(hist["Low"].min(), 2),
        })

    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)