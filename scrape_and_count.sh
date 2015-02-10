#!/bin/sh -e

# Create the directories as needed
mkdir -p texts
mkdir -p counts

python scrape.py texts
python count.py texts counts
python process_counts.py counts counts.csv
