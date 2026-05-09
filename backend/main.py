from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI(title="StockScope API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stockscope-1-gwll.onrender.com"],
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
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        # yfinance sometimes returns empty info for invalid tickers
        if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
            raise HTTPException(status_code=404, detail=f"Ticker '{ticker.upper()}' not found.")

        return {
            "symbol": ticker.upper(),
            "name": info.get("longName", info.get("shortName", "N/A")),
            "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "change": round(info.get("regularMarketChange", 0), 2),
            "changePercent": round(info.get("regularMarketChangePercent", 0), 4),
            "marketCap": info.get("marketCap", None),
            "pe": info.get("trailingPE", None),
            "high52": info.get("fiftyTwoWeekHigh", None),
            "low52": info.get("fiftyTwoWeekLow", None),
            "volume": info.get("regularMarketVolume", None),
            "avgVolume": info.get("averageVolume", None),
            "dividendYield": info.get("dividendYield", None),
            "sector": info.get("sector", None),
            "currency": info.get("currency", "USD"),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{ticker}/history")
def get_stock_history(ticker: str, period: str = "1mo"):
    valid_periods = ["7d", "1mo", "3mo", "6mo", "1y"]
    if period not in valid_periods:
        raise HTTPException(status_code=400, detail=f"Invalid period. Choose from: {valid_periods}")

    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period=period)

        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No historical data for '{ticker.upper()}'.")

        data = []
        for date, row in hist.iterrows():
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "volume": int(row["Volume"]),
            })
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
