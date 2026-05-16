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