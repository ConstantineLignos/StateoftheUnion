#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""Practice making a simple web scraper!

Takes a URL and a file path and write the abstract titles from the URL
(assumed to be the LSA 2015 schedule) and writes them out.
"""

import sys
import re
import codecs
from urllib2 import urlopen

from bs4 import BeautifulSoup

ABSTRACT_RE = re.compile("abstract")
BAD_CHARS = u"\"“”‘’`'"
BAD_CHARS_MAP = {ord(char): None for char in BAD_CHARS}


def get_titles(url):
    """Return all the abstract titles from the given URL."""
    req = urlopen(url)
    # Read encoding from page
    encoding = req.headers['content-type'].split('charset=')[-1]
    # Encode content properly
    content = unicode(req.read(), encoding)
    soup = BeautifulSoup(content, "lxml")
    # Clean each title
    titles = [clean_title(a.string) for a in soup.find_all(href=ABSTRACT_RE)]
    return (titles, encoding)


def clean_title(title):
    """Return a sanitized version of a title."""
    return title.translate(BAD_CHARS_MAP)


def main():
    """Get and print the titles."""
    try:
        url = sys.argv[1]
        out_path = sys.argv[2]
    except IndexError:
        print >> sys.stderr, "Usage: practice_scaper url output_path"
        sys.exit(1)

    # Read titles
    titles, encoding = get_titles(url)

    # Write them out
    with codecs.open(out_path, 'w', encoding) as out_file:
        for title in titles:
            print >> out_file, title


if __name__ == '__main__':
    main()
