
# 🏦 Customer Experience Analytics for Ethiopian Fintech Apps

## 💡 Challenge Overview

This project addresses a real-world data engineering and analysis challenge to assess customer satisfaction for three major Ethiopian mobile banking applications by scraping, processing, analyzing, and visualizing user reviews from the **Google Play Store**.

As a **Data Analyst** at **Omega Consultancy**, the objective is to provide data-driven insights and actionable recommendations to **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank** to help them enhance their mobile app user experience, improve retention, and foster feature innovation.

-----

## 🎯 Business Objectives & Scenarios

The analysis is guided by core fintech priorities, simulating real consulting tasks:

  * **Scenario 1: Retaining Users**
      * **Objective:** Analyze the prevalence of critical pain points (e.g., slow transfers) across all banks and suggest areas for technical investigation.
  * **Scenario 2: Enhancing Features**
      * **Objective:** Extract desired features (e.g., fingerprint login, budgeting tools) and competitive gaps through thematic and keyword analysis.
  * **Scenario 3: Managing Complaints**
      * **Objective:** Cluster recurring complaints (e.g., “login error”) to inform strategies for AI chatbot integration and faster support resolution.

-----

## 🛠️ Project Architecture & Methodology

The project follows a standard data pipeline workflow: **Scraping** $\rightarrow$ **Preprocessing/NLP** $\rightarrow$ **Storage** $\rightarrow$ **Analysis/Reporting**.

### ⚙️ Technologies Used

  * **Web Scraping:** Python (e.g., `google-play-scraper`)
  * **Data Processing:** Python (`pandas`, `numpy`)
  * **Natural Language Processing (NLP):**
      * **Sentiment:** `distilbert-base-uncased-finetuned-sst-2-english` (or VADER/TextBlob fallback)
      * **Thematic Analysis:** `spaCy`, `scikit-learn` (TF-IDF)
  * **Database:** **PostgreSQL** (`psycopg2` or `SQLAlchemy`)
  * **Visualization:** `Matplotlib`, `Seaborn`
  * **Version Control:** **Git/GitHub**


## 📝 Task-Specific Implementation & Status

### **Task 1: Data Collection and Preprocessing**

  * **Objective:** Collect $\text{1200+ reviews}$ ($\text{400+ per bank}$) and clean the data.
  * **Implementation:** Used the `google-play-scraper` library. Handled duplicates and missing data, and normalized dates to `YYYY-MM-DD`.
  * **Status:** **Complete**. Cleaned data is saved to `data/processed_reviews.csv`.

### **Task 2: Sentiment and Thematic Analysis**

  * **Objective:** Quantify sentiment and extract $\text{3-5 actionable themes}$ per bank.
  * **Implementation:** Sentiment scores calculated using a fine-tuned DistilBERT model. $\text{TF-IDF}$ and $\text{spaCy}$ used to extract keywords and cluster them into themes like 'Transaction Performance', 'User Interface', and 'Account Access'.
  * **Status:** **Complete**. Sentiment scores and theme labels are integrated into the dataset.

### **Task 3: Store Cleaned Data in PostgreSQL**

  * **Objective:** Design and implement a relational database to store the processed data for persistent management.
  * **Schema:** Two tables: **`banks`** (PK: `bank_id`) and **`reviews`** (PK: `review_id`, FK: `bank_id`).
  * **Implementation:** A Python script using `psycopg2` handles the database creation and bulk insertion of over $\text{1,000}$ review records.
  * **Status:** **Complete**. Database `bank_reviews` is populated and verified.

### **Task 4: Insights and Recommendations**

  * **Objective:** Derive actionable insights, compare banks, and deliver $\text{2+}$ improvements per bank.
  * **Implementation:** Analysis focuses on linking low ratings/negative sentiment to specific themes/keywords to identify pain points (e.g., crashes) and drivers (e.g., good UI). $\text{3-5 core visualizations}$ generated.
  * **Status:** **Pending Final Report Generation**. Analysis and visualizations are ready for inclusion in the final report (`final_report.pdf`).

