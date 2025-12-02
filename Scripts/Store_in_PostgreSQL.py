# File: store_reviews_postgres.py

import os
import sys
import pandas as pd
import psycopg2
from psycopg2 import sql

# ================================
# Configuration
# ================================
DB_CONFIG = {
    "dbname": "bank_reviews",
    "user": "postgres",      # Replace with your username
    "password": "root",      # Replace with your password
    "host": "localhost",
    "port": "5433"
}

CSV_PATHS = {
    "positive": "../output/positive_reviews_with_themes.csv",
    "negative": "../output/negative_reviews_with_themes.csv"
}

TABLE_NAMES = {
    "positive": "positive_reviews_with_themes",
    "negative": "negative_reviews_with_themes"
}

# ================================
# PostgreSQL Helper Class
# ================================
class PostgresHandler:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL successfully!")
        except Exception as e:
            print("Error connecting to PostgreSQL:", e)
            sys.exit(1)
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("PostgreSQL connection closed.")
    
    def create_table(self, table_name):
        """Create table if not exists"""
        create_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table} (
                review_id TEXT PRIMARY KEY,
                bank_id TEXT,
                review_text TEXT,
                rating REAL,
                review_date TIMESTAMP,
                bank_name TEXT,
                bank_code TEXT,
                source TEXT,
                sentiment_label TEXT,
                sentiment_score REAL,
                sentiment_group TEXT,
                cleaned_text TEXT,
                keywords TEXT,
                theme TEXT
            );
        """).format(table=sql.Identifier(table_name))
        
        self.cursor.execute(create_query)
        self.conn.commit()
        print(f"Table '{table_name}' created or already exists.")
    
    def insert_dataframe(self, table_name, df):
        """Insert a DataFrame into the given table"""
        for _, row in df.iterrows():
            try:
                insert_query = sql.SQL("""
                    INSERT INTO {table} (
                        review_id, bank_id, review_text, rating, review_date, bank_name,
                        bank_code, source, sentiment_label, sentiment_score,
                        sentiment_group, cleaned_text, keywords, theme
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (review_id) DO NOTHING;
                """).format(table=sql.Identifier(table_name))
                
                self.cursor.execute(insert_query, (
                    row.get('review_id'),
                    row.get('bank_id'),
                    row.get('review_text'),
                    row.get('rating'),
                    row.get('review_date'),
                    row.get('bank_name'),
                    row.get('bank_code'),
                    row.get('source'),
                    row.get('sentiment_label'),
                    row.get('sentiment_score'),
                    row.get('sentiment_group'),
                    row.get('cleaned_text'),
                    row.get('keywords'),
                    row.get('theme')
                ))
            except Exception as e:
                print(f"Error inserting row {row.get('review_id')}: {e}")
        self.conn.commit()
        print(f"Data inserted into '{table_name}' successfully! Total rows: {len(df)}")

# ================================
# Main Execution
# ================================
def main():
    # 1. Connect to PostgreSQL
    db = PostgresHandler(DB_CONFIG)
    db.connect()
    
    # 2. Process CSVs
    for key in ['positive', 'negative']:
        csv_path = CSV_PATHS[key]
        table_name = TABLE_NAMES[key]
        
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            continue
        
        df = pd.read_csv(csv_path)
        print(f"Loaded '{csv_path}' with {len(df)} rows.")
        
        # 3. Create table if not exists
        db.create_table(table_name)
        
        # 4. Insert data
        db.insert_dataframe(table_name, df)
    
    # 5. Close connection
    db.close()

# ================================
# Entry point
# ================================
if __name__ == "__main__":
    main()
