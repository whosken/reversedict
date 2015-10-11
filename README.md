Reverse Dictionary
==================

Ever have that problem when you know there's a specific term for a concept? Thesaurus are usually pretty poor at this task because it's built to link individual words to each other. Not a rough description to a single word.

This is a heuristically driven solution, built around [WordNet](https://wordnet.princeton.edu/) through [NLTK](www.nltk.org) and [TextBlob](textblob.readthedocs.org/en/dev/). It attempts to extract the intended entity type via part-of-speech tagging. Then, using its hyponyms, i.e. more specific forms, it selects the relavant ones by comparing the hyponym's definition against other parts of the inputted description.

Install
-------

```shell
pip install reversedict
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

During the basic look up, the engine will attempt to extract the intended word through part-of-speech. To specify the part of speech, use `pos` argument.

```python
reversedict.lookup('run fast', pos='vb')
```

or

```shell
python cli.py --verbose 'run fast'
```