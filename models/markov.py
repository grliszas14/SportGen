import random
import glob
import os
from textblob import TextBlob
import string
from nltk.corpus import brown


class Markov:

    def __init__(self):
        self.texts = self.read_data('../dataset/bbcsport/football')
        self.texts += self.read_data('../dataset/bnc')
        self.texts += [' '.join(sent).translate(str.maketrans('', '', string.punctuation)) for sent in
                                brown.sents(fileids=['ca11', 'ca12', 'ca13', 'ca14', 'ca15'])]

    def read_data(self, path):
        all_files = glob.glob(os.path.join(path, "*.txt"))
        contents = []
        for filename in all_files:
            path = open(filename, "r+")
            article = TextBlob(
                ''.join(path.read()).replace("\n", " ").translate(str.maketrans('', '', string.punctuation)))
            contents.append(str(article))
        return contents

    def make_rule(self, text, context, rule):
        if rule is None:
            rule = {}
        words = text.split(' ')
        try:
            context_index = text.index(context)
            index = context_index
            for word in words[index:]:
                key = ' '.join(words[index - context_index:index])
                if key in rule:
                    rule[key].append(word)
                else:
                    rule[key] = [word]
                index += 1
        except ValueError:
            pass
        return rule

    def make_string(self, rule, length):
        prefices = random.choice(list(rule.keys())).split(' ')  # random starting words
        text = ' '.join(prefices) + ' '

        for i in range(length):
            try:
                key = ' '.join(prefices)
                suffix = random.choice(rule[key])
                text += suffix + ' '

                for word in range(len(prefices)):
                    prefices[word] = prefices[(word + 1) % len(prefices)]
                prefices[-1] = suffix

            except KeyError:
                return text
        return text

    def generate(self, context, length):
        rule = {}
        for text in self.texts:
            rule = self.make_rule(text, context, rule)
        return self.make_string(rule, length)


if __name__ == '__main__':
    markov = Markov()
    print(markov.generate('miss', 1))
