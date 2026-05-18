import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Database Connection Setup
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/bank_reviews"
engine = create_engine(DATABASE_URL)

# Ensure output directory exists
os.makedirs("notebooks/plots", exist_ok=True)

def load_data():
    query = """
        SELECT r.*, b.bank_name 
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def plot_sentiment_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Calculate counts for stacked bar representation
    sentiment_counts = df.groupby(['bank_name', 'sentiment_label']).size().unstack(fill_value=0)
    sentiment_pct = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100
    
    sentiment_pct.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#e74c3c', '#95a5a6', '#2ecc71'])
    plt.title("Sentiment Label Distribution Across Ethiopian Retail Banking Apps", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Banking Institution", fontsize=12)
    plt.ylabel("Percentage Coverage (%)", fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title="Sentiment Classification", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("notebooks/plots/sentiment_distribution.png", dpi=300)
    plt.close()
    print("📈 Saved: notebooks/plots/sentiment_distribution.png")

def plot_rating_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='bank_name', y='rating', data=df, palette='Set2', hue='bank_name', legend=False)
    plt.title("Review Rating Distribution Across Target Applications", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Banking Institution", fontsize=12)
    plt.ylabel("App Store Star Rating (1-5)", fontsize=12)
    plt.tight_layout()
    plt.savefig("notebooks/plots/rating_distribution.png", dpi=300)
    plt.close()
    print("📈 Saved: notebooks/plots/rating_distribution.png")

def plot_theme_frequencies(df):
    plt.figure(figsize=(12, 6))
    theme_counts = df.groupby(['bank_name', 'identified_theme']).size().unstack(fill_value=0)
    
    theme_counts.plot(kind='bar', figsize=(12, 6), cmap='viridis')
    plt.title("Categorized Operational Pillars & Feature Concerns by Bank", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Banking Institution", fontsize=12)
    plt.ylabel("Total Review Mentions (Volume)", fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title="Identified Theme Cluster", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("notebooks/plots/theme_frequencies.png", dpi=300)
    plt.close()
    print("📈 Saved: notebooks/plots/theme_frequencies.png")

if __name__ == "__main__":
    print("🎨 Initializing pipeline visualization generation suite...")
    data = load_data()
    if not data.empty:
        plot_sentiment_distribution(data)
        plot_rating_distribution(data)
        plot_theme_frequencies(data)
        print("🎉 All 3 analytical visualizations exported successfully!")
    else:
        print("❌ Error: No database entries found to visualize.")