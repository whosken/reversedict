Reverse Dictionary
==================

Ever have that problem when you know of the concept yet can't recall the word? Thesaurus are usually pretty poor at this task because it's built to link individual words to each other. Not a rough description to a single word.

This is a solution built around [WordNet](https://wordnet.princeton.edu/) through [NLTK](http://www.nltk.org) and [TextBlob](http://textblob.readthedocs.org/en/dev/). It utilizes [tfidf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) implemented by [Elasticsearch](https://www.elastic.co/) to index each term by their definitions.

Install
-------

```shell
pip install reversedict
service elasticsearch start # assumes elasticsearch is installed
python cli.py --index
```

Usage
-----

Basic look up

```python
import reversedict
reversdict.lookup('run fast')
```

or

```shell
python cli.py 'run fast'
```
