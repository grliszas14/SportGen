import random
import glob
import os
from textblob import TextBlob
from itertools import chain


class Markov:

    def __init__(self):
        self.text = self.read_data('../dataset/bbcsport/football')

    def read_data(self, path):
        all_files = glob.glob(os.path.join(path, "*.txt"))
        contents = []
        for filename in all_files:
            path = open(filename, "r+")
            article = TextBlob(''.join(path.read()).replace("\n", " "))
            contents.append(str(article))
        contents = ''.join(chain.from_iterable(contents))
        return contents

    def make_rule(self, context):
        rule = {}
        words = self.text.split(' ')
        context_index = self.text.index(context)

        index = context_index
        for word in words[index:]:
            key = ' '.join(words[index - context_index:index])
            if key in rule:
                rule[key].append(word)
            else:
                rule[key] = [word]
            index += 1

        return rule

    def make_string(self, rule, length):
        prefices = random.choice(list(rule.keys())).split(' ')  # random starting words
        string = ' '.join(prefices) + ' '

        for i in range(length):
            try:
                key = ' '.join(prefices)
                suffix = random.choice(rule[key])
                string += suffix + ' '

                for word in range(len(prefices)):
                    prefices[word] = prefices[(word + 1) % len(prefices)]
                prefices[-1] = suffix

            except KeyError:
                return string
        return string

    def generate(self, context, length):
        rule = self.make_rule(context)
        return self.make_string(rule, length)


if __name__ == '__main__':
    markov = Markov()
    print(markov.generate('Rooney', 3))
