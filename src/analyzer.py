import os
import pandas as pd
import spacy
from transformers import pipeline

print("Loading language models and tokenizers...")
# Load spaCy's English model for text normalization (lemmatization)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

print("Initializing DistilBERT deep learning sentiment pipeline...")
# Initialize Hugging Face Transformer sentiment analyzer pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncate=True
)

def clean_and_lemmatize(text):
    """
    Cleans text by converting to lowercase, removing stop words,
    and reducing words to their base form (e.g., 'crashing' -> 'crash').
    """
    if not isinstance(text, str) or text.strip() == "":
        return ""
    
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def analyze_sentiment_batch(texts):
    """
    Processes review texts through DistilBERT to classify sentiment.
    """
    results = []
    print("Running reviews through the transformer model...")
    for idx, text in enumerate(texts):
        if not isinstance(text, str) or text.strip() == "":
            results.append({'sentiment_label': 'NEUTRAL', 'sentiment_score': 0.5})
            continue
            
        try:
            prediction = sentiment_pipeline(text[:512])[0]
            results.append({
                'sentiment_label': prediction['label'],
                'sentiment_score': round(prediction['score'], 4)
            })
        except Exception as e:
            results.append({'sentiment_label': 'NEUTRAL', 'sentiment_score': 0.5})
            
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(texts)} reviews...")
            
    return pd.DataFrame(results)

def main():
    # Looking for the file from preprocess.py output
    input_path = 'data/raw/raw_scraped_reviews.csv'
    output_path = 'data/raw/analyzed_reviews.csv'
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Scraped dataset not found at {input_path}. Run scraper/preprocess scripts first.")
        
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} records for NLP processing.")
    
    # Drop rows missing review text
    df = df.dropna(subset=['review'])
    
    # 1. Create a unique ID tracking key for each review row
    df.insert(0, 'review_id', range(1, len(df) + 1))
    
    # 2. Clean text data
    print("Normalizing text data (removing stop words)...")
    df['processed_text'] = df['review'].apply(clean_and_lemmatize)
    
    # 3. Compute sentiment labels and scores
    sentiment_df = analyze_sentiment_batch(df['review'].tolist())
    df = pd.concat([df.reset_index(drop=True), sentiment_df.reset_index(drop=True)], axis=1)
    
    # 4. Map keywords to distinct business themes (Thematic Analysis KPI)
    def assign_theme(text):
        text = str(text).lower()
        if any(w in text for w in ['login', 'otp', 'password', 'sign', 'log', 'verification', 'account']):
            return 'Account Access Issues'
        elif any(w in text for w in ['transfer', 'send', 'money', 'payment', 'cbebirr', 'amole', 'pay', 'balance']):
            return 'Transaction Performance'
        elif any(w in text for w in ['ui', 'slow', 'crash', 'freeze', 'loading', 'error', 'bug', 'worst', 'network']):
            return 'App Stability & UI'
        elif any(w in text for w in ['feature', 'update', 'fingerprint', 'biometric', 'dark mode']):
            return 'Feature Requests'
        else:
            return 'General Feedback'

    print("Mapping reviews to specific app themes...")
    df['identified_theme'] = df['processed_text'].apply(assign_theme)
    
    # Reorganize matching the exact format requested by Task 2
    final_cols = ['review_id', 'review', 'rating', 'date', 'bank', 'source', 'sentiment_label', 'sentiment_score', 'identified_theme']
    df = df[final_cols]
    
    # Save the deep analytics data asset
    df.to_csv(output_path, index=False)
    print(f"\nTask 2 pipeline executed successfully! Analyzed dataset saved at {output_path}")
    print("\nTheme Breakdown Summary:")
    print(df['identified_theme'].value_counts())

if __name__ == "__main__":
    main()