from collections import defaultdict
from textblob import TextBlob
from nltk.util import trigrams
from random import random
import pandas as pd


class Tweet:

    def __init__(self, path):
        self.sentences = self.load_data(path)
        self.model = self.fit()

    def load_data(self, path):
        df = pd.read_csv(path, sep=";")
        sentences = []
        for tweet in df.values:
            sentences.append([str(word) for word in TextBlob(tweet[0]).words])
        return sentences

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

    def generate(self):
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
        return ' '.join([t for t in text if t])


if __name__ == '__main__':
    row = []

    for j in range(1,2):
        column = []
        tweet = Tweet('testdata/small' + str(j) + '.csv')
        for i in range(1,200):
            # Generate 10 tweets
            column.append(tweet.generate())
        row.append(column)

    all_words = []
    for j in range(1):
        for i in range(199):
            words = row[j][i].strip().split(' ')
            for w in words:
                all_words.append(w.lower())

    all_words_processed = list(set(all_words))
    count = 0
    for w in all_words_processed:
        count = count + 1
    print('All different words in generated tweets:' + str(count))

    all_words_processed.sort()

    word_map = {}
    for word in all_words_processed:
        word_map[word] = {}
        for second_word in all_words_processed:
            word_map[word][second_word] = 0

    for j in range(1):
        for i in range(199):
            words = row[j][i].strip().split(' ')
            words.sort()
            for k in range(len(words)):
                for l in range(k, len(words)):
                    word_map[words[k].lower()][words[l].lower()] += 1

    more_than_0 = 0
    more_than_5 = 0
    more_than_10 = 0
    more_than_15 = 0
    more_than_20 = 0
    more_than_25 = 0

    for word in all_words_processed:
        for second_word in all_words_processed:
            if word_map[word][second_word] > 0:
                more_than_0 += 1
            if word_map[word][second_word] > 5:
                more_than_5 += 1
            if word_map[word][second_word] > 10:
                more_than_10 += 1
            if word_map[word][second_word] > 15:
                more_than_15 += 1
            if word_map[word][second_word] > 20:
                more_than_20 += 1
            if word_map[word][second_word] > 25:
                more_than_25 += 1

print('Number of pairs that ocurred more than 0 times:' + str(more_than_0))
print('Number of pairs that ocurred more than 5 times:' + str(more_than_5))
print('Number of pairs that ocurred more than 10 times:' + str(more_than_10))
print('Number of pairs that ocurred more than 15 times:' + str(more_than_15))
print('Number of pairs that ocurred more than 20 times:' + str(more_than_20))
print('Number of pairs that ocurred more than 25 times:' + str(more_than_25))
