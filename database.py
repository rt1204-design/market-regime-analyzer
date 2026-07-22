import sqlite3

DB_PATH = "market-data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS PRICES (
                     date TEXT NOT NULL,
                     symbol TEXT NOT NULL,
                     close REAL NOT NULL,
                     PRIMARY KEY (date, symbol)
                    )
                """)
    conn.commit()
    conn.close()

def save_prices(symbol,df):
    conn = get_connection()
    for date, row in df.iterrows():
        conn.execute(
            "INSERT OR REPLACE INTO prices (date, symbol, close) VALUES (?, ?, ?)",
            (date.strftime("%Y-%m-%d"), symbol, row["Close"]),
        )
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    create_table()
    print("Table 'prices' ready.")