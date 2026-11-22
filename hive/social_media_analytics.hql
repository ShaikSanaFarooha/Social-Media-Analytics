-- =============================================================================
-- Apache Hive Data Warehouse Schema & Analytical Queries (HiveQL)
-- Project: Social Media Analytics Using Python & Big Data
-- Description:
--     Creates the Big Data Warehouse schema, partitioned ORC storage tables,
--     and high-performance analytical HiveQL queries over HDFS data.
-- =============================================================================

-- Step 1: Create and Switch to Dedicated Data Warehouse Database
CREATE DATABASE IF NOT EXISTS social_media_dw
COMMENT 'Enterprise Social Media Big Data Analytics Data Warehouse';

USE social_media_dw;

-- Step 2: Create External Raw Table pointing to HDFS input directory
CREATE EXTERNAL TABLE IF NOT EXISTS raw_social_posts (
    post_id STRING,
    username STRING,
    platform STRING,
    post_text STRING,
    hashtags STRING,
    likes INT,
    comments INT,
    shares INT,
    post_date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\""
)
LOCATION '/user/bigdata/social_media/input'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Step 3: Create High-Performance Partitioned Managed Table (ORC Columnar Format)
CREATE TABLE IF NOT EXISTS partitioned_social_analytics (
    post_id STRING,
    username STRING,
    post_text STRING,
    hashtags STRING,
    likes INT,
    comments INT,
    shares INT,
    total_engagement INT,
    polarity_score DOUBLE,
    post_date TIMESTAMP
)
PARTITIONED BY (platform_name STRING, sentiment_category STRING)
STORED AS ORC
TBLPROPERTIES (
    "orc.compress"="SNAPPY",
    "transactional"="true"
);

-- =============================================================================
-- ANALYTICAL HIVEQL QUERIES (BI & EXECUTIVE REPORTING)
-- =============================================================================

-- Query 1: Executive KPI Summary Across the Entire Enterprise
SELECT 
    COUNT(*) AS total_posts,
    SUM(likes) AS total_likes,
    SUM(comments) AS total_comments,
    SUM(shares) AS total_shares,
    SUM(likes + comments + shares) AS grand_total_engagement,
    ROUND(AVG(likes + comments + shares), 2) AS avg_engagement_per_post
FROM raw_social_posts;

-- Query 2: Platform Comparison with Sentiment Cross-Tabulation
SELECT 
    platform,
    COUNT(*) AS post_count,
    ROUND(AVG(likes), 1) AS avg_likes,
    ROUND(AVG(comments), 1) AS avg_comments,
    ROUND(AVG(shares), 1) AS avg_shares,
    SUM(likes + comments + shares) AS total_platform_engagement
FROM raw_social_posts
GROUP BY platform
ORDER BY total_platform_engagement DESC;

-- Query 3: Top 10 Most Active Influencers / Power Users
SELECT 
    username,
    COUNT(post_id) AS total_posts,
    SUM(likes) AS total_likes_earned,
    SUM(comments) AS total_comments_earned,
    SUM(likes + comments + shares) AS total_engagement,
    ROUND(AVG(likes + comments + shares), 2) AS avg_engagement_per_post
FROM raw_social_posts
GROUP BY username
HAVING total_posts >= 2
ORDER BY total_engagement DESC
LIMIT 10;

-- Query 4: Identify Viral Content (Engagement > 2x Mean) Using Window Functions
WITH engagement_stats AS (
    SELECT 
        post_id,
        username,
        platform,
        post_text,
        (likes + comments + shares) AS engagement,
        AVG(likes + comments + shares) OVER() AS overall_mean_engagement
    FROM raw_social_posts
)
SELECT 
    post_id,
    username,
    platform,
    post_text,
    engagement,
    ROUND(engagement / overall_mean_engagement, 2) AS virality_multiplier
FROM engagement_stats
WHERE engagement > (2 * overall_mean_engagement)
ORDER BY virality_multiplier DESC
LIMIT 15;
