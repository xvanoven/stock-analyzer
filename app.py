from flask import Flask, jsonify, render_template
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

PORTFOLIO = ["AAPL", "GOOGL", "MSFT", "TSLA", "HPE", "AMZN", "NVDA", "META", "NFLX", "AMD", "CRM", "AVGO", "CSGP", "EXPGY", "EFX", "APH", "PLTR", "SMCI", "FSLR", "KO", "LLY", "ISRG", "CSCO", "ORCL", "ENGIY", "HPQ"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/portfolio")
def get_portfolio():
    results = []
    for ticker in PORTFOLIO:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="5d")

            results.append({
                "symbol": ticker,
                "name": info.get("longName") or info.get("shortName") or ticker,
                "price": round(info.get("currentPrice", 0), 2),
                "change_pct": round(info.get("regularMarketChangePercent", 0), 2),
                "week_high": round(hist["High"].max(), 2),
                "week_low": round(hist["Low"].min(), 2),
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            results.append({
                "symbol": ticker,
                "name": ticker,
                "price": 0,
                "change_pct": 0,
                "week_high": 0,
                "week_low": 0,
            })

    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response