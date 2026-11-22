#!/bin/bash
# =============================================================================
# Execution Script for Apache Pig Latin Script
# Supports: MapReduce mode (cluster) and Local mode (standalone)
# =============================================================================

echo "===================================================================="
echo " Submitting Apache Pig ETL Job: Social Media Analytics              "
echo "===================================================================="

# Check execution mode argument: default to local if not specified
MODE=${1:-local}

if [ "$MODE" == "mapreduce" ]; then
    echo "Executing in Hadoop MapReduce Cluster Mode..."
    pig -x mapreduce pig/social_media_etl.pig
else
    echo "Executing in Local Standalone Mode..."
    pig -x local -f pig/social_media_etl.pig
fi

echo "===================================================================="
echo " Pig ETL Pipeline Execution Completed Successfully!                 "
echo "===================================================================="
