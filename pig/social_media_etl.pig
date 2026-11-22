/*
=============================================================================
Apache Pig Latin Script: Social Media ETL & Aggregation Pipeline
Project: Social Media Analytics Using Python & Big Data
Description:
    Performs Extract, Transform, Load (ETL) on social media records on HDFS.
    Calculates composite user engagement, groups metrics by platform,
    and isolates high-engagement viral content using Pig Latin data flow.
=============================================================================
*/

-- Step 1: Load raw social media dataset from HDFS with strict Pig schema
raw_posts = LOAD '/user/bigdata/social_media/input/social_media_data.csv' 
    USING PigStorage(',') 
    AS (
        post_id: chararray,
        username: chararray,
        platform: chararray,
        post_text: chararray,
        hashtags: chararray,
        likes: int,
        comments: int,
        shares: int,
        post_date: chararray
    );

-- Step 2: Filter out CSV header row and null records
clean_posts = FILTER raw_posts BY post_id != 'Post_ID' AND post_id IS NOT NULL;

-- Step 3: Transform records: calculate Total_Engagement (Likes + Comments + Shares)
transformed_posts = FOREACH clean_posts GENERATE 
    post_id,
    username,
    platform,
    post_text,
    hashtags,
    likes,
    comments,
    shares,
    (likes + comments + shares) AS total_engagement,
    post_date;

-- Step 4: Group data by social media Platform
posts_by_platform = GROUP transformed_posts BY platform;

-- Step 5: Compute summary aggregates per platform (Total posts, Avg Engagement, Max Likes)
platform_kpi = FOREACH posts_by_platform GENERATE 
    group AS platform_name,
    COUNT(transformed_posts) AS total_posts,
    SUM(transformed_posts.likes) AS total_likes,
    SUM(transformed_posts.comments) AS total_comments,
    SUM(transformed_posts.shares) AS total_shares,
    AVG(transformed_posts.total_engagement) AS avg_engagement,
    MAX(transformed_posts.likes) AS max_likes;

-- Step 6: Identify High-Engagement Viral Posts (Total Engagement > 3000)
viral_posts = FILTER transformed_posts BY total_engagement > 3000;
sorted_viral = ORDER viral_posts BY total_engagement DESC;
top_viral_posts = LIMIT sorted_viral 20;

-- Step 7: Store analytical results back into HDFS storage
STORE platform_kpi INTO '/user/bigdata/social_media/output/pig_platform_kpi' USING PigStorage('\t');
STORE top_viral_posts INTO '/user/bigdata/social_media/output/pig_viral_posts' USING PigStorage('\t');

-- Step 8: Interactive Display (DUMP to console for verification)
DUMP platform_kpi;
