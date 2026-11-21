"""
=============================================================================
Module: data_processing.py
Project: Social Media Analytics Using Python
Description:
    Handles data ingestion, validation, cleaning, missing values, duplicates,
    feature engineering (engagement metrics), and text tokenization for hashtags
    and trending topics.
=============================================================================
"""

import re
import pandas as pd
import numpy as np


def load_data(file_or_path):
    """
    Loads social media dataset from a CSV file path or Streamlit UploadedFile.

    Parameters:
        file_or_path: str or UploadedFile
            The file path or file-like object of the CSV file.

    Returns:
        pd.DataFrame: Loaded raw DataFrame, or None if error occurs.
    """
    encodings = ['utf-8', 'latin1', 'utf-8-sig', 'cp1252']
    
    for encoding in encodings:
        try:
            if hasattr(file_or_path, 'seek'):
                file_or_path.seek(0)
            df = pd.read_csv(file_or_path, encoding=encoding)
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

    raise ValueError("Failed to decode CSV file with supported encodings (UTF-8, Latin1, CP1252).")


def clean_data(df):
    """
    Cleans raw social media dataset:
    - Normalizes column names
    - Fills missing values with sensible defaults
    - Removes duplicate rows
    - Converts Date column to datetime objects
    - Adds derived metrics: Total_Engagement and Engagement_Level

    Parameters:
        df (pd.DataFrame): Raw input dataframe.

    Returns:
        tuple (pd.DataFrame, dict): Cleaned dataframe and dictionary of cleaning stats.
    """
    # Create a copy to prevent modifying the original dataframe
    cleaned_df = df.copy()

    # Track data quality statistics
    initial_rows = len(cleaned_df)
    missing_before = int(cleaned_df.isnull().sum().sum())

    # Standardize column names (strip whitespace and normalize casing)
    cleaned_df.columns = [col.strip() for col in cleaned_df.columns]

    # Required column mapping helper for flexibility in uploaded CSVs
    col_mapping = {}
    for col in cleaned_df.columns:
        low = col.lower()
        if 'id' in low and 'post' in low:
            col_mapping[col] = 'Post_ID'
        elif 'user' in low:
            col_mapping[col] = 'Username'
        elif 'plat' in low:
            col_mapping[col] = 'Platform'
        elif 'text' in low or 'content' in low or 'post' in low:
            if 'id' not in low:
                col_mapping[col] = 'Post_Text'
        elif 'tag' in low:
            col_mapping[col] = 'Hashtags'
        elif 'like' in low:
            col_mapping[col] = 'Likes'
        elif 'comment' in low:
            col_mapping[col] = 'Comments'
        elif 'share' in low:
            col_mapping[col] = 'Shares'
        elif 'date' in low or 'time' in low:
            col_mapping[col] = 'Date'

    cleaned_df.rename(columns=col_mapping, inplace=True)

    # Ensure baseline required columns exist
    if 'Post_Text' not in cleaned_df.columns:
        # Fallback to the first object/text column
        obj_cols = cleaned_df.select_dtypes(include=['object']).columns
        if len(obj_cols) > 0:
            cleaned_df['Post_Text'] = cleaned_df[obj_cols[0]]
        else:
            cleaned_df['Post_Text'] = ""

    if 'Post_ID' not in cleaned_df.columns:
        cleaned_df['Post_ID'] = [f"POST_{i+1:04d}" for i in range(len(cleaned_df))]

    if 'Username' not in cleaned_df.columns:
        cleaned_df['Username'] = "Anonymous"

    if 'Platform' not in cleaned_df.columns:
        cleaned_df['Platform'] = "General"

    if 'Hashtags' not in cleaned_df.columns:
        cleaned_df['Hashtags'] = ""

    # Numeric engagement columns
    for num_col in ['Likes', 'Comments', 'Shares']:
        if num_col not in cleaned_df.columns:
            cleaned_df[num_col] = 0
        else:
            cleaned_df[num_col] = pd.to_numeric(cleaned_df[num_col], errors='coerce').fillna(0).astype(int)

    # Handle text missing values
    cleaned_df['Post_Text'] = cleaned_df['Post_Text'].fillna("").astype(str).str.strip()
    cleaned_df['Username'] = cleaned_df['Username'].fillna("Anonymous").astype(str).str.strip()
    cleaned_df['Platform'] = cleaned_df['Platform'].fillna("General").astype(str).str.strip()
    cleaned_df['Hashtags'] = cleaned_df['Hashtags'].fillna("").astype(str).str.strip()

    # Drop duplicate records based on Post_Text and Username
    duplicates_removed = int(cleaned_df.duplicated(subset=['Post_Text', 'Username']).sum())
    cleaned_df.drop_duplicates(subset=['Post_Text', 'Username'], keep='first', inplace=True)

    # Convert Date column
    if 'Date' in cleaned_df.columns:
        cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'], errors='coerce')
        # Fill missing dates with current timestamp
        cleaned_df['Date'] = cleaned_df['Date'].fillna(pd.Timestamp.now())
    else:
        cleaned_df['Date'] = pd.Timestamp.now()

    # Derived Feature Engineering:
    # 1. Total Engagement = Likes + Comments + Shares
    cleaned_df['Total_Engagement'] = (
        cleaned_df['Likes'] + cleaned_df['Comments'] + cleaned_df['Shares']
    )

    # 2. Engagement Level (Categorical: Low, Medium, High)
    # Using dynamic percentiles with safe fallbacks
    p33 = cleaned_df['Total_Engagement'].quantile(0.33)
    p66 = cleaned_df['Total_Engagement'].quantile(0.66)

    def categorize_engagement(val):
        if val <= p33:
            return 'Low'
        elif val <= p66:
            return 'Medium'
        else:
            return 'High'

    cleaned_df['Engagement_Level'] = cleaned_df['Total_Engagement'].apply(categorize_engagement)

    # Reset index
    cleaned_df.reset_index(drop=True, inplace=True)

    cleaning_stats = {
        "initial_rows": initial_rows,
        "final_rows": len(cleaned_df),
        "missing_values_handled": missing_before,
        "duplicates_removed": duplicates_removed
    }

    return cleaned_df, cleaning_stats


