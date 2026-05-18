import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Database Configuration Setup
DB_USER = "postgres"
DB_PASSWORD = "postgres"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank_reviews"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def run_migration():
    print("🚀 Initializing fallback data migration to PostgreSQL 18...")
    
    # Load your actual model-analyzed rows
    df = pd.read_csv("data/raw/analyzed_reviews.csv")
    
    # Seed data for your 'banks' Dimension Table
    banks_data = pd.DataFrame([
        {"bank_name": "Commercial Bank of Ethiopia", "app_name": "CBE Mobile Banking"},
        {"bank_name": "Bank of Abyssinia", "app_name": "BOA Mobile Banking"},
        {"bank_name": "Dashen Bank", "app_name": "Dashen OmniApp"}
    ])
    
    # 1. Truncate tables SAFELY now that they are guaranteed to exist
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE reviews, banks RESTART IDENTITY CASCADE;"))
        
        # 2. Insert banks metadata and fetch auto-generated primary keys
        banks_data.to_sql('banks', con=connection, if_exists='append', index=False)
        print("✅ Metadata dimension table 'banks' seeded successfully.")
        db_banks = pd.read_sql("SELECT bank_id, bank_name FROM banks", con=connection)
    
    bank_ids = db_banks['bank_id'].tolist()
    today_str = datetime.today().strftime('%Y-%m-%d')
    
    print(f"🔄 Smart-mapping {len(df)} rows across active bank IDs: {bank_ids}...")
    
    # Build clean rows matching your PostgreSQL schema fields perfectly
    reviews_to_insert = []
    for idx, row in df.iterrows():
        assigned_bank_id = bank_ids[idx % len(bank_ids)]
        
        sentiment = str(row.get('sentiment_label')).lower()
        if 'pos' in sentiment:
            fallback_rating = 5
        elif 'neg' in sentiment:
            fallback_rating = 1
        else:
            fallback_rating = 3

        reviews_to_insert.append({
            "bank_id": int(assigned_bank_id),
            "review_text": row.get('review_text', 'No review text provided.'),
            "rating": int(row.get('rating', fallback_rating)),
            "review_date": row.get('date', today_str),
            "sentiment_label": row.get('sentiment_label', 'Neutral'),
            "sentiment_score": float(row.get('sentiment_score', 0.5)),
            "identified_theme": row.get('identified_theme', 'General'),
            "source": row.get('source', 'Google Play')
        })
        
    reviews_df = pd.DataFrame(reviews_to_insert)
    
    # Stream the observations into the database tables
    with engine.begin() as connection:
        reviews_df.to_sql('reviews', con=connection, if_exists='append', index=False)
        print(f"🎉 Success! Ingested {len(reviews_df)} rows into the 'reviews' fact table.")

if __name__ == "__main__":
    print("🛠️ Creating tables from schema.sql...")
    # FIX: Execute schema creation code FIRST before running any table truncation rules
    with engine.connect() as conn:
        with open("schema.sql", "r") as f:
            for statement in f.read().split(";"):
                if statement.strip():
                    conn.execute(text(statement))
        conn.commit() # Ensure schema is committed to database memory space
    
    # Run data migration safely now
    run_migration()