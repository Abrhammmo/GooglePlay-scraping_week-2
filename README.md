
# Ethiopian Mobile Banking App Reviews Analysis

## Overview

This project scrapes user reviews from **three Ethiopian mobile banking apps** (BOA, CBE, Dashen Bank) and performs comprehensive preprocessing to prepare the data for analysis. The goal is to create a clean dataset suitable for sentiment analysis, visualization, and other downstream analytics.

---

## Project Structure

* **scraping/**: Contains the Python scripts for scraping reviews from Google Play Store.
* **data/raw/raw_reviews.csv**: Raw scraped review data.
* **data/processed/cleaned_reviews.csv**: Preprocessed and cleaned dataset ready for analysis.
* **preprocessing/**: Contains the `ReviewPreprocessor` class and pipeline.
* **visualizations/**: Folder for generated graphs and charts (optional).
* **config.py**: Configuration file specifying paths and other constants.

---

## Goal 1: Scraping Reviews

The scraping script collects:

* **review_text**: Text content of the review
* **rating**: Star rating (1-5)
* **review_date**: Date of the review
* **bank_name / bank_code**: Bank identifiers
* **user_name**: Name of the reviewer
* **thumbs_up**: Number of likes/upvotes
* **reply_content**: Bank reply, if any
* **source**: Source platform (Google Play)

The script ensures that all data is aggregated into a **single raw CSV**.

---

## Goal 2: Preprocessing

The `ReviewPreprocessor` class performs the following steps:

1. **Load raw data**: Reads the CSV file containing scraped reviews.
2. **Check for missing data**: Identifies missing values in critical columns (`review_text`, `rating`, `bank_name`) and logs statistics.
3. **Handle missing values**:

   * Drops rows missing critical information.
   * Fills `user_name` with `'Anonymous'`, `thumbs_up` with `0`, and `reply_content` with empty strings.
4. **Normalize dates**: Converts `review_date` into `YYYY-MM-DD` format and extracts `review_year` and `review_month`.
5. **Clean review text**:

   * Removes extra spaces and leading/trailing whitespace.
   * Drops empty reviews.
   * Computes `text_length` for analysis.
6. **Validate ratings**: Ensures ratings are within the 1-5 range; invalid rows are removed.
7. **Prepare final output**:

   * Reorders columns: `review_id`, `review_text`, `rating`, `review_date`, `review_year`, `review_month`, `bank_code`, `bank_name`, `user_name`, `thumbs_up`, `text_length`, `source`.
   * Sorts by `bank_code` and `review_date`.
   * Resets the index for clean output.
8. **Save processed data**: Writes cleaned data to CSV (`data/processed/cleaned_reviews.csv`).
9. **Generate preprocessing report**:

   * Summarizes number of records removed at each step.
   * Shows distribution per bank, rating distribution, and text statistics.
   * Computes data retention and error rates.

---

## Goal 3: Additional Cleaning and Analysis (Optional)

* **Remove duplicate rows**: Ensures no repeated reviews remain.
* **Filter non-English reviews**: Uses `langdetect` to keep only English reviews.
* **Per-bank summaries**: Generate descriptive statistics and plots by `bank_code`.
* **Visualizations**: Create bar charts, rating distributions, and other exploratory charts for insights.


## Notes

* All steps are **modular**: new preprocessing steps or filters can be added easily.
* The preprocessing pipeline is **robust** against missing or malformed data.
* This dataset is now ready for **machine learning**, **text analysis**, or **dashboard visualizations**.

## Task 2 – Thematic Analysis of Bank Reviews

This task focuses on analyzing user reviews for multiple banks to identify recurring themes, extract insights, and provide actionable recommendations for improving user experience.


Steps Performed

* Data Preprocessing

Cleaned, normalized, and tokenized review text.

Removed noise such as special characters, stopwords, and irrelevant content to ensure high-quality input for analysis.

* Theme Clustering

Applied TF-IDF vectorization to convert reviews into numerical features.

Used KMeans clustering to group reviews into 5 meaningful themes for each bank.

* Keyword Extraction

Identified the top keywords for each theme to summarize the main topics discussed by users.

* Visualization

Created plots showing keywords per theme for each bank, enabling quick interpretation of user feedback.

* Cross-Bank Comparison

Compared themes across banks to identify common strengths, weaknesses, and areas for improvement.

* Actionable Insights

Highlighted recurring complaints, such as transaction issues and login errors.

Identified praised features, including smooth UI and fast processing times.

* Scalability

The pipeline can handle incoming review data, automatically categorizing new reviews and updating visualizations.

* Output

CSV files containing keywords, theme clusters, and review counts.

Visualizations for each bank showing key themes and associated keywords.

Comparative insights across banks to guide strategic improvements in user experience.

# 📌 Task 3 – Database Storage & Integration

## **Overview**

Task 3 focuses on storing the processed sentiment and thematic analysis results into a PostgreSQL database.
After completing data scraping (Task 1) and thematic analysis (Task 2), this task ensures the processed outputs are structured, validated, and stored in a relational database for analytics, dashboards, or future machine-learning applications.

This step involved:

* Creating a PostgreSQL schema for storing review datasets
* Preparing cleaned CSV outputs (`positive_reviews_with_themes.csv` and `negative_reviews_with_themes.csv`)
* Writing a Python script to automatically:

  * Connect to PostgreSQL
  * Create required tables
  * Load and insert cleaned data
  * Prevent duplicate records using conflict handling (`ON CONFLICT DO NOTHING`)
* Exporting the database schema into a GitHub-ready SQL dump folder

---

## **Pipeline Summary**

### **1. Input Files**

The two datasets generated from Task 2:

* `positive_reviews_with_themes.csv`
* `negative_reviews_with_themes.csv`

These files include:

| Column          | Description                      |
| --------------- | -------------------------------- |
| review_id       | Unique review identifier         |
| bank_id         | Bank reference ID                |
| review_text     | Raw review text                  |
| rating          | Star rating (1–5)                |
| review_date     | Review timestamp                 |
| bank_name       | Bank’s name                      |
| bank_code       | Bank identifier (e.g., CBE, BOA) |
| source          | Data source (Google Play Store)  |
| sentiment_label | Positive / Negative / Neutral    |
| sentiment_score | Polarity score                   |
| sentiment_group | Grouped sentiment category       |
| cleaned_text    | Preprocessed review text         |
| keywords        | Extracted keywords (TF-IDF)      |
| theme           | Assigned theme label             |

---

## **2. Output Tables (Created Automatically)**

The script creates:

### **`positive_reviews_with_themes`**

Contains all positive-sentiment thematic results
(Themes: `positivetheme_0` → `positivetheme_3`)

### **`negative_reviews_with_themes`**

Contains all negative-sentiment thematic results
(Themes: `negativetheme_0` → `negativetheme_2`)

Each table is created automatically if it does not already exist.

---

## **3. PostgreSQL Storage Script**

A standalone script (`store_reviews_postgres.py`) was created to handle:

✔ Connecting to PostgreSQL
✔ Table creation with correct schema
✔ Reading CSV files from the `../output/` directory
✔ Inserting all rows with conflict handling
✔ Closing connections safely

This script allows easy re-runs and clean integration in production pipelines.

---

## **4. Exporting the Database Schema**

A `schema/` folder was created inside the repository where:

* `schema.sql`
* `bank_reviews_schema.sql`

were exported using:

```bash
pg_dump -U postgres -h localhost -p 5433 -d bank_reviews -s > schema/bank_reviews_schema.sql
```

These files allow full database reconstruction on any machine.

---

## **5. Verification Queries**

Useful SQL checks included:

```sql
SELECT COUNT(*) FROM positive_reviews_with_themes;
SELECT COUNT(*) FROM negative_reviews_with_themes;

SELECT bank_name, COUNT(*) 
FROM positive_reviews_with_themes 
GROUP BY bank_name;

SELECT bank_name, AVG(rating)
FROM negative_reviews_with_themes
GROUP BY bank_name;
```

These queries verify the accuracy and consistency of the inserted data.

---

## **Conclusion**

Task 3 successfully integrates all processed sentiment and thematic datasets into a structured PostgreSQL database.
This creates a reliable backend foundation for:

* Dashboards
* Reporting
* Advanced analytics
* Recommendation system input (Final Year Project)

The workflow is now production-ready and can be fully automated.


