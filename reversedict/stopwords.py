import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'stopwords.txt')

def load():
    stop_words = []
    for line in open(path):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word.lower())
    return stop_words

def get_is_not_stopword():
    stopword_list = load()
    return lambda t: not stopword_list or t.lower() not in stopword_list
