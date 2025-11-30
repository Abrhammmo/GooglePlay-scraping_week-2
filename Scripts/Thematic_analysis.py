"""
Thematic Analysis Module
Author: Your Name
Description:
    This module performs thematic analysis on bank reviews.
    Steps:
        1. Text preprocessing (cleaning, tokenization, lemmatization, stopword removal)
        2. Keyword extraction (TF-IDF)
        3. Theme clustering (KMeans, 5 themes per bank)
        4. Returns processed DataFrame with theme labels
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are downloaded
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class ThematicAnalyzer:
    def __init__(self, n_themes=5):
        """
        Initialize the thematic analyzer

        Args:
            n_themes (int): Number of clusters/themes per bank
        """
        self.n_themes = n_themes
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = None
        self.kmeans_models = {}

    def preprocess_text(self, text):
        """Clean, tokenize, remove stopwords, and lemmatize"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(tok) for tok in tokens if tok not in self.stop_words]
        return " ".join(tokens)

    def extract_keywords(self, corpus, top_n=5):
        """
        Fit TF-IDF and extract top_n keywords per document
        """
        self.vectorizer = TfidfVectorizer(max_features=5000)
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        
        keywords_list = []
        for row in tfidf_matrix:
            # Get TF-IDF scores
            row_array = row.toarray().flatten()
            top_indices = row_array.argsort()[-top_n:][::-1]
            top_keywords = feature_names[top_indices]
            keywords_list.append(", ".join(top_keywords))
        
        return tfidf_matrix, keywords_list

    def cluster_themes(self, df, tfidf_matrix):
        """
        Cluster reviews into themes per bank
        """
        df['theme'] = ""
        # Process per bank
        for bank in df['bank_code'].unique():
            bank_mask = df['bank_code'] == bank
            bank_matrix = tfidf_matrix[bank_mask.values]
            if bank_matrix.shape[0] < self.n_themes:
                # Not enough reviews to form clusters
                df.loc[bank_mask, 'theme'] = "Theme_0"
                continue
            kmeans = KMeans(n_clusters=self.n_themes, random_state=42)
            labels = kmeans.fit_predict(bank_matrix)
            df.loc[bank_mask, 'theme'] = ["Theme_" + str(lbl) for lbl in labels]
            self.kmeans_models[bank] = kmeans
        return df

    def process(self, df):
        """
        Run full pipeline: preprocess, extract keywords, cluster themes
        """
        if df is None or df.empty:
            print("DataFrame is empty.")
            return df
        
        # Step 1: Preprocess review text
        print("Preprocessing review text...")
        df['cleaned_text'] = df['review_text'].apply(self.preprocess_text)
        
        # Step 2: Extract keywords
        print("Extracting keywords via TF-IDF...")
        tfidf_matrix, keywords = self.extract_keywords(df['cleaned_text'])
        df['keywords'] = keywords
        
        # Step 3: Cluster themes
        print(f"Clustering into {self.n_themes} themes per bank...")
        df = self.cluster_themes(df, tfidf_matrix)
        
        print("Thematic analysis complete.")
        return df
