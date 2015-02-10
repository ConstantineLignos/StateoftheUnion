#!/usr/bin/env python
"""Process counts generated by count.py."""

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

import sys
import os
import re
import csv
from collections import Counter

from nltk.stem import wordnet
from nltk.corpus.reader.wordnet import ADJ, VERB
from nltk.corpus import stopwords

FILENAME_RE = re.compile(r"(\d{4})-([\w.]+)\.txt")
STOPWORDS = set(stopwords.words('english'))
GOLDEN_WORDS = set(["us"])


def process_counts(count_dir, out_csv):
    """Process counts generated by count.py."""
    # Set up stemmer
    lemmatizer = wordnet.WordNetLemmatizer()

    # Read in all counts. Data are organized by:
    # year_presidents: dict mapping years to president names
    year_presidents = {}
    # year_counts: dict mapping years to counts
    year_counts = {}
    # year_totals: dict mapping years to total counts
    year_totals = {}
    # total_counter: Counter for overall word counts
    total_counter = Counter()
    # document_counts: Counter for number of documents each word appears in
    doc_counter = Counter()

    print "Reading counts..."
    for filename in os.listdir(count_dir):
        # Extract the name and year
        year, president = FILENAME_RE.match(filename).groups()
        year = int(year)
        president = president.replace("_", " ")
        year_presidents[year] = president

        # Init totals and counts
        year_counts[year] = counts = Counter()
        year_totals[year] = 0

        # Process the counts
        with open(os.path.join(count_dir, filename), "U") as count_file:
            for line in count_file:
                word, count = line.split()
                count = int(count)

                # Skip stopwords
                if word in STOPWORDS:
                    continue

                # Remove any "'s"
                word = word.replace("'s", "")

                # Stem the word
                lemma = lemmatizer.lemmatize(word)
                # If using the default POS didn't do anything, try verb and adjective
                if lemma == word:
                    lemma = lemmatizer.lemmatize(word, VERB)
                if lemma == word:
                    lemma = lemmatizer.lemmatize(word, ADJ)

                # It the word is golden, override any lemmatization.
                # TODO: This should be rewritten to skip lemmatization for these items.
                if word in GOLDEN_WORDS:
                    lemma = word

                # Add to the document counts if this is the first time seeing it in
                # the document
                if lemma not in counts:
                    doc_counter[lemma] += 1

                # Update counts
                counts[lemma] += count
                total_counter[lemma] += count
                year_totals[year] += count

    print "Writing counts..."
    # Write out counts for all files
    with open(out_csv, 'w') as count_file:
        # Set up a CSV writer
        count_csv = csv.writer(count_file)
        count_csv.writerow(["Year", "President", "Word", "Count"])
        # Loop over years and their counts and output them
        for year, counts in year_counts.iteritems():
            president = year_presidents[year]
            for word, count in counts.most_common():
                # Compute relative count as the count over the average count for
                # this item
                count_csv.writerow([year, president, word, count])


if __name__ == "__main__":
    try:
        COUNT_DIR = sys.argv[1]
        OUT_CSV = sys.argv[2]
    except IndexError:
        print >> sys.stderr, "Usage: process_counts count_dir output_csv"
        sys.exit()
    process_counts(COUNT_DIR, OUT_CSV)
