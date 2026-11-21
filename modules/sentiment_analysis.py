"""
=============================================================================
Module: sentiment_analysis.py
Project: Social Media Analytics Using Python
Description:
    Performs Natural Language Processing (NLP) and Sentiment Analysis on social
    media posts. Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
    and TextBlob with robust fallback mechanisms to classify posts into
    Positive, Negative, and Neutral.
=============================================================================
"""

import re
import pandas as pd

# Attempt to import VADER and TextBlob gracefully
VADER_AVAILABLE = False
TEXTBLOB_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
    VADER_AVAILABLE = True
except ImportError:
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        vader_analyzer = SentimentIntensityAnalyzer()
        VADER_AVAILABLE = True
    except Exception:
        vader_analyzer = None
        VADER_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


# Lightweight built-in sentiment lexicon as an ultra-reliable offline fallback
BUILTIN_POSITIVE_WORDS = set([
    'good', 'great', 'excellent', 'amazing', 'love', 'loving', 'best', 'awesome',
    'fantastic', 'wonderful', 'happy', 'thrilled', 'excited', 'proud', 'success',
    'successful', 'blessed', 'gratitude', 'clean', 'perfect', 'flawlessly', 'inspiring',
    'innovation', 'promising', 'beautiful', 'phenomenal', 'enjoy', 'favorite', 'win',
    'winner', 'boost', 'delight', 'super', 'sweet', 'valuable', 'incredible', 'magic'
])

BUILTIN_NEGATIVE_WORDS = set([
    'bad', 'terrible', 'horrible', 'worst', 'hate', 'hating', 'broken', 'fail',
    'failure', 'failed', 'delay', 'delayed', 'frustrated', 'frustrating', 'disappointed',
    'disappointing', 'outage', 'downtime', 'bug', 'buggy', 'pain', 'painful', 'scam',
    'breach', 'ruined', 'awful', 'headache', 'slow', 'crash', 'crashed', 'annoying',
    'overpriced', 'complaint', 'throttle', 'throttling', 'drain', 'unacceptable'
])


def _clean_text_for_sentiment(text):
    """
    Cleans raw post text for sentiment analysis while preserving sentiment cues.
    Preserves exclamation points, question marks, and uppercase letters for VADER.
    """
    if not isinstance(text, str):
        return ""
    # Remove URL links
    cleaned = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove user mentions (@username)
    cleaned = re.sub(r'@\w+', '', cleaned)
    # Strip excess whitespace
    cleaned = cleaned.strip()
    return cleaned


def analyze_single_text(text):
    """
    Analyzes sentiment of a single piece of text.

    Parameters:
        text (str): The social media post text.

    Returns:
        dict: Sentiment classification, polarity score (-1.0 to 1.0),
              subjectivity score (0.0 to 1.0), and component scores.
    """
    cleaned = _clean_text_for_sentiment(text)
    if not cleaned:
        return {
            "sentiment": "Neutral",
            "polarity": 0.0,
            "subjectivity": 0.0,
            "pos_score": 0.0,
            "neg_score": 0.0,
            "neu_score": 1.0,
            "method": "None (Empty Text)"
        }

    # Method 1: VADER (Primary choice for social media text)
    if VADER_AVAILABLE and vader_analyzer is not None:
        scores = vader_analyzer.polarity_scores(cleaned)
        compound = scores['compound']
        
        # Calculate subjectivity via TextBlob if available
        subj = 0.5
        if TEXTBLOB_AVAILABLE:
            try:
                subj = round(TextBlob(cleaned).sentiment.subjectivity, 2)
            except Exception:
                subj = 0.5

        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "polarity": round(compound, 3),
            "subjectivity": subj,
            "pos_score": round(scores['pos'], 3),
            "neg_score": round(scores['neg'], 3),
            "neu_score": round(scores['neu'], 3),
            "method": "VADER Sentiment Intensity"
        }

    # Method 2: TextBlob (Secondary choice)
    if TEXTBLOB_AVAILABLE:
        blob = TextBlob(cleaned)
        polarity = round(blob.sentiment.polarity, 3)
        subjectivity = round(blob.sentiment.subjectivity, 3)

        if polarity > 0.05:
            sentiment = "Positive"
        elif polarity < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "pos_score": max(0.0, polarity),
            "neg_score": abs(min(0.0, polarity)),
            "neu_score": round(1.0 - abs(polarity), 2),
            "method": "TextBlob Lexicon"
        }

    # Method 3: Built-in Rule-Based Lexicon (Offline / Standalone Fallback)
    words = re.findall(r'\b\w+\b', cleaned.lower())
    pos_count = sum(1 for w in words if w in BUILTIN_POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in BUILTIN_NEGATIVE_WORDS)
    total_matches = pos_count + neg_count

    if total_matches == 0:
        polarity = 0.0
        sentiment = "Neutral"
    else:
        polarity = round((pos_count - neg_count) / max(total_matches, 1), 3)
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": 0.5,
        "pos_score": round(pos_count / max(len(words), 1), 3),
        "neg_score": round(neg_count / max(len(words), 1), 3),
        "neu_score": round(1.0 - (pos_count + neg_count) / max(len(words), 1), 3),
        "method": "Rule-Based Lexicon Fallback"
    }


