# report_generator.py
import yfinance as yf
import pandas as pd
from datetime import datetime

def get_top_gainers(tickers):
    data = yf.download(tickers, period="1d", group_by="ticker", progress=False)
    results = []

    for ticker in tickers:
        try:
            open_price = data[ticker]["Open"][0]
            close_price = data[ticker]["Close"][0]
            percent_change = ((close_price - open_price) / open_price) * 100
            results.append({
                "Ticker": ticker,
                "Open": round(open_price, 2),
                "Close": round(close_price, 2),
                "Change (%)": round(percent_change, 2)
            })
        except Exception as e:
            print(f"Error with {ticker}: {e}")

    df = pd.DataFrame(results)
    df.sort_values("Change (%)", ascending=False, inplace=True)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"top_gainers_{today}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Saved: {filename}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMD", "PLTR", "META"]
    get_top_gainers(tickers)
