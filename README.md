Reverse Dictionary
==================

Ever have that problem when you know there's a specific term for a concept? Thesaurus are usually pretty poor at this task because it's built to link individual words to each other. Not a rough description to a single word.

This tiny hack was built as my submition to an ad-hoc hackday with [Hacker Paradise](hackerparadise.org).

This is a heuristically driven solution, built around [WordNet](https://wordnet.princeton.edu/) via [NLTK](www.nltk.org) and [TextBlob](textblob.readthedocs.org/en/dev/). It attempts to extract the intended entity type via part-of-speech tagging. Then, using its hyponyms, i.e. more specific forms, we select the relavant ones by comparing the hyponym's definition against other parts of the inputted description.

To run, you'll need to download the nltk corpus via:

```shell
$ pip install -U textblob
$ python -m textblob.download_corpora
```