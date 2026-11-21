"""
=============================================================================
Module: visualization.py
Project: Social Media Analytics Using Python
Description:
    Generates rich, modern, interactive visualizations using Plotly, Matplotlib,
    and Seaborn. Adheres to a professional blue and purple theme with clean
    light-mode aesthetics.
=============================================================================
"""

import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Optional wordcloud support with graceful fallback
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False


# Theme Color Constants (Blue & Purple modern palette)
COLOR_PRIMARY_BLUE = "#4A00E0"
COLOR_PRIMARY_PURPLE = "#8E2DE2"
COLOR_ACCENT_CYAN = "#00CEC9"
COLOR_ACCENT_VIOLET = "#6C5CE7"
COLOR_BG_LIGHT = "#FFFFFF"

# Standard Sentiment Colors
SENTIMENT_COLOR_MAP = {
    "Positive": "#00B894",  # Emerald Green
    "Neutral": "#0984E3",   # Professional Blue
    "Negative": "#D63031"   # Crimson Red
}


def plot_sentiment_pie(df):
    """
    Creates an interactive Plotly donut chart displaying sentiment distribution.
    """
    if df.empty or 'Sentiment' not in df.columns:
        return go.Figure()

    counts = df['Sentiment'].value_counts().reset_index()
    counts.columns = ['Sentiment', 'Count']

    fig = px.pie(
        counts,
        names='Sentiment',
        values='Count',
        color='Sentiment',
        color_discrete_map=SENTIMENT_COLOR_MAP,
        hole=0.55,
        title="<b>Sentiment Distribution Overview</b>"
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436", family="Arial"),
        font=dict(family="Arial", size=13),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=30),
        height=380
    )
    return fig


def plot_sentiment_bar(df):
    """
    Creates an interactive bar chart of sentiment counts.
    """
    if df.empty or 'Sentiment' not in df.columns:
        return go.Figure()

    counts = df['Sentiment'].value_counts().reset_index()
    counts.columns = ['Sentiment', 'Count']

    fig = px.bar(
        counts,
        x='Sentiment',
        y='Count',
        color='Sentiment',
        color_discrete_map=SENTIMENT_COLOR_MAP,
        text='Count',
        title="<b>Sentiment Frequency Count</b>"
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker=dict(line=dict(color='#2D3436', width=1))
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436", family="Arial"),
        font=dict(family="Arial", size=13),
        xaxis_title="<b>Sentiment Category</b>",
        yaxis_title="<b>Number of Posts</b>",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        height=380
    )
    return fig


def plot_sentiment_by_platform(df):
    """
    Creates a grouped bar chart comparing sentiment distribution across platforms.
    """
    if df.empty or 'Platform' not in df.columns or 'Sentiment' not in df.columns:
        return go.Figure()

    grouped = df.groupby(['Platform', 'Sentiment']).size().reset_index(name='Count')

    fig = px.bar(
        grouped,
        x='Platform',
        y='Count',
        color='Sentiment',
        barmode='group',
        color_discrete_map=SENTIMENT_COLOR_MAP,
        title="<b>Sentiment Comparison Across Social Platforms</b>"
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Platform</b>",
        yaxis_title="<b>Number of Posts</b>",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=20),
        height=400
    )
    return fig


def plot_likes_comments_shares(df):
    """
    Creates a multi-dimensional interactive scatter plot comparing Likes vs Comments
    with bubble size proportional to Shares and color-coded by Sentiment.
    """
    if df.empty:
        return go.Figure()

    # Safety clipping for bubble sizes
    marker_sizes = np.clip(df['Shares'] / (df['Shares'].max() + 1) * 35, 8, 40)

    fig = px.scatter(
        df,
        x='Likes',
        y='Comments',
        size=marker_sizes,
        color='Sentiment' if 'Sentiment' in df.columns else 'Platform',
        color_discrete_map=SENTIMENT_COLOR_MAP,
        hover_data=['Username', 'Platform', 'Shares'],
        title="<b>Engagement Matrix: Likes vs. Comments (Bubble Size = Shares)</b>"
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Total Likes</b>",
        yaxis_title="<b>Total Comments</b>",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=40),
        height=430
    )
    return fig


def plot_top_hashtags(hashtag_df, top_n=10):
    """
    Creates a horizontal bar chart displaying top trending hashtags.
    """
    if hashtag_df.empty:
        return go.Figure()

    top_df = hashtag_df.head(top_n).sort_values(by='Count', ascending=True)

    fig = px.bar(
        top_df,
        x='Count',
        y='Hashtag',
        orientation='h',
        color='Count',
        color_continuous_scale=[[0, '#8E2DE2'], [1, '#4A00E0']],
        text='Count',
        title=f"<b>Top {top_n} Trending Hashtags</b>"
    )

    fig.update_traces(
        textposition='outside',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Mention Frequency</b>",
        yaxis_title="<b>Hashtag</b>",
        coloraxis_showscale=False,
        margin=dict(l=20, r=30, t=50, b=20),
        height=420
    )
    return fig


