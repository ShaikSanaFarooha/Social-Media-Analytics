"""
Modules package initialization for Social Media Analytics project.
Includes Big Data Analytics engines: Apache Spark, Hive, Pig, and Hadoop.
"""

from .data_processing import (
    load_data,
    clean_data,
    get_summary_metrics,
    get_top_active_users,
    extract_hashtags,
    get_trending_words
)

from .sentiment_analysis import (
    analyze_dataframe_sentiment,
    analyze_single_text,
    get_sentiment_summary
)

from .visualization import (
    plot_sentiment_pie,
    plot_sentiment_bar,
    plot_sentiment_by_platform,
    plot_likes_comments_shares,
    plot_top_hashtags,
    plot_top_words,
    plot_engagement_distribution,
    plot_engagement_over_time,
    plot_top_active_users,
    generate_wordcloud_figure
)

from .spark_processing import (
    execute_spark_sql,
    get_spark_rdd_wordcount,
    get_big_data_architecture_info
)
