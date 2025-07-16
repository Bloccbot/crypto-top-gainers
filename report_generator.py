# report_generator.py
import yfinance as yf
import pandas as pd
from datetime import datetime
# ACCESSING THE KEYS IN YOUR SCRIPT
import os
import json

openai_key = os.getenv("OPENAI_API_KEY")
email_user = os.getenv("EMAIL_SENDER")
email_pass = os.getenv("EMAIL_APP_PASSWORD")

# Load Google Sheets creds
gsheet_json_str = os.getenv("GSHEET_CREDENTIALS_JSON")
gsheet_creds = json.loads(gsheet_json_str)
#########################################################################

from email_sender import send_email_with_attachment

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
# Uses email_sender to send the report

# Send email after saving the Excel file
send_email_with_attachment(
    to_email="eddieloya191@gmail.com",
    subject="🚀 Daily Crypto Gainers Report",
    body="Attached is your automated crypto gainers report. Let me know if you want anything changed!",
attachment_path=filename
)


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMD", "PLTR", "META"]
    get_top_gainers(tickers)
