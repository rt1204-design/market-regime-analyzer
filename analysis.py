import sqlite3
import pandas as pd

DB_path = "market-data.db"
QUERY = """
    SELECT
        nq.date,
        nq.close AS nq_close,
        es.close AS es_close
    FROM prices AS nq
    JOIN prices AS es
        ON nq.date = es.date
    WHERE nq.symbol = 'NQ'
        AND es.symbol = 'ES'
    ORDER BY nq.date
"""

def load_data ():
    conn = sqlite3.connect(DB_path)
    df = pd.read_sql(QUERY, conn, parse_dates=["date"], index_col="date")
    conn.close()
    return df

def compute_divergence(df):
    df["nq_ret"]=df["nq_close"].pct_change() * 100
    df["es_ret"]=df["es_close"].pct_change() * 100
    df["divergence"] = df["nq_ret"] - df["es_ret"]
    return df.dropna()

def detect_regimes(df,window=20):
    df["rolling_vol"] = df["divergence"].rolling(window).std()
    low, high = df["rolling_vol"].quantile([1/3, 2/3])
    df["regime"] = pd.cut(
        df["rolling_vol"],
        bins=[0, low, high, float("inf")],
        labels=["quiet", "normal", "turbulent"],
    )
    return df.dropna(subset=["rolling_vol"])

if __name__ == "__main__":
    df = detect_regimes(compute_divergence(load_data()))
    print(df.tail())
    print("\nDays per regime:")
    print(df["regime"].value_counts())
    print(f"\nCurrent regime: {df['regime'].iloc[-1]}")
