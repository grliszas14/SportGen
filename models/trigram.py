from collections import defaultdict
from textblob import TextBlob
from nltk.util import trigrams
from nltk.corpus import brown
import os
import glob
from random import random
from itertools import chain


class Trigram:
    bbc_path = "../dataset/bbcsport/football"
    bbc = glob.glob(os.path.join(bbc_path, "*.txt"))
    bnc_path = "../dataset/bnc"
    bnc = glob.glob(os.path.join(bnc_path, "*.txt"))

    def __init__(self):
        self.sentences = self.load_data(Trigram.bbc)
        self.sentences += self.load_data(Trigram.bnc)
        self.sentences += [list(sent) for sent in brown.sents(fileids=['ca11', 'ca12', 'ca13', 'ca14', 'ca15'])]
        self.model = self.fit()

    def load_data(self, files):
        sentences = []
        for filename in files:
            file = open(filename, "r+")
            article = TextBlob(''.join(file.read()).replace("\n", " "))
            article_sentences = [[str(word) for word in sentence.words] for sentence in article.sentences]
            sentences.append(article_sentences)

        return list(chain.from_iterable(sentences))

    def fit(self):
        model = defaultdict(lambda: defaultdict(lambda: 0))
        for sentence in self.sentences:
            for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
                model[(w1, w2)][w3] += 1

        for w1_w2 in model:
            total_count = float(sum(model[w1_w2].values()))
            for w3 in model[w1_w2]:
                model[w1_w2][w3] /= total_count
        return model

    def generate(self, min_prob):
        text = [None, None]
        prob = 1.0
        sentence_finished = False

        while not sentence_finished:
            r = random()
            accumulator = .0
            for word in self.model[tuple(text[-2:])].keys():
                accumulator += self.model[tuple(text[-2:])][word]
                if accumulator >= r:
                    prob *= self.model[tuple(text[-2:])][word]
                    text.append(word)
                    break
            if text[-2:] == [None, None]:
                sentence_finished = True
        print(prob)
        return ' '.join([t for t in text if t])


if __name__ == '__main__':
    trigram = Trigram()
    print(trigram.generate(min_prob=0.9))
