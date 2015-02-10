#!/usr/bin/env python
"""Compute word frequency counts over a directory of documents."""

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

import sys
import os
import re
from collections import Counter

# Accept alphabetical tokens with an optional apostrophe in the middl
TOKEN_RE = re.compile(r"([a-z]+'?[a-z]+)")


def make_freq_counts():
    """Parse arguments and write frequency counts."""
    try:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    except IndexError:
        print >> sys.stderr, "Usage: count input_dir output_dir"
        sys.exit(1)

    try:
        filenames = os.listdir(input_dir)
    except IOError:
        print >> sys.stderr, \
            "Error: could not open input directory {}".format(input_dir)

    for filename in filenames:
        process_file(filename, input_dir, output_dir)


def process_file(filename, input_dir, output_dir):
    """Write word frequencies for input_dir/filename to output_dir/filename."""
    input_file = open(os.path.join(input_dir, filename), 'U')
    counts = Counter()
    # Count tokens
    for line in input_file:
        tokens = extract_tokens(line)
        for token in tokens:
            if token:
                counts[token] += 1

    # Write out counts
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w') as output_file:
        for token, count in counts.most_common():
            print >> output_file, "\t".join((token, str(count)))


def extract_tokens(line):
    """Extract tokens from a line in a file.
    None is put in place of any excluded tokens."""
    raw_tokens = line.strip().split()
    return [extract_token(token) for token in raw_tokens]


def extract_token(raw_token):
    """Return the good portion of a token or None if there is not any."""
    match = TOKEN_RE.search(raw_token.lower())
    return match.group(1) if match else None


if __name__ == "__main__":
    make_freq_counts()
