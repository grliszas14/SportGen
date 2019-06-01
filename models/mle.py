from textblob import TextBlob
from nltk.lm.models import MLE
from nltk.lm import Vocabulary
from nltk.util import ngrams
import os
import glob
import itertools
import re

path = "../dataset/bbcsport/football"
all_files = glob.glob(os.path.join(path, "*.txt"))

sentences = []
words = []

for filename in all_files:
    file = open(filename, "r+")
    article = TextBlob(''.join(file.read()).replace("\n", " "))
    article_words = [str(word) for word in article.words]
    words.append(article_words)
    article_sentences = list(ngrams(article_words, 5))
    sentences.append(article_sentences)

words = list(itertools.chain.from_iterable(words))
# sentences = list(itertools.chain.from_iterable(sentences))
# sentences = re.sub(r'[^a-zA-Z0-9\s]', ' ', sentences)
# tokens = [token for token in sentences.split(" ") if token != ""]

# ngrams = ngrams(words, 5)
# vocabulary = Vocabulary(words)

language_model = MLE(2)
language_model.fit(sentences, vocabulary_text=Vocabulary(words))

a = language_model.generate(num_words=3, text_seed='Rooney')

print(a)

