#!/usr/bin/env python3
"""
=============================================================================
Hadoop Streaming MapReduce - Reducer
Project: Social Media Analytics Using Python & Big Data
Description:
    Reads sorted (key, value) pairs from sys.stdin emitted by Mapper nodes
    and aggregated during Hadoop Shuffle & Sort phase. Sums the occurrences
    of each key and emits the final aggregated counts to HDFS.
=============================================================================
"""

import sys

def main():
    current_key = None
    current_count = 0

    # Read line-by-line from sorted standard input
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            key, count_str = line.split('\t', 1)
            count = int(count_str)
        except ValueError:
            # Skip improperly formatted lines
            continue

        # If key is identical to the current key, accumulate
        if current_key == key:
            current_count += count
        else:
            # When key changes, emit the accumulated sum for the previous key
            if current_key:
                print(f"{current_key}\t{current_count}")
            current_key = key
            current_count = count

    # Emit the final key-count pair
    if current_key:
        print(f"{current_key}\t{current_count}")

if __name__ == "__main__":
    main()
