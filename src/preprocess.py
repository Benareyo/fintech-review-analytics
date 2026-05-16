import os
import pandas as pd

def clean_review_data(input_path, output_path):
    """
    Loads raw scraped reviews, handles structural cleanup anomalies,
    normalizes dates, and saves the output data.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw tracking reference file not found at {input_path}")
        
    # Load dataset
    df = pd.read_csv(input_path)
    initial_count = len(df)
    print(f"Loaded raw dataset containing {initial_count} observations.")
    
    # 1. Drop records lacking core targets (review content or score)
    df = df.dropna(subset=['review', 'rating'])
    after_drop_nan = len(df)
    
    # 2. Drop duplicate user text metrics
    df = df.drop_duplicates(subset=['review', 'bank', 'date'])
    after_dedup = len(df)
    
    # 3. Normalize Date Formats securely to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    print(f"\n--- Data Integrity Statistics ---")
    print(f"Dropped NaN Records: {initial_count - after_drop_nan}")
    print(f"Dropped Duplicate Rows: {after_drop_nan - after_dedup}")
    print(f"Final Retained Analysis Sample Size: {after_dedup}")
    
    # Save cleaned output data asset
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset written successfully to {output_path}")

def main():
    raw_csv = 'data/raw/raw_scraped_reviews.csv'
    clean_csv = 'data/raw/cleaned_reviews.csv'
    clean_review_data(raw_csv, clean_csv)

if __name__ == "__main__":
    main()