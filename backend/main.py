from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
API_KEY = os.environ.get("API_KEY", "520YNHN2QNMWIFZP")

BASE = "https://www.alphavantage.co/query"

app = FastAPI(title="StockScope API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://stockscope-1-gwll.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "StockScope API is running 🚀"}

@app.get("/api/stock/{ticker}")
def get_stock_info(ticker: str):
    try:
        r = requests.get(BASE, params={
            "function": "GLOBAL_QUOTE",
            "symbol": ticker.upper(),
            "apikey": API_KEY,
        })
        data = r.json()
        quote = data.get("Global Quote", {})
        if not quote:
            raise HTTPException(status_code=404, detail=f"Ticker '{ticker.upper()}' not found.")
        return {
            "symbol": ticker.upper(),
            "name": ticker.upper(),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "changePercent": float(quote.get("10. change percent", "0%").replace("%", "")) / 100,
            "marketCap": None,
            "pe": None,
            "high52": float(quote.get("03. high", 0)),
            "low52": float(quote.get("04. low", 0)),
            "volume": int(quote.get("06. volume", 0)),
            "avgVolume": None,
            "dividendYield": None,
            "sector": None,
            "currency": "USD",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{ticker}/history")
def get_stock_history(ticker: str, period: str = "1mo"):
    try:
        r = requests.get(BASE, params={
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker.upper(),
            "outputsize": "compact",
            "apikey": API_KEY,
        })
        data = r.json()
        ts = data.get("Time Series (Daily)", {})
        if not ts:
            raise HTTPException(status_code=404, detail=f"No data for '{ticker.upper()}'.")

        days = {"7d": 7, "1mo": 30, "3mo": 90, "6mo": 180, "1y": 365}
        limit = days.get(period, 30)

        result = []
        for date, values in sorted(ts.items(), reverse=False)[-limit:]:
            result.append({
                "date": date,
                "close": float(values["4. close"]),
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "volume": int(values["5. volume"]),
            })
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))