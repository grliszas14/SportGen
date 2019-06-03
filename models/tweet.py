from collections import defaultdict
from textblob import TextBlob
from nltk.util import trigrams
from random import random
import pandas as pd


class Tweet:

    def __init__(self, path, k=0):
        self.sentences = self.load_data(path)
        self.model = self.fit(k)

    def load_data(self, path):
        df = pd.read_csv(path, sep=";")
        sentences = []
        for tweet in df.values:
            sentences.append([str(word) for word in TextBlob(tweet[0]).words])
        return sentences

    def fit(self, k):
        model = defaultdict(lambda: defaultdict(lambda: 0))
        for sentence in self.sentences:
            for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
                model[(w1, w2)][w3] += 1

        for w1_w2 in model:
            total_count = float(sum(model[w1_w2].values()))
            occurences = len(model[w1_w2])
            for w3 in model[w1_w2]:
                model[w1_w2][w3] = (model[w1_w2][w3] + k) / (total_count + k * occurences)
        return model

    def generate(self, context=None):
        text = [None, context]
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
        return ' '.join([t for t in text if t])


if __name__ == '__main__':
    # tweet = Tweet("../dataset/tweets_processed.csv")
    tweet = Tweet("../dataset/tweets_processed.csv", k=2)
    print(tweet.generate(context='goal'))
    print(tweet.generate(context='champion'))
    print(tweet.generate(context='Zlatan'))
    print(tweet.generate(context='Russia'))
    print(tweet.generate(context='penalty'))
