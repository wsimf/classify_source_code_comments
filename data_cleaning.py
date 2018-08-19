from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string


class DataCleaner:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def remove_stop_words(self, word_list):
        filtered = []

        for word in word_list:
            if word not in self.stop_words:
                filtered.append(word)

        return filtered

    def string_stemming(self, word_list):
        filtered = set()

        for word in word_list:
            filtered.add(self.ps.stem(word))

        return filtered

    def clean_document(self, document):
        document = document.translate(None, string.punctuation)  # remove punctuations
        tokenize = word_tokenize(document)  # tokenize the comment
        no_stop_words = self.remove_stop_words(tokenize)
        cleaned = self.string_stemming(no_stop_words)

        for index, word in enumerate(cleaned):
            word = word.lower()  # convert to lower case

            cleaned[index] = word

        return cleaned

