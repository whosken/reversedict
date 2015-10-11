import textblob

import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'stopwords.txt')

def load():
    stop_words = textblob.blob.WordList([])
    for line in open(path):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words