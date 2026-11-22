"""
=============================================================================
Project Title: Social Media Analytics Using Python & Big Data Ecosystem
Academic Domain: Big Data Analytics & Artificial Intelligence (B.Tech Mini-Project)
Author / Developer: Shaik Sana Farooha (B.Tech CSE - AI)
Frontend Engine: Streamlit
Big Data Stack: Apache Spark (PySpark), Apache Hive, Apache Pig, Hadoop (HDFS & MapReduce)
Data Analytics: Pandas, NumPy, VADER, TextBlob, Plotly, Matplotlib, WordCloud
=============================================================================
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

# Import custom analysis, visualization, and Big Data modules
from modules.data_processing import (
    load_data,
    clean_data,
    get_summary_metrics,
    get_top_active_users,
    extract_hashtags,
    get_trending_words
)

from modules.sentiment_analysis import (
    analyze_dataframe_sentiment,
    analyze_single_text,
    get_sentiment_summary
)

from modules.visualization import (
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

from modules.spark_processing import (
    execute_spark_sql,
    get_spark_rdd_wordcount,
    get_big_data_architecture_info
)

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Social Media Analytics | Big Data Mini Project",
    page_icon="🐘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Blue & Purple Professional Light Theme
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Top Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(74, 0, 224, 0.15);
    }
    .hero-title {
        font-size: 30px;
        font-weight: 700;
        margin: 0;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 15px;
        font-weight: 400;
        margin-top: 6px;
        color: #E0E7FF !important;
    }
    .badge-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-top: 10px;
        margin-right: 8px;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 12px;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(110, 45, 226, 0.1);
        border-color: #8E2DE2;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #1E293B;
    }
    .metric-sub {
        font-size: 12px;
        color: #10B981;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Card Containers */
    .content-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }

    /* Section Subheadings */
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #6C5CE7;
        padding-left: 10px;
    }

    .bigdata-badge {
        background: #EDE9FE;
        color: #6D28D9;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        margin-right: 5px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION & DATA CACHING
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_and_preprocess_dataset(file_or_path):
    """Loads, cleans, and runs sentiment analysis on the dataset (cached for speed)."""
    raw_df = load_data(file_or_path)
    clean_df, stats = clean_data(raw_df)
    analyzed_df = analyze_dataframe_sentiment(clean_df)
    return analyzed_df, stats


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & DATASET SELECTION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 38px; margin-bottom: 5px;">🐘</div>
            <h2 style="margin: 0; font-size: 20px; color: #4A00E0; font-weight: 700;">Big Data Analytics</h2>
            <p style="margin: 0; font-size: 12px; color: #64748B;">Spark • Hive • Pig • Hadoop • B.Tech AI</p>
        </div>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;">
    """, unsafe_allow_html=True)

    st.subheader("⚙️ Big Data Engine")
    execution_engine = st.radio(
        "Select Processing Engine:",
        ["⚡ Apache Spark (PySpark Distributed)", "🚀 Pandas High-Performance"],
        index=0,
        help="Switch between Apache Spark distributed execution engine and Pandas in-memory engine."
    )

    st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    st.subheader("📁 Dataset Source")
    data_source_mode = st.radio(
        "Select Data Input:",
        ["Default Sample Dataset (235 Posts)", "Upload Custom CSV File"],
        index=0
    )

    uploaded_file = None
    default_csv_path = os.path.join("data", "social_media_data.csv")

    if data_source_mode == "Upload Custom CSV File":
        uploaded_file = st.file_uploader(
            "Upload your social media CSV file",
            type=["csv"],
            help="Upload CSV with Post_Text, Likes, Comments, Shares, Platform, Hashtags, Username columns."
        )
        if uploaded_file is None:
            st.info("👆 Please upload a CSV file or switch to the Default Sample Dataset.")
    else:
        st.success("✅ Dataset loaded (`data/social_media_data.csv`)")

    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # Main Navigation Menu
    st.subheader("🧭 Dashboard Menu")
    nav_selection = st.radio(
        "Navigate to Page:",
        [
            "📊 Overview & Summary",
            "🐘 Big Data Tools (Spark, Hive, Pig, Hadoop)",
            "🔍 Data Exploration & Cleaning",
            "💬 Sentiment Analysis",
            "#️⃣ Hashtags & Trending Topics",
            "📈 User Engagement Analytics",
            "🧪 Live Sentiment Tester",
            "📥 Dataset Preview & Download"
        ],
        index=0
    )


