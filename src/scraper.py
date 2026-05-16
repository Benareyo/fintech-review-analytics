import os
import pandas as pd
from google_play_scraper import Sort, reviews

def scrape_bank_reviews(app_id, bank_name, target_count=500):
    """
    Scrapes a target number of reviews using pagination tokens
    to guarantee data asset collection sizes.
    """
    print(f"Starting data collection for {bank_name} ({app_id})...")
    all_reviews = []
    continuation_token = None
    
    # Paginate until we hit our target count per bank safely
    while len(all_reviews) < target_count:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',        # Focus strictly on English comments for the transformer models
                country='us',     # Widen marketplace storefront to pull stable data packages
                sort=Sort.NEWEST, # Fetch fresh feedback
                count=200,        # Max batch size threshold per API call
                continuation_token=continuation_token
            )
            
            if not result:
                print(f"No more reviews visible for {bank_name}.")
                break
                
            for r in result:
                if len(all_reviews) >= target_count:
                    break
                all_reviews.append({
                    'review': r.get('content'),
                    'rating': r.get('score'),
                    'date': r.get('at'),
                    'bank': bank_name,
                    'source': 'Google Play'
                })
                
            if not continuation_token:
                break
                
        except Exception as e:
            print(f"Error encountered while extracting data from {bank_name}: {e}")
            break
            
    df = pd.DataFrame(all_reviews)
    print(f"Successfully collected {len(df)} records for {bank_name}.\n")
    return df

def main():
    # FIXED: True production IDs active on Google Play Store
    target_apps = {
        'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
        'Bank of Abyssinia': 'com.boa.boaMobileBanking',
        'Dashen Bank': 'com.dashen.dbmobile'
    }
    
    aggregated_df = pd.DataFrame()
    
    for bank, app_id in target_apps.items():
        bank_df = scrape_bank_reviews(app_id, bank, target_count=500)
        aggregated_df = pd.concat([aggregated_df, bank_df], ignore_index=True)
        
    # Ensure data directory structures exist
    os.makedirs('data/raw', exist_ok=True)
    
    output_path = 'data/raw/raw_scraped_reviews.csv'
    aggregated_df.to_csv(output_path, index=False)
    print(f"Data pipeline step 1 complete. Raw asset stored at {output_path}")

if __name__ == "__main__":
    main()