def plot_top_words(words_df, top_n=15):
    """
    Creates an interactive bar chart of top trending words.
    """
    if words_df.empty:
        return go.Figure()

    top_df = words_df.head(top_n).sort_values(by='Frequency', ascending=True)

    fig = px.bar(
        top_df,
        x='Frequency',
        y='Word',
        orientation='h',
        color='Frequency',
        color_continuous_scale=[[0, '#6C5CE7'], [1, '#00CEC9']],
        text='Frequency',
        title=f"<b>Top {top_n} Frequently Used Words</b>"
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Word Count Frequency</b>",
        yaxis_title="<b>Word</b>",
        coloraxis_showscale=False,
        margin=dict(l=20, r=30, t=50, b=20),
        height=420
    )
    return fig


def plot_engagement_distribution(df):
    """
    Creates an interactive box plot and violin plot showing engagement by platform.
    """
    if df.empty or 'Platform' not in df.columns or 'Total_Engagement' not in df.columns:
        return go.Figure()

    fig = px.box(
        df,
        x='Platform',
        y='Total_Engagement',
        color='Platform',
        points="all",
        color_discrete_sequence=['#4A00E0', '#8E2DE2', '#0984E3', '#00CEC9'],
        title="<b>User Engagement Distribution Across Platforms</b>"
    )

    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Platform</b>",
        yaxis_title="<b>Total Engagement (Likes + Comments + Shares)</b>",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        height=400
    )
    return fig


def plot_engagement_over_time(df):
    """
    Creates a time-series area/line chart showing daily engagement trends.
    """
    if df.empty or 'Date' not in df.columns or 'Total_Engagement' not in df.columns:
        return go.Figure()

    temp_df = df.copy()
    temp_df['Day'] = temp_df['Date'].dt.date
    daily = temp_df.groupby('Day').agg(
        Total_Engagement=('Total_Engagement', 'sum'),
        Posts_Count=('Post_ID', 'count')
    ).reset_index()

    fig = px.area(
        daily,
        x='Day',
        y='Total_Engagement',
        title="<b>Total User Engagement Trend Over Time</b>",
        color_discrete_sequence=['#6C5CE7']
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Daily Engagement</b>",
        margin=dict(l=20, r=20, t=50, b=20),
        height=380
    )
    return fig


def plot_top_active_users(user_df, top_n=10):
    """
    Creates a bar chart showcasing the most active social media users.
    """
    if user_df.empty:
        return go.Figure()

    top_users = user_df.head(top_n).sort_values(by='Post_Count', ascending=True)

    fig = px.bar(
        top_users,
        x='Post_Count',
        y='Username',
        orientation='h',
        color='Total_Engagement',
        color_continuous_scale=[[0, '#8E2DE2'], [1, '#4A00E0']],
        text='Post_Count',
        title=f"<b>Top {top_n} Most Active Users by Post Count</b>"
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=18, color="#2D3436"),
        xaxis_title="<b>Number of Posts Created</b>",
        yaxis_title="<b>Username</b>",
        margin=dict(l=20, r=30, t=50, b=20),
        height=400
    )
    return fig


def generate_wordcloud_figure(text_or_df):
    """
    Generates a Matplotlib WordCloud figure. If wordcloud library is not installed,
    returns a clean Matplotlib bar chart placeholder.

    Parameters:
        text_or_df (str or pd.DataFrame): Text string or DataFrame containing 'Post_Text'.

    Returns:
        matplotlib.figure.Figure: Generated Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')

    if isinstance(text_or_df, pd.DataFrame):
        if 'Post_Text' in text_or_df.columns:
            combined_text = " ".join(text_or_df['Post_Text'].dropna().astype(str))
        else:
            combined_text = ""
    else:
        combined_text = str(text_or_df)

    # Clean text: remove URLs and mentions
    combined_text = re.sub(r'https?://\S+|www\.\S+|@\w+|[^\w\s]', ' ', combined_text)

    if not combined_text.strip():
        ax.text(0.5, 0.5, "No text available for Word Cloud", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig

    if WORDCLOUD_AVAILABLE:
        try:
            wc = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='viridis',
                max_words=80,
                contour_width=1,
                contour_color='#6C5CE7'
            ).generate(combined_text)

            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout(pad=0)
            return fig
        except Exception:
            pass

    # Fallback to Matplotlib top-words horizontal bar chart
    from .data_processing import get_trending_words
    temp_df = pd.DataFrame({'Post_Text': [combined_text]})
    words_df = get_trending_words(temp_df, top_n=10)

    if not words_df.empty:
        ax.barh(words_df['Word'][::-1], words_df['Frequency'][::-1], color='#6C5CE7')
        ax.set_title("Top Words Frequency (WordCloud Fallback)", fontsize=14, fontweight='bold', color='#2D3436')
        ax.set_xlabel("Frequency", fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    else:
        ax.text(0.5, 0.5, "Insufficient text data to generate Word Cloud", ha='center', va='center', fontsize=12)
        ax.axis('off')

    plt.tight_layout()
    return fig