def get_summary_metrics(df):
    """
    Calculates key Big Data analytics metrics from the dataset.

    Parameters:
        df (pd.DataFrame): Cleaned social media dataframe.

    Returns:
        dict: High-level KPI metrics.
    """
    total_posts = len(df)
    total_likes = int(df['Likes'].sum()) if total_posts > 0 else 0
    total_comments = int(df['Comments'].sum()) if total_posts > 0 else 0
    total_shares = int(df['Shares'].sum()) if total_posts > 0 else 0
    total_engagement = int(df['Total_Engagement'].sum()) if total_posts > 0 else 0

    avg_likes = round(float(df['Likes'].mean()), 2) if total_posts > 0 else 0.0
    avg_comments = round(float(df['Comments'].mean()), 2) if total_posts > 0 else 0.0
    avg_shares = round(float(df['Shares'].mean()), 2) if total_posts > 0 else 0.0
    avg_engagement = round(float(df['Total_Engagement'].mean()), 2) if total_posts > 0 else 0.0

    unique_users = int(df['Username'].nunique()) if total_posts > 0 else 0
    unique_platforms = int(df['Platform'].nunique()) if total_posts > 0 else 0

    return {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_engagement": total_engagement,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
        "avg_shares": avg_shares,
        "avg_engagement": avg_engagement,
        "unique_users": unique_users,
        "unique_platforms": unique_platforms
    }