# -----------------------------------------------------------------------------
# 4. DATA LOADING PIPELINE
# -----------------------------------------------------------------------------
analyzed_df = None
cleaning_stats = None

try:
    if data_source_mode == "Upload Custom CSV File" and uploaded_file is not None:
        analyzed_df, cleaning_stats = load_and_preprocess_dataset(uploaded_file)
    else:
        if os.path.exists(default_csv_path):
            analyzed_df, cleaning_stats = load_and_preprocess_dataset(default_csv_path)
        else:
            st.error(f"Default dataset not found at `{default_csv_path}`. Please run `generate_dataset.py` first.")
            st.stop()
except Exception as e:
    st.error(f"❌ Error during dataset loading and processing: {str(e)}")
    st.stop()

if analyzed_df is None or analyzed_df.empty:
    st.warning("⚠️ No data available to analyze. Please provide a valid CSV dataset.")
    st.stop()


# -----------------------------------------------------------------------------
# 5. SIDEBAR GLOBAL FILTERS (Interactive Slice & Dice)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.subheader("⚡ Quick Filters")

    # Platform Filter
    available_platforms = ["All Platforms"] + sorted(list(analyzed_df['Platform'].unique()))
    selected_platform = st.selectbox("Filter by Platform:", available_platforms, index=0)

    # Sentiment Filter
    available_sentiments = ["All Sentiments", "Positive", "Neutral", "Negative"]
    selected_sentiment = st.selectbox("Filter by Sentiment:", available_sentiments, index=0)

    # Engagement Level Filter
    if 'Engagement_Level' in analyzed_df.columns:
        available_engagement = ["All Engagement Levels"] + list(analyzed_df['Engagement_Level'].unique())
        selected_engagement = st.selectbox("Engagement Level:", available_engagement, index=0)
    else:
        selected_engagement = "All Engagement Levels"

# Apply Sidebar Filters to Create Filtered DataFrame
filtered_df = analyzed_df.copy()

if selected_platform != "All Platforms":
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

if selected_sentiment != "All Sentiments":
    filtered_df = filtered_df[filtered_df['Sentiment'] == selected_sentiment]

if selected_engagement != "All Engagement Levels":
    filtered_df = filtered_df[filtered_df['Engagement_Level'] == selected_engagement]

# Filter Summary in Sidebar
with st.sidebar:
    st.caption(f"Showing **{len(filtered_df)}** of **{len(analyzed_df)}** posts.")
    st.caption(f"Engine: **{execution_engine.split(' ')[1]}**")


# -----------------------------------------------------------------------------
# 6. HEADER HERO BANNER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">Social Media Analytics Using Big Data & Python</h1>
        <p class="hero-subtitle">
            An End-to-End Big Data Architecture utilizing <b>Apache Spark, Apache Hive, Apache Pig, and Hadoop</b>
            for Distributed Social Media Sentiment Extraction and Engagement Intelligence.
        </p>
        <div>
            <span class="badge-tag">🎓 B.Tech Mini-Project</span>
            <span class="badge-tag">⚡ Apache Spark (PySpark)</span>
            <span class="badge-tag">🐝 Apache Hive (HiveQL)</span>
            <span class="badge-tag">🐷 Apache Pig (Pig Latin)</span>
            <span class="badge-tag">🐘 Hadoop (HDFS & MapReduce)</span>
            <span class="badge-tag">🤖 NLP Sentiment Analysis</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# PAGE 1: OVERVIEW & SUMMARY METRICS
