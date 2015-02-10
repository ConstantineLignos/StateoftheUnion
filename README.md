# Scraping and analyzing the State of the Union

This repository provides teaching examples for how to scrape web
documents, extract words from them, and perform very simple analysis.

While the examples are very simple and can be accomplished using
existing software packages, this repository serves as a starting point
for researchers who want to understand how to perform simple text
processing.

The key scripts are:

* `scrape.py`: Download the texts for SOTU

* `count.py`: Process the texts into counts for individual words per
  speech

* `process_counts.py`: Process the counts into a CSV file

* `analyze_counts.R`: Analyze the counts

A few notes on state of the union (SOTU) addresses:

* The SOTU was first broadcast on evening TV in 1965

* From that point onward, all state of the union addresses were
  delivered orally on live television, with the exceptions of Jimmy
  Carter's 1981 address which was a written farewell address.

* Nixon's 1973 address was broken into a "series of messages"
  rather than a single address.
