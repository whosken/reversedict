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
    def is_not_stopword(term):
        if term.isnumeric():
            return False
        if not stopword_list:
            return True
        return term.lower() not in stopword_list
    return is_not_stopword