def analyze_dataframe_sentiment(df):
    """
    Applies sentiment analysis across all posts in a social media DataFrame.

    Adds three columns to the DataFrame:
    - Sentiment: 'Positive', 'Negative', or 'Neutral'
    - Polarity_Score: Compound or polarity value (-1.0 to +1.0)
    - Subjectivity_Score: Subjectivity value (0.0 = Objective, 1.0 = Highly Subjective)

    Parameters:
        df (pd.DataFrame): Social media DataFrame with 'Post_Text' column.

    Returns:
        pd.DataFrame: Enriched DataFrame with sentiment columns.
    """
    enriched_df = df.copy()

    if 'Post_Text' not in enriched_df.columns:
        enriched_df['Sentiment'] = "Neutral"
        enriched_df['Polarity_Score'] = 0.0
        enriched_df['Subjectivity_Score'] = 0.5
        return enriched_df

    sentiments = []
    polarities = []
    subjectivities = []

    for text in enriched_df['Post_Text']:
        result = analyze_single_text(text)
        sentiments.append(result['sentiment'])
        polarities.append(result['polarity'])
        subjectivities.append(result['subjectivity'])

    enriched_df['Sentiment'] = sentiments
    enriched_df['Polarity_Score'] = polarities
    enriched_df['Subjectivity_Score'] = subjectivities

    return enriched_df


def get_sentiment_summary(df):
    """
    Calculates aggregate sentiment statistics from an analyzed DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Sentiment' column.

    Returns:
        dict: Sentiment counts, percentages, and Net Sentiment Score (NSS).
    """
    if df.empty or 'Sentiment' not in df.columns:
        return {
            "positive_count": 0, "negative_count": 0, "neutral_count": 0,
            "positive_pct": 0.0, "negative_pct": 0.0, "neutral_pct": 0.0,
            "net_sentiment_score": 0.0, "dominant_sentiment": "Neutral"
        }

    total = len(df)
    counts = df['Sentiment'].value_counts()
    
    pos = int(counts.get('Positive', 0))
    neg = int(counts.get('Negative', 0))
    neu = int(counts.get('Neutral', 0))

    pos_pct = round((pos / total) * 100, 1) if total > 0 else 0.0
    neg_pct = round((neg / total) * 100, 1) if total > 0 else 0.0
    neu_pct = round((neu / total) * 100, 1) if total > 0 else 0.0

    # Net Sentiment Score (NSS) = % Positive - % Negative
    net_sentiment_score = round(pos_pct - neg_pct, 1)

    # Determine dominant sentiment
    if pos >= neg and pos >= neu:
        dominant = "Positive"
    elif neg >= pos and neg >= neu:
        dominant = "Negative"
    else:
        dominant = "Neutral"

    return {
        "positive_count": pos,
        "negative_count": neg,
        "neutral_count": neu,
        "positive_pct": pos_pct,
        "negative_pct": neg_pct,
        "neutral_pct": neu_pct,
        "net_sentiment_score": net_sentiment_score,
        "dominant_sentiment": dominant
    }