def get_top_active_users(df, top_n=10):
    """
    Computes user activity and engagement rankings.

    Parameters:
        df (pd.DataFrame): Cleaned social media dataframe.
        top_n (int): Number of top users to retrieve.

    Returns:
        pd.DataFrame: Top users sorted by post count and total engagement.
    """
    if df.empty:
        return pd.DataFrame(columns=['Username', 'Post_Count', 'Total_Likes', 'Total_Engagement', 'Avg_Engagement'])

    user_stats = df.groupby('Username').agg(
        Post_Count=('Post_ID', 'count'),
        Total_Likes=('Likes', 'sum'),
        Total_Comments=('Comments', 'sum'),
        Total_Shares=('Shares', 'sum'),
        Total_Engagement=('Total_Engagement', 'sum')
    ).reset_index()

    user_stats['Avg_Engagement'] = (user_stats['Total_Engagement'] / user_stats['Post_Count']).round(2)
    user_stats = user_stats.sort_values(by=['Post_Count', 'Total_Engagement'], ascending=[False, False])
    return user_stats.head(top_n).reset_index(drop=True)


def extract_hashtags(df):
    """
    Extracts, normalizes, and counts hashtags across the dataset.
    Extracts both from the dedicated 'Hashtags' column and directly from 'Post_Text'.

    Parameters:
        df (pd.DataFrame): Cleaned social media dataframe.

    Returns:
        pd.DataFrame: DataFrame containing 'Hashtag' and 'Count', sorted descending.
    """
    all_hashtags = []

    # 1. From Hashtags column
    if 'Hashtags' in df.columns:
        for tags in df['Hashtags'].dropna():
            # Split by comma or whitespace
            parts = re.split(r'[, ]+', str(tags))
            for p in parts:
                cleaned_tag = p.strip().lower()
                if cleaned_tag.startswith('#') and len(cleaned_tag) > 1:
                    all_hashtags.append(cleaned_tag)
                elif cleaned_tag and not cleaned_tag.startswith('#') and len(cleaned_tag) > 1:
                    all_hashtags.append(f"#{cleaned_tag}")

    # 2. From Post_Text column (capturing inline hashtags like #AI, #Python)
    if 'Post_Text' in df.columns:
        for text in df['Post_Text'].dropna():
            found = re.findall(r'#\w+', str(text).lower())
            all_hashtags.extend(found)

    if not all_hashtags:
        return pd.DataFrame(columns=['Hashtag', 'Count'])

    tag_series = pd.Series(all_hashtags).value_counts().reset_index()
    tag_series.columns = ['Hashtag', 'Count']
    return tag_series


# Comprehensive list of standard English stopwords for text frequency analysis
STOPWORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
    't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd',
    'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",
    'also', 'get', 'got', 'like', 'one', 'would', 'make', 'know', 'see', 'us'
])


def get_trending_words(df, top_n=20):
    """
    Cleans post text, filters out URLs, punctuation, and stopwords, and computes
    the most frequently used trending words.

    Parameters:
        df (pd.DataFrame): Cleaned social media dataframe.
        top_n (int): Number of top trending words to return.

    Returns:
        pd.DataFrame: Top words and their frequencies.
    """
    if df.empty or 'Post_Text' not in df.columns:
        return pd.DataFrame(columns=['Word', 'Frequency'])

    all_words = []

    for text in df['Post_Text'].dropna():
        # Remove URLs (http, https, www)
        text_clean = re.sub(r'https?://\S+|www\.\S+', '', str(text))
        # Remove hashtags and mentions so only raw words remain
        text_clean = re.sub(r'[@#]\w+', '', text_clean)
        # Remove non-alphabetical characters
        text_clean = re.sub(r'[^a-zA-Z\s]', '', text_clean)
        
        # Tokenize and filter stopwords
        words = text_clean.lower().split()
        filtered = [w for w in words if len(w) > 2 and w not in STOPWORDS]
        all_words.extend(filtered)

    if not all_words:
        return pd.DataFrame(columns=['Word', 'Frequency'])

    word_series = pd.Series(all_words).value_counts().reset_index()
    word_series.columns = ['Word', 'Frequency']
    return word_series.head(top_n)

