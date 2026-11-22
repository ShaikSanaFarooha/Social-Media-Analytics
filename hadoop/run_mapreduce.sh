#!/bin/bash
# =============================================================================
# Hadoop MapReduce Job Execution Script
# Project: Social Media Analytics Using Python & Big Data
# =============================================================================

echo "===================================================================="
echo " Starting Hadoop Distributed MapReduce Job: Social Media Analytics  "
echo "===================================================================="

# Step 1: Create HDFS directory structure
echo "[1/4] Creating HDFS input and output directories..."
hdfs dfs -mkdir -p /user/bigdata/social_media/input
hdfs dfs -mkdir -p /user/bigdata/social_media/output

# Step 2: Ingest local dataset to Hadoop Distributed File System (HDFS)
echo "[2/4] Uploading raw social media CSV to HDFS..."
hdfs dfs -put -f data/social_media_data.csv /user/bigdata/social_media/input/

# Remove existing output folder on HDFS if present
hdfs dfs -rm -r -f /user/bigdata/social_media/output/mapreduce_results

# Step 3: Run Hadoop Streaming MapReduce Job
echo "[3/4] Submitting MapReduce Streaming Job to YARN..."
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files hadoop/mapper.py,hadoop/reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /user/bigdata/social_media/input/social_media_data.csv \
    -output /user/bigdata/social_media/output/mapreduce_results

# Step 4: Display Output results from HDFS
echo "[4/4] Job Completed! Fetching top aggregated results from HDFS:"
hdfs dfs -cat /user/bigdata/social_media/output/mapreduce_results/part-00000 | head -n 25

echo "===================================================================="
