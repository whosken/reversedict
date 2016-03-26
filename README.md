Reverse Dictionary
==================

Ever had that problem when you know of the concept yet can't recall the word? Thesaurus are usually pretty poor at this task, because it's built to link individual words to each other, instead of definitions to a single word.

This solution is built from [WordNet](https://wordnet.princeton.edu/) through [NLTK](http://www.nltk.org) and [TextBlob](http://textblob.readthedocs.org/en/dev/). It utilizes [tfidf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) implemented by [Elasticsearch](https://www.elastic.co/) to index each word by their definitions.

Install
------

```python
# install elasticsearch via https://www.elastic.co/downloads/elasticsearch 
git clone git@github.com:whosken/reversedict.git
cd reversedict
pip install -r requirements.txt
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

Synonym boosting

```shell
python cli.py 'run fast' --synonym sprint
```
