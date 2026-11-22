#!/usr/bin/env python3
"""
=============================================================================
Hadoop Streaming MapReduce - Mapper
Project: Social Media Analytics Using Python & Big Data
Description:
    Reads social media records line-by-line from standard input (sys.stdin),
    tokenizes hashtags and keywords, and emits key-value pairs (key, 1)
    to standard output for Hadoop Shuffle & Sort.
=============================================================================
"""

import sys
import re
import csv

def main():
    # Read each line from standard input (HDFS data blocks)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # Skip CSV header line if present
        if line.startswith("Post_ID") or line.startswith("post_id"):
            continue

        try:
            # Parse CSV row
            reader = csv.reader([line])
            row = next(reader)
            
            # Expected schema: Post_ID, Username, Platform, Post_Text, Hashtags, Likes, Comments, Shares, Date
            if len(row) >= 4:
                post_text = row[3]
                platform = row[2] if len(row) > 2 else "Unknown"

                # 1. Emit platform count: platform\t1
                print(f"platform_{platform.lower().replace(' ', '_')}\t1")

                # 2. Extract and emit hashtags: hashtag_#tag\t1
                hashtags = re.findall(r'#\w+', post_text.lower())
                if len(row) >= 5 and row[4]:
                    raw_tags = re.split(r'[, ]+', row[4].lower())
                    for t in raw_tags:
                        if t.startswith('#') and len(t) > 1:
                            hashtags.append(t)
                        elif t and not t.startswith('#') and len(t) > 1:
                            hashtags.append(f"#{t}")

                for tag in set(hashtags):
                    print(f"hashtag_{tag}\t1")

                # 3. Emit clean words for vocabulary analysis
                words = re.findall(r'\b[a-zA-Z]{3,}\b', post_text.lower())
                stopwords = {'the', 'and', 'this', 'that', 'with', 'for', 'from', 'have', 'were', 'what', 'when'}
                for w in words:
                    if w not in stopwords:
                        print(f"word_{w}\t1")

        except Exception:
            # Skip corrupted rows gracefully
            continue

if __name__ == "__main__":
    main()
