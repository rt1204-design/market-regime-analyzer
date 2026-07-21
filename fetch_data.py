import yfinance as yf
import pandas as pd

nq = yf.Ticker("NQ=F").history(period="1y")
es = yf.Ticker("ES=F").history(period="1y")

df = pd.DataFrame({
    "nq_close": nq["Close"],
    "es_close": es["Close"],
})

df ["nq_ret"] = df["nq_close"].pct_change() * 100
df ["es_ret"] = df["es_close"].pct_change() * 100
df["divergence"] = df["nq_ret"] - df["es_ret"]

df = df.dropna()

print(df.tail(10))
print(f"\nAvg Daily Divergence: {df['divergence'].mean():.3f}%")
print(f"Biggest NQ Outperformance: {df['divergence'].max():.2f}%")
print(f"Biggest NQ Underperformance: {df['divergence'].min():.2f}%")