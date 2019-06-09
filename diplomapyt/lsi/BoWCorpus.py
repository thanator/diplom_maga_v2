from gensim.utils import simple_preprocess


class BoWCorpus(object):
    def __init__(self, docs, dictionary):
        self.docs = docs
        self.dictionary = dictionary

    def __iter__(self):
        for line in self.docs:
            # tokenize
            tokenized_list = simple_preprocess(line, deacc=True)
            # create bag of words
            bow = self.dictionary.doc2bow(tokenized_list, allow_update=True)
            # update the source dictionary (OPTIONAL)
            # lazy return the BoW
            yield bow

