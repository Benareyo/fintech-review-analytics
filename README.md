# Fintech Customer Experience Analytics Pipeline

A production-grade data engineering pipeline designed to scrape, clean, analyze, and structure user feedback from the Google Play Store for three major Ethiopian banking applications: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

---

## Task 1: Data Collection & Preprocessing Methodology

### Data Extraction Summary
* **Source:** Google Play Store marketplace entries.
* **Target Count:** Minimum 400 reviews per bank (Targeted: 500 per bank, 1,500 total sample size).
* **Language/Country Focus:** English (`en`) reviews pulled globally (`us` marketplace footprint extension) to ensure a stable dataset for NLP transformer tasks.

### Target Applications
| Bank | Package App ID | Target Volume |
| :--- | :--- | :--- |
| Commercial Bank of Ethiopia (CBE) | `com.combanketh.mobilebanking` | 500 |
| Bank of Abyssinia (BOA) | `com.boa.boaMobileBanking` | 500 |
| Dashen Bank | `com.dashen.dbmobile` | 500 |

### Preprocessing Protocol (`src/preprocess.py`)
1. **Data Integrity Check:** Dropped any rows missing critical textual feedback components or rating scores.
2. **Deduplication:** Cleared repeat review text inputs matching on identical user text values, timestamps, and target bank contexts.
3. **Date Standardization:** Transformed raw transaction execution timestamps into clear `YYYY-MM-DD` features using `pandas`.
4. **Storage Architecture:** Saved output directly to `data/raw/cleaned_reviews.csv` (properly isolated via `.gitignore`).

### Encountered Limitations
* **Marketplace Localization Filtering:** Initial localized query combinations (`lang='en'`, `country='et'`) produced limited data rows due to storefront labeling structures. Shifting parameters to a wider footprint successfully resolved the tracking limitations and guaranteed data volume requirements.

## Task 2: Sentiment and Thematic Analysis Insights

### Sentiment Tool Selection Rationale
For this analysis, we utilized `distilbert-base-uncased-finetuned-sst-2-english` over traditional rule-based lexicon models like VADER or TextBlob. While VADER operates with low computational overhead, it fails to capture deep semantic context, multi-word modifiers, or structural sarcasm common in financial services user reviews. DistilBERT leverages attention mechanisms to parse semantic context, ensuring a highly accurate 100% classification coverage across the text corpus.

### Thematic Analysis & Grouping Logic
Using linguistic tokenization and stop-word removal via `spaCy`, reviews were dynamically clustered into business-relevant operational pillars based on keyword matrices:
*   **Account Access Issues:** Triggered by critical login roadblocks (`login`, `otp`, `password`, `verification`, `code`).
*   **Transaction Performance:** Mapped to financial liquidity events (`transfer`, `send`, `money`, `payment`, `cbebirr`, `amole`, `balance`).
*   **App Stability & UI:** Captured systemic execution degradation (`slow`, `crash`, `freeze`, `bug`, `network`, `error`).
*   **Feature Requests:** Isolated user utility optimization trends (`biometric`, `update`, `dark mode`).

### Processing Distribution Summary
The pipeline successfully executed against the scraped review assets with the following categorical distribution:

| Identified Theme | Volumetric Count | Relational Weight |
| :--- | :--- | :--- |
| **General Feedback** | 847 | 84.7% |
| **App Stability & UI** | 50 | 5.0% |
| **Transaction Performance** | 43 | 4.3% |
| **Account Access Issues** | 38 | 3.8% |
| **Feature Requests** | 22 | 2.2% |
