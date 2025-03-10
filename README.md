# TREC-Search-Engine-Components
Components of a web search engine using various heavily researched theories and implementations of text and query processing, indexing, retrieval, ranking, evaluation, and analysis. Processes and tests use various TREC datasets and formats.



Different implementations of text processing based on past and current research. Includes tokenizing, stopping, and stemming. Analysis of term statistics in accordance with Heaps' and Zipf's Laws.

At a high level:
"
  It will read in the (gzip compressed) input file and break it into tokens (loosely speaking, "words") using spaces or a fancier approach.
  It will optionally remove tokens that match stopwords in a provided list.
  It will optionally stem those tokens to their root form using a simple suffix-s stemmer or the Porter stemmer.
  It will calculate some statistics and summar[ize] information about the resulting tokens.
  It will generate incremental and cumulative information about the tokens the system encounters and generates.
" - Professor James Allan at the University of Massachusetts Amherst.

Implementation(s):
  - Takes a text file as input
  - /Tokenizing/
    - White-space separated tokens
    - 4-gram separated tokens
    - Complex tokenizer that handles URLs, currency, punctuation, symbols, abbreviations, etc.
  - /Stopping/
    - Removes stop words (highly common and redundant words that provide little to no meaning, e.g. in, of, and, the, is, etc.)
  - /Stemming/
    -  suffix-s stemmer
    -  Porter stemmer (algorithm for fast complex token normalization)

