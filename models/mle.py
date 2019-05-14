from textblob import TextBlob
from nltk.lm.models import MLE
from nltk.lm import Vocabulary
import os
import glob
import itertools

path = "../dataset/bbcsport/football"
all_files = glob.glob(os.path.join(path, "*.txt"))

sentences = []
words = []

for filename in all_files:
    file = open(filename, "r+")
    article = TextBlob(''.join(file.read()).replace("\n", " "))
    article_sentences = tuple(article.sentences)
    sentences.append(article_sentences)
    words.append(article.words)

words = list(itertools.chain.from_iterable(words))

language_model = MLE(2)
language_model.fit(sentences, vocabulary_text=Vocabulary(words))

language_model.generate(num_words=1, text_seed='Rooney')

