import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def generate_and_save_plots():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files and os.path.exists('data'):
        csv_files = [os.path.join('data', f) for f in os.listdir('data') if f.endswith('.csv')]
        
    if not csv_files:
        print("❌ Error: Missing source CSV files for rendering.")
        return
        
    df = pd.read_csv(csv_files[0])
    os.makedirs("notebooks/plots", exist_ok=True)
    
    df.columns = [col.lower().strip() for col in df.columns]
    bank_col = 'bank_name' if 'bank_name' in df.columns else ('bank' if 'bank' in df.columns else None)
    sentiment_col = 'sentiment_label' if 'sentiment_label' in df.columns else ('sentiment' if 'sentiment' in df.columns else None)
    rating_col = 'rating'
    theme_col = 'identified_theme' if 'identified_theme' in df.columns else ('theme' if 'theme' in df.columns else None)

    print("🚀 Running visualization rendering matrices...")

    if bank_col and sentiment_col:
        plt.figure(figsize=(10, 6))
        matrix = pd.crosstab(df[bank_col], df[sentiment_col], normalize='index') * 100
        matrix.plot(kind='bar', stacked=True, color=['#e11d48', '#16a34a'], ax=plt.gca())
        plt.title('Fintech App Sentiment Distribution Matrix', fontsize=12, fontweight='bold')
        plt.ylabel('Percentage Proportion (%)')
        plt.tight_layout()
        plt.savefig('notebooks/plots/sentiment_distribution.png', dpi=300)
        plt.close()
        print("  ✅ Metric Chart 1 Saved: notebooks/plots/sentiment_distribution.png")

    if bank_col and rating_col in df.columns:
        plt.figure(figsize=(9, 5))
        sns.boxplot(x=bank_col, y=rating_col, data=df, palette='Set2')
        plt.title('App Store Star Rating Polarization Spread', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.savefig('notebooks/plots/rating_distribution.png', dpi=300)
        plt.close()
        print("  ✅ Metric Chart 2 Saved: notebooks/plots/rating_distribution.png")

    if theme_col and bank_col:
        plt.figure(figsize=(11, 6))
        sns.countplot(x=theme_col, hue=bank_col, data=df, palette='muted')
        plt.title('Volumetric Frequency of Identified Technical Themes', fontsize=12, fontweight='bold')
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig('notebooks/plots/theme_frequencies.png', dpi=300)
        plt.close()
        print("  ✅ Metric Chart 3 Saved: notebooks/plots/theme_frequencies.png")

if __name__ == "__main__":
    generate_and_save_plots()
