# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

library(dplyr)
library(ggplot2)
library(wordcloud)
theme_set(theme_bw())

# Load the counts
raw.counts <- tbl_df(read.csv("counts.csv"))

# Compute total counts and note the 1981 weirdness
year.counts <- raw.counts %>% group_by(Year) %>% summarise(Count = sum(Count))
# Overall SOTU
ggplot(year.counts, aes(Year, Count)) + geom_line()
# Evening televised SOTU
ggplot(subset(year.counts, Year >= 1965), aes(Year, Count)) + geom_line()
# 1981 was a written record of accomplishments of the Carter presidency
ggplot(subset(year.counts, Year >= 1965 & Year != 1981), aes(Year, Count)) + geom_line()
# 1973 was an outlier because it was not a single speech, 1973 because it was a
# set of mini-speeches
ggplot(subset(year.counts, Year >= 1965 & !Year %in% c(1973, 1981)), aes(Year, Count)) + geom_line()
# Note that 2001 is still an outlier. This is because it was a "budget message".
# Most post-inaguration SOTUs are not actual SOTUs; it might be worth excluding
# them. See more comments here: http://www.presidency.ucsb.edu/sou.php

# Implement the exclusions
counts <- subset(raw.counts, Year >= 1965 & !Year %in% c(1973, 1981))

# Basic plot to test sanity
plot.words <- function(words, counts, smooth = TRUE) {
  if (smooth) {
    ggplot(subset(counts, Word %in% words), aes(Year, Count, color = Word)) + geom_smooth(method = "loess", se = FALSE, span = 0.6)
  }
  else {
    ggplot(subset(counts, Word %in% words), aes(Year, Count, color = Word)) + geom_line()
  }
}
plot.words(c("congress", "america"), counts)
plot.words(c("terror", "war"), counts)
# Consider a log scale here
plot.words(c("iraq", "afghanistan", "russia"), counts)
plot.words(c("iraq", "afghanistan", "russia"), counts) + scale_y_log10()

# Add total counts per item. This is a little awkward; I'm very open to better
# ways to do this.
# Total counts for each lemma
total.counts <- counts %>% group_by(Word) %>% summarise(Total.count = sum(Count), Mean.count = mean(Count))
# Summarize by president
pres.total.counts <- counts %>% group_by(President, Word) %>% summarise(Pres.count = sum(Count))
# Compute averages over the President counts
pres.mean.counts <- pres.total.counts %>% group_by(Word) %>% summarise(Mean.pres.count = mean(Pres.count))

# Word cloud for all SOTU
wordcloud(total.counts$Word, total.counts$Mean.count, min.freq = 12)

# Some relative counts
# Each word and its total count
rel.counts <- left_join(counts, total.counts, by = "Word")
rel.counts$Count <- with(rel.counts, Count / Mean.count)
# Plot examples
rel.plot.words <- function(words, counts) {
  plot.words(words, counts) + geom_hline(aes(yintercept = 1), linetype = "dashed") + xlab("Relative count")
}
rel.plot.words(c("foreign", "domestic"), rel.counts)
rel.plot.words(c("war", "peace"), rel.counts)
rel.plot.words(c("budget", "deficit"), rel.counts)

# Per-president relative counts
pres.counts <- left_join(pres.total.counts, pres.mean.counts, by = "Word")
pres.counts$Count <- with(pres.counts, Pres.count / Mean.pres.count)
# Plotting helper
pres.plot.words <- function(words, presidents, counts) {
  ggplot(subset(counts, President %in% presidents & Word %in% words), aes(Word, Count, fill = President)) + geom_bar(stat = "identity", position = "dodge") + geom_hline(aes(yintercept = 1), linetype = "dashed") + ylab("Relative count")
}
# Plot some words
pres.plot.words(c("america", "iraq"), c("Barack Obama", "George W. Bush"), pres.counts)
pres.plot.words(c("spend", "save"), c("Barack Obama", "George W. Bush"), pres.counts)

# Make word clouds for some presidents
pres.word.cloud <- function(president, counts) {
  counts <- subset(counts, President == president)
  wordcloud(counts$Word, counts$Count, min.freq = 3.5)
}
# These look a little different!
pres.word.cloud("George W. Bush", pres.counts)
pres.word.cloud("Barack Obama", pres.counts)
