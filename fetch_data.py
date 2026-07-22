import yfinance as yf
import database

SYMBOLS = {"NQ": "NQ=F", "ES": "ES=F"}

def fetch_and_store():
    database.create_table()
    for name, yahoo_ticker in SYMBOLS.items():
        df = yf.Ticker(yahoo_ticker).history(period="1y")
        database.save_prices(name,df)
        print(f"Saved {len(df)} rows for {name}")

if __name__ == "__main__":
    fetch_and_store()
