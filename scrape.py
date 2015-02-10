#!/usr/bin/env python
"""Scrape texts of SOTU addresses and save them to a directory."""

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

import urllib2
import re
import sys
import os
import time

from lxml import html
from urlparse import urljoin

SOURCE_URL = "http://stateoftheunion.onetwothree.net/texts/index.html"
LINK_RE = re.compile(r"(.+?)\s*,.+?,\s*(\d{4})")


def scrape(url, out_dir):
    """Download state of the Union addresses from the given URL."""

    # Exit if the output directory does not exist
    if not os.path.isdir(out_dir):
        print >> sys.stderr, \
            "Output directory {!r} does not exist".format(out_dir)
        sys.exit(1)

    # Create a parser for the url
    response = urllib2.urlopen(url)
    parser = html.fromstring(response.read())
    # The list is in the second <ul>
    ul_tag = parser.findall('.//ul')[1]
    for item in ul_tag:
        # First tag is a link
        link = item.find('a')
        # Extract the text, minus extra spaces
        text = link.text_content().strip()
        # Link to individual speech
        link_url = urljoin(url, link.attrib['href'])
        # President info
        president, year = parse_link_text(text)

        # Get the speech and write it
        print "Downloading {} ({})...".format(president, year)
        write_speech(link_url, president, year, out_dir)
        # Sleep to avoid slamming the server
        time.sleep(0.1)


def parse_link_text(text):
    """Parse a link text into (president, year)."""
    match = LINK_RE.match(text)
    if not match:
        print "Could not parse: {!r}".format(text)
        raise ValueError
    else:
        return match.groups()


def write_speech(url, president, year, out_dir):
    """Write the speech from the specified url out to out_dir/president-year.html"""
    response = urllib2.urlopen(url)
    parser = html.fromstring(response.read())

    out_path = os.path.join(out_dir, "-".join([year, president.replace(" ", "_")]) + ".txt")
    with open(out_path, "w") as out_file:
        # Find the first div with the id "content"
        content = parser.get_element_by_id("text")
        for item in content:
            # Skip everything but p
            if item.tag != "p":
                continue
            # Write out the paragraph content
            print >> out_file, item.text_content().strip()
            # Blank line between paragraphs
            print >> out_file


if __name__ == "__main__":
    try:
        OUT_DIR = sys.argv[1]
    except IndexError:
        print >> sys.stderr, "Usage: scrape output_dir"
        sys.exit(1)
    scrape(SOURCE_URL, OUT_DIR)