# -----------------------------------------------------------------------------
if nav_selection == "📊 Overview & Summary":
    st.markdown("<div class='section-header'>Executive KPI Summary</div>", unsafe_allow_html=True)

    metrics = get_summary_metrics(filtered_df)
    sentiment_stats = get_sentiment_summary(filtered_df)

    # KPI Top Row (6 Key Metrics)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Posts</div>
                <div class="metric-value">{metrics['total_posts']:,}</div>
                <div class="metric-sub">Analyzed sample</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Likes</div>
                <div class="metric-value">{metrics['total_likes']:,}</div>
                <div class="metric-sub">Avg {metrics['avg_likes']:,.0f} / post</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Comments</div>
                <div class="metric-value">{metrics['total_comments']:,}</div>
                <div class="metric-sub">Avg {metrics['avg_comments']:,.0f} / post</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Shares</div>
                <div class="metric-value">{metrics['total_shares']:,}</div>
                <div class="metric-sub">Avg {metrics['avg_shares']:,.0f} / post</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Engagement</div>
                <div class="metric-value">{metrics['total_engagement']:,}</div>
                <div class="metric-sub">Avg {metrics['avg_engagement']:,.0f} / post</div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        nss = sentiment_stats['net_sentiment_score']
        nss_color = "#10B981" if nss >= 0 else "#EF4444"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Net Sentiment</div>
                <div class="metric-value" style="color: {nss_color};">{nss:+.1f}%</div>
                <div class="metric-sub">{sentiment_stats['dominant_sentiment']} Dominant</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Visual High-Level Charts
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        st.plotly_chart(plot_sentiment_pie(filtered_df), use_container_width=True)

    with chart_col2:
        st.plotly_chart(plot_sentiment_by_platform(filtered_df), use_container_width=True)

    # Row 3: Engagement Over Time & Platform Boxplot
    chart_col3, chart_col4 = st.columns([1, 1])

    with chart_col3:
        st.plotly_chart(plot_engagement_over_time(filtered_df), use_container_width=True)

    with chart_col4:
        st.plotly_chart(plot_engagement_distribution(filtered_df), use_container_width=True)

    # Recent Posts Quick Inspection Table
    st.markdown("<div class='section-header'>Recent Social Media Activity</div>", unsafe_allow_html=True)
    display_cols = ['Post_ID', 'Username', 'Platform', 'Post_Text', 'Likes', 'Comments', 'Shares', 'Sentiment']
    available_display = [c for c in display_cols if c in filtered_df.columns]
    st.dataframe(filtered_df[available_display].head(10), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 2: BIG DATA ECOSYSTEM (SPARK, HIVE, PIG, HADOOP)
# -----------------------------------------------------------------------------
elif nav_selection == "🐘 Big Data Tools (Spark, Hive, Pig, Hadoop)":
    st.markdown("<div class='section-header'>Big Data Analytics Stack: Spark, Hive, Pig & Hadoop</div>", unsafe_allow_html=True)
    st.write(
        "This section illustrates how raw social media streams flow through the enterprise Big Data ecosystem: "
        "**HDFS storage**, **MapReduce/Pig ETL**, **Hive Data Warehousing**, and **Apache Spark In-Memory Analytics**."
    )

    # Four Main Big Data Tabs
    bd_tab1, bd_tab2, bd_tab3, bd_tab4 = st.tabs([
        "⚡ Apache Spark (PySpark)",
        "🐝 Apache Hive (HiveQL DW)",
        "🐷 Apache Pig (Pig Latin ETL)",
        "🐘 Hadoop (HDFS & MapReduce)"
    ])

    # TAB 1: APACHE SPARK (PYSPARK)
    with bd_tab1:
        st.markdown("### ⚡ Apache Spark Distributed Processing")
        st.markdown(
            "Apache Spark processes Big Data in-memory using Resilient Distributed Datasets (RDDs) "
            "and Spark SQL with the Catalyst Query Optimizer."
        )

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Spark In-Memory Acceleration", "100x vs MapReduce")
        with col_s2:
            st.metric("Catalyst Partitioning", "4 Active Partitions")
        with col_s3:
            st.metric("Execution Engine", "PySpark 3.x Engine")

        st.markdown("#### 1. Interactive Spark SQL Query Console")
        
        sample_queries = {
            "Platform Summary (Count & Avg Likes)": 
                "SELECT Platform, COUNT(*) AS Post_Count, ROUND(AVG(Likes), 1) AS Avg_Likes, SUM(Total_Engagement) AS Total_Engagement FROM social_media_posts GROUP BY Platform ORDER BY Total_Engagement DESC",
            "Top 5 Influencers by Engagement":
                "SELECT Username, COUNT(*) AS Total_Posts, SUM(Likes) AS Total_Likes, SUM(Total_Engagement) AS Total_Engagement FROM social_media_posts GROUP BY Username ORDER BY Total_Engagement DESC LIMIT 5",
            "Sentiment Breakdown Across Platforms":
                "SELECT Platform, Sentiment, COUNT(*) AS Posts_Count FROM social_media_posts GROUP BY Platform, Sentiment ORDER BY Platform, Posts_Count DESC",
            "High Virality Posts (Engagement > 3500)":
                "SELECT Post_ID, Username, Platform, Likes, Comments, Shares, Total_Engagement FROM social_media_posts WHERE Total_Engagement > 3500 ORDER BY Total_Engagement DESC"
        }

        selected_query_title = st.selectbox("Select a Pre-Built Spark SQL Query:", list(sample_queries.keys()))
        custom_spark_query = st.text_area(
            "Spark SQL Query Editor (Live Execution):",
            value=sample_queries[selected_query_title],
            height=90
        )

        if st.button("🚀 Execute Spark SQL Query", type="primary"):
            with st.spinner("Executing Spark SQL on distributed DataFrame..."):
                spark_res_df, engine_name, catalyst_plan = execute_spark_sql(filtered_df, custom_spark_query)
                st.success(f"Executed successfully via **{engine_name}**")
                st.dataframe(spark_res_df, use_container_width=True)

                with st.expander("🔍 View Spark Catalyst Optimizer Query Execution Plan"):
                    st.code(catalyst_plan, language="text")

        st.markdown("#### 2. Spark RDD Transformation Pipeline (Map & ReduceByKey)")
        st.write("Canonical Big Data transformation line: `sc.parallelize() -> flatMap() -> map(w, 1) -> reduceByKey(add)`")
        
        rdd_df, rdd_lineage = get_spark_rdd_wordcount(filtered_df, top_n=10)
        col_rdd1, col_rdd2 = st.columns([1, 1])
        with col_rdd1:
            st.dataframe(rdd_df, use_container_width=True)
        with col_rdd2:
            st.code(rdd_lineage, language="text")

    # TAB 2: APACHE HIVE
    with bd_tab2:
        st.markdown("### 🐝 Apache Hive Distributed Data Warehouse (HiveQL)")
        st.write(
            "Apache Hive facilitates querying and managing large datasets residing in distributed storage (HDFS) "
            "using SQL-like language (**HiveQL**). Features schema-on-read, ORC columnar storage, and partitioning."
        )

        st.markdown("#### 1. Hive Data Warehouse Architecture")
        hive_code = """-- Step 1: Create Big Data Warehouse Database
CREATE DATABASE IF NOT EXISTS social_media_dw;
USE social_media_dw;

-- Step 2: Create External Raw Table pointing to HDFS
CREATE EXTERNAL TABLE IF NOT EXISTS raw_social_posts (
    post_id STRING, username STRING, platform STRING,
    post_text STRING, hashtags STRING,
    likes INT, comments INT, shares INT, post_date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION '/user/bigdata/social_media/input';

-- Step 3: Create High-Performance Partitioned Table (ORC Format)
CREATE TABLE IF NOT EXISTS partitioned_social_analytics (
    post_id STRING, username STRING, post_text STRING,
    likes INT, comments INT, shares INT, total_engagement INT
)
PARTITIONED BY (platform_name STRING, sentiment_category STRING)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");"""

        st.code(hive_code, language="sql")

        st.markdown("#### 2. HiveQL Analytical Query Execution")
        st.write("**Top 5 Power Users via HiveQL Aggregation:**")
        hive_res_df, _, _ = execute_spark_sql(
            filtered_df,
            "SELECT Username, COUNT(*) AS Total_Posts, SUM(Likes) AS Total_Likes, SUM(Total_Engagement) AS Total_Engagement FROM social_media_posts GROUP BY Username ORDER BY Total_Engagement DESC LIMIT 5"
        )
        st.dataframe(hive_res_df, use_container_width=True)

        if os.path.exists("hive/social_media_analytics.hql"):
            with open("hive/social_media_analytics.hql", "r", encoding="utf-8") as hf:
                st.download_button(
                    label="📥 Download Full HiveQL Script (social_media_analytics.hql)",
                    data=hf.read(),
                    file_name="social_media_analytics.hql",
                    mime="text/plain"
                )

    # TAB 3: APACHE PIG
    with bd_tab3:
        st.markdown("### 🐷 Apache Pig (Pig Latin) ETL Pipeline")
        st.write(
            "Apache Pig is a high-level dataflow platform for executing MapReduce jobs. "
            "It expresses complex data pipelines using **Pig Latin** dataflow language."
        )

        st.markdown("#### Pig Latin Dataflow Script (`social_media_etl.pig`)")
        pig_script = """/* Load Raw CSV from HDFS */
raw_posts = LOAD '/user/bigdata/social_media/input/social_media_data.csv' 
    USING PigStorage(',') 
    AS (post_id:chararray, username:chararray, platform:chararray, 
        post_text:chararray, hashtags:chararray, likes:int, comments:int, shares:int, post_date:chararray);

/* Filter Header and Corrupted Records */
clean_posts = FILTER raw_posts BY post_id != 'Post_ID' AND post_id IS NOT NULL;

/* Transform & Feature Engineering */
transformed = FOREACH clean_posts GENERATE 
    post_id, username, platform, post_text,
    (likes + comments + shares) AS total_engagement;

/* Group By Platform & Compute Platform KPIs */
by_platform = GROUP transformed BY platform;
platform_stats = FOREACH by_platform GENERATE 
    group AS platform,
    COUNT(transformed) AS post_count,
    AVG(transformed.total_engagement) AS avg_engagement;

/* Store results into HDFS */
STORE platform_stats INTO '/user/bigdata/social_media/output/pig_kpi' USING PigStorage('\\t');"""
        
        st.code(pig_script, language="pig")

        st.markdown("#### Pig Latin Data Model Hierarchy")
        st.markdown("""
        * **Atom:** Simple atomic data value (e.g. `'alex_dev'`, `3500`).
        * **Tuple:** Ordered set of fields equivalent to a table row (e.g. `('P001', 'alex_dev', 'Instagram')`).
        * **Bag:** Collection of tuples, equivalent to an entire relation/table.
        * **Map:** Key-value pairs used for nested attributes.
        """)

    # TAB 4: HADOOP HDFS & MAPREDUCE
    with bd_tab4:
        st.markdown("### 🐘 Hadoop Ecosystem (HDFS & MapReduce)")
        st.write(
            "Hadoop provides distributed, fault-tolerant storage across commodity hardware via **HDFS** "
            "and batch computational processing via **YARN MapReduce**."
        )

        h_col1, h_col2 = st.columns(2)
        with h_col1:
            st.markdown("#### 1. Hadoop Streaming Mapper (`mapper.py`)")
            st.code("""import sys, csv, re

for line in sys.stdin:
    if line.startswith("Post_ID"): continue
    row = next(csv.reader([line]))
    if len(row) >= 4:
        # Emit hashtags
        for tag in re.findall(r'#\\w+', row[3].lower()):
            print(f"hashtag_{tag}\\t1")
        # Emit platform count
        print(f"platform_{row[2].lower()}\\t1")""", language="python")

        with h_col2:
            st.markdown("#### 2. Hadoop Streaming Reducer (`reducer.py`)")
            st.code("""import sys

curr_key, curr_count = None, 0
for line in sys.stdin:
    key, count = line.strip().split('\\t', 1)
    if curr_key == key:
        curr_count += int(count)
    else:
        if curr_key: print(f"{curr_key}\\t{curr_count}")
        curr_key, curr_count = key, int(count)
if curr_key: print(f"{curr_key}\\t{curr_count}")""", language="python")

        st.markdown("#### 3. Live MapReduce Simulation Over Current Dataset")
        if st.button("⚙️ Run Hadoop MapReduce Simulation", type="secondary"):
            all_tags = []
            for text in filtered_df['Post_Text']:
                all_tags.extend(re.findall(r'#\w+', text.lower()))
            tag_counts = pd.Series(all_tags).value_counts().head(8).reset_index()
            tag_counts.columns = ['Key (Emitted Token)', 'Value (Reducer Sum)']
            st.success("✅ MapReduce Distributed Job Emulation Completed!")
            st.dataframe(tag_counts, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 3: DATA EXPLORATION & CLEANING
# -----------------------------------------------------------------------------
elif nav_selection == "🔍 Data Exploration & Cleaning":
    st.markdown("<div class='section-header'>Data Quality, Cleaning & Statistical Overview</div>", unsafe_allow_html=True)

    # Cleaning Statistics Card
    if cleaning_stats:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Initial Raw Rows", f"{cleaning_stats['initial_rows']:,}")
        with c2:
            st.metric("Clean Records Retained", f"{cleaning_stats['final_rows']:,}")
        with c3:
            st.metric("Duplicates Removed", f"{cleaning_stats['duplicates_removed']:,}")
        with c4:
            st.metric("Missing Values Handled", f"{cleaning_stats['missing_values_handled']:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Dataset Schema and Summary Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Data Schema & Null Check", "📊 Descriptive Statistics", "🧩 Clean Dataset Sample"])

    with tab1:
        col_info = []
        for col in analyzed_df.columns:
            col_info.append({
                "Column Name": col,
                "Data Type": str(analyzed_df[col].dtype),
                "Non-Null Count": int(analyzed_df[col].notnull().sum()),
                "Null Values": int(analyzed_df[col].isnull().sum()),
                "Unique Values": int(analyzed_df[col].nunique())
            })
        st.dataframe(pd.DataFrame(col_info), use_container_width=True)

    with tab2:
        st.write("**Numerical Features Summary (Pandas .describe()):**")
        numeric_cols = ['Likes', 'Comments', 'Shares', 'Total_Engagement', 'Polarity_Score']
        existing_num = [c for c in numeric_cols if c in analyzed_df.columns]
        st.dataframe(analyzed_df[existing_num].describe().round(2), use_container_width=True)

    with tab3:
        st.dataframe(filtered_df.head(25), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 4: SENTIMENT ANALYSIS
# -----------------------------------------------------------------------------
elif nav_selection == "💬 Sentiment Analysis":
    st.markdown("<div class='section-header'>Sentiment Analysis & Opinion Mining</div>", unsafe_allow_html=True)

    sent_stats = get_sentiment_summary(filtered_df)

    # Sentiment KPI Cards
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)

    with s_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label" style="color: #00B894;">Positive Posts</div>
                <div class="metric-value" style="color: #00B894;">{sent_stats['positive_count']:,}</div>
                <div class="metric-sub">{sent_stats['positive_pct']}% of posts</div>
            </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label" style="color: #0984E3;">Neutral Posts</div>
                <div class="metric-value" style="color: #0984E3;">{sent_stats['neutral_count']:,}</div>
                <div class="metric-sub">{sent_stats['neutral_pct']}% of posts</div>
            </div>
        """, unsafe_allow_html=True)

    with s_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label" style="color: #D63031;">Negative Posts</div>
                <div class="metric-value" style="color: #D63031;">{sent_stats['negative_count']:,}</div>
                <div class="metric-sub">{sent_stats['negative_pct']}% of posts</div>
            </div>
        """, unsafe_allow_html=True)

    with s_col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Dominant Tone</div>
                <div class="metric-value" style="font-size: 22px;">{sent_stats['dominant_sentiment']}</div>
                <div class="metric-sub">NSS: {sent_stats['net_sentiment_score']:+.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sentiment Visualizations
    v_col1, v_col2 = st.columns([1, 1])

    with v_col1:
        st.plotly_chart(plot_sentiment_pie(filtered_df), use_container_width=True)

    with v_col2:
        st.plotly_chart(plot_sentiment_bar(filtered_df), use_container_width=True)

    st.plotly_chart(plot_sentiment_by_platform(filtered_df), use_container_width=True)

    # Sentiment Sample Posts Inspector
    st.markdown("<div class='section-header'>Inspect Sample Posts by Sentiment Category</div>", unsafe_allow_html=True)
    inspect_sentiment = st.radio("Choose Sentiment to View Examples:", ["Positive", "Negative", "Neutral"], horizontal=True)

    sample_subset = filtered_df[filtered_df['Sentiment'] == inspect_sentiment].head(6)

    if not sample_subset.empty:
        s_row_1, s_row_2 = st.columns(2)
        for idx, (_, row) in enumerate(sample_subset.iterrows()):
            target_col = s_row_1 if idx % 2 == 0 else s_row_2
            with target_col:
                score = row.get('Polarity_Score', 0.0)
                badge_color = "#00B894" if inspect_sentiment == "Positive" else ("#D63031" if inspect_sentiment == "Negative" else "#0984E3")
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid {badge_color}; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-size: 13px; color: #64748B; margin-bottom: 6px;">
                            <span><b>@{row['Username']}</b> on {row['Platform']}</span>
                            <span style="font-weight: 600; color: {badge_color};">Polarity: {score:+.2f}</span>
                        </div>
                        <div style="font-size: 14px; color: #1E293B; line-height: 1.5;">"{row['Post_Text']}"</div>
                        <div style="font-size: 12px; color: #94A3B8; margin-top: 8px;">
                            ❤️ {row['Likes']} likes &nbsp;•&nbsp; 💬 {row['Comments']} comments &nbsp;•&nbsp; 🔁 {row['Shares']} shares
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info(f"No posts found matching '{inspect_sentiment}' sentiment under the current filters.")


# -----------------------------------------------------------------------------
# PAGE 5: HASHTAGS & TRENDING TOPICS
# -----------------------------------------------------------------------------
elif nav_selection == "#️⃣ Hashtags & Trending Topics":
    st.markdown("<div class='section-header'>Hashtag Intelligence & Trending Topic Discovery</div>", unsafe_allow_html=True)

    hashtag_df = extract_hashtags(filtered_df)
    trending_words_df = get_trending_words(filtered_df, top_n=15)

    h_col1, h_col2 = st.columns([1, 1])

    with h_col1:
        st.plotly_chart(plot_top_hashtags(hashtag_df, top_n=10), use_container_width=True)

    with h_col2:
        st.plotly_chart(plot_top_words(trending_words_df, top_n=12), use_container_width=True)

    # Word Cloud Section
    st.markdown("<div class='section-header'>Audience Word Cloud Visualization</div>", unsafe_allow_html=True)
    wc_fig = generate_wordcloud_figure(filtered_df)
    st.pyplot(wc_fig)

    # Hashtag Breakdown Table
    with st.expander("🔍 View All Extracted Hashtags & Frequencies"):
        if not hashtag_df.empty:
            st.dataframe(hashtag_df, use_container_width=True)
        else:
            st.info("No hashtags found in the current dataset.")


# -----------------------------------------------------------------------------
# PAGE 6: USER ENGAGEMENT ANALYTICS
# -----------------------------------------------------------------------------
elif nav_selection == "📈 User Engagement Analytics":
    st.markdown("<div class='section-header'>Engagement Metrics & User Behavior Intelligence</div>", unsafe_allow_html=True)

    # Multi-dimensional Engagement Scatter
    st.plotly_chart(plot_likes_comments_shares(filtered_df), use_container_width=True)

    u_col1, u_col2 = st.columns([1, 1])

    with u_col1:
        top_users_df = get_top_active_users(filtered_df, top_n=10)
        st.plotly_chart(plot_top_active_users(top_users_df, top_n=10), use_container_width=True)

    with u_col2:
        st.plotly_chart(plot_engagement_distribution(filtered_df), use_container_width=True)

    # Top Active Influencers Leaderboard Table
    st.markdown("<div class='section-header'>Top Influencers & Active Accounts</div>", unsafe_allow_html=True)
    if not top_users_df.empty:
        st.dataframe(top_users_df, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 7: LIVE SENTIMENT TESTER (Interactive Demo Feature)
# -----------------------------------------------------------------------------
elif nav_selection == "🧪 Live Sentiment Tester":
    st.markdown("<div class='section-header'>Live Interactive Sentiment Predictor</div>", unsafe_allow_html=True)
    st.write(
        "Type or paste any custom social media text below to test real-time NLP sentiment analysis. "
        "Ideal for live viva / college presentation demonstration!"
    )

    sample_input = st.text_area(
        "Enter Social Media Text / Tweet:",
        value="Apache Spark and Hive transformed our Big Data mini project! Distributed computing with PySpark is amazing.",
        height=100
    )

    if st.button("🚀 Analyze Sentiment Now", type="primary"):
        if sample_input.strip():
            result = analyze_single_text(sample_input)

            sentiment = result['sentiment']
            polarity = result['polarity']
            method = result['method']

            if sentiment == "Positive":
                badge_bg = "#00B894"
                icon = "😄"
            elif sentiment == "Negative":
                badge_bg = "#D63031"
                icon = "😡"
            else:
                badge_bg = "#0984E3"
                icon = "😐"

            st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid {badge_bg}; border-radius: 12px; padding: 20px; margin-top: 15px;">
                    <div style="font-size: 28px; font-weight: 700; color: {badge_bg}; margin-bottom: 8px;">
                        {icon} Classified Sentiment: {sentiment}
                    </div>
                    <div style="font-size: 14px; color: #64748B;">
                        NLP Engine Used: <b>{method}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Polarity Score (-1 to +1)", f"{polarity:+.3f}")
            with c2:
                st.metric("Positive Confidence", f"{result.get('pos_score', 0):.2f}")
            with c3:
                st.metric("Neutral Confidence", f"{result.get('neu_score', 0):.2f}")
            with c4:
                st.metric("Negative Confidence", f"{result.get('neg_score', 0):.2f}")

        else:
            st.warning("Please enter some text before analyzing.")


# -----------------------------------------------------------------------------
# PAGE 8: DATASET PREVIEW & DOWNLOAD
# -----------------------------------------------------------------------------
elif nav_selection == "📥 Dataset Preview & Download":
    st.markdown("<div class='section-header'>Enriched Dataset Preview & Export</div>", unsafe_allow_html=True)
    st.write(
        "Here you can inspect the full cleaned dataset with computed sentiment scores, "
        "engagement totals, and export it as a CSV file for further reporting."
    )

    # Search filter within table
    search_query = st.text_input("🔍 Search within post text or username:", "")
    view_df = filtered_df.copy()
    if search_query:
        view_df = view_df[
            view_df['Post_Text'].str.contains(search_query, case=False, na=False) |
            view_df['Username'].str.contains(search_query, case=False, na=False)
        ]

    st.write(f"Displaying **{len(view_df)}** records:")
    st.dataframe(view_df, use_container_width=True)

    # CSV Download Button
    csv_bytes = view_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Analyzed Dataset as CSV",
        data=csv_bytes,
        file_name="social_media_analytics_results.csv",
        mime="text/csv",
        type="primary"
    )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style="margin-top: 40px; border: none; border-top: 1px solid #E2E8F0;">
    <div style="text-align: center; color: #94A3B8; font-size: 13px; padding-bottom: 20px;">
        Social Media Analytics Using Big Data (Spark • Hive • Pig • Hadoop) & Python | B.Tech CSE (AI) Mini-Project
    </div>
""", unsafe_allow_html=True)
