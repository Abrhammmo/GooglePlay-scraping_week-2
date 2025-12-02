
# 📘 **Database Schema Documentation – `bank_reviews`**

This document describes the PostgreSQL schema used in the **Bank Reviews Sentiment & Thematic Analysis Project**.
The schema was exported using `pg_dump` and contains all database objects required to store:

* Bank metadata
* Positive reviews (with themes)
* Negative reviews (with themes)

The database supports analytics, dashboards, and downstream machine-learning tasks.

---

# 🏛 **Schema Overview**

The database contains **three main tables**:

1. **`banks`** – Bank metadata
2. **`positive_reviews_with_themes`** – Positive reviews + sentiment + themes
3. **`negative_reviews_with_themes`** – Negative reviews + sentiment + themes

All tables reside in the **public** schema.

A dedicated PostgreSQL schema named **`banks`** also exists with a descriptive comment, but the bank table itself is stored under `public`.

---

# 📄 **1. banks Table**

Stores static information about each bank.

### **Definition**

```sql
CREATE TABLE public.banks (
    bank_id VARCHAR(50) PRIMARY KEY,
    bank_name VARCHAR(50) NOT NULL,
    app_name VARCHAR(100) NOT NULL
);
```

### **Purpose**

* Maps bank codes (`CBE`, `BOA`, `DASHENBANK`) to their official names and app titles
* Supports joining reviews with bank metadata
* Acts as the dimension table in BI queries

---

# 🟩 **2. positive_reviews_with_themes Table**

Contains **processed positive reviews** with:

* Sentiment scoring
* Cleaned text
* Extracted keywords
* Assigned thematic cluster (`positivetheme_0`, `positivetheme_1`, etc.)

### **Definition**

```sql
CREATE TABLE public.positive_reviews_with_themes (
    review_id INTEGER PRIMARY KEY DEFAULT nextval('positive_reviews_with_themes_review_id_seq'),
    bank_id VARCHAR(50),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    bank_name VARCHAR(50),
    bank_code VARCHAR(50),
    source VARCHAR(50),
    sentiment_label VARCHAR(20),
    sentiment_score DOUBLE PRECISION,
    sentiment_group VARCHAR(20),
    cleaned_text TEXT,
    keywords TEXT,
    theme VARCHAR(100)
);
```

### **Purpose**

* Stores model-processed **positive** reviews
* Enables analysis such as:

  * Reasons for customer satisfaction
  * Most common positive themes
  * Positive trends over time
* Supports visualizations in Task 4

---

# 🟥 **3. negative_reviews_with_themes Table**

Contains **processed negative reviews** with:

* Sentiment scoring
* Cleaned text
* Extracted keywords
* Assigned thematic cluster (`negativetheme_0`, `negativetheme_1`, etc.)

### **Definition**

```sql
CREATE TABLE public.negative_reviews_with_themes (
    review_id INTEGER PRIMARY KEY DEFAULT nextval('negative_reviews_with_themes_review_id_seq'),
    bank_id VARCHAR(50),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    bank_name VARCHAR(50),
    bank_code VARCHAR(50),
    source VARCHAR(50),
    sentiment_label VARCHAR(20),
    sentiment_score DOUBLE PRECISION,
    sentiment_group VARCHAR(20),
    cleaned_text TEXT,
    keywords TEXT,
    theme VARCHAR(100)
);
```

### **Purpose**

* Stores model-processed **negative** reviews
* Enables analysis such as:

  * Customer pain points
  * System issues and user frustrations
  * Frequency of complaints by theme
  * Negative sentiment trends over time

---

# 🔢 **4. Sequences**

Two sequences automatically generate incremental IDs:

* `positive_reviews_with_themes_review_id_seq`
* `negative_reviews_with_themes_review_id_seq`

These ensure unique `review_id` values on insert.

---

# 🧩 **5. Constraints**

Each table includes a **PRIMARY KEY** constraint:

```sql
ALTER TABLE ONLY public.banks
    ADD CONSTRAINT banks_pkey PRIMARY KEY (bank_id);

ALTER TABLE ONLY public.positive_reviews_with_themes
    ADD CONSTRAINT positive_reviews_with_themes_pkey PRIMARY KEY (review_id);

ALTER TABLE ONLY public.negative_reviews_with_themes
    ADD CONSTRAINT negative_reviews_with_themes_pkey PRIMARY KEY (review_id);
```

This guarantees data integrity and indexing for faster queries.

---

# 📊 **6. How This Schema Supports the Project**

This schema enables:

### ✔ Efficient data retrieval for sentiment & theme analytics

### ✔ Smooth visualization workflows (Task 4)

### ✔ Clean separation of positive/negative datasets

### ✔ Fast SQL queries such as:

* Review counts per bank
* Average ratings
* Theme frequencies
* Trends by date

### ✔ Integration with dashboards (PowerBI, Streamlit, Tableau)

### ✔ Future ML tasks (recommendation systems, topic modeling)

---

# 📁 **7. File Location**

The schema is stored in:

```
/schema/bank_reviews_schema.sql
```

This file allows full reconstruction of the database on any machine.

---

# 🏁 **Conclusion**

This schema forms the backbone of your **Bank Reviews Analysis Pipeline**, ensuring that all scraped, cleaned, analyzed, and themed reviews are stored in a clear, structured, and query-optimized PostgreSQL database.

It supports:

* Task 3 — Storage
* Task 4 — Visualization
* Task 5 — Reporting
* Task 6 — ML integration

A robust and scalable foundation for your Final Year Project.
