from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
import nltk
import string
import re

nltk.download('stopwords')
ps = EnglishStemmer()


def data_tokenize_clean(text):
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
    tokens = word_tokenize(text)  # tokenize the comment
    filtered = set()

    for word in tokens:
        word = ps.stem(word)
        word = word.lower()

        filtered.add(word)

    return filtered


class DataCleaner:

    def __init__(self):
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.ps = EnglishStemmer()

    @staticmethod
    def check_is_url(word):
        url = re.findall(r'http?://\S+', word)
        for text in url:
            word.strip(text)

        return word

    def clean_document(self, document):
        document = document.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
        tokenize = word_tokenize(document)  # tokenize the comment
        filtered = set()

        for word in tokenize:
            if word not in self.stop_words and 3 < len(word) < 20:
                word = DataCleaner.check_is_url(word)
                word = self.ps.stem(word)
                word = word.lower()

                filtered.add(word)

        return filtered

    @staticmethod
    def check_if_copyright(comment):
        copyright_words = ["Copyright", "Apache License"]
        for word in copyright_words:
            if word in comment:
                return True

        return False
