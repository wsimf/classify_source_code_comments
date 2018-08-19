import os
import colorama
import javalang
import pandas as pd
import data_cleaning

from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


class SourceCodeMetadata:

    def __init__(self, comment, method=None, params=None, return_value=None):
        self.comment = comment
        self.method = method
        self.params = params
        self.return_value = return_value
        self.is_multiline = False

    def append_comment(self, string):
        if len(self.comment) == 0 or self.comment.isspace():
            self.comment = string
        else:
            seq = (self.comment, string)
            self.comment = " ".join(seq)
            self.is_multiline = True


class FileInspector:

    def __init__(self, directory=None):
        if directory is None:
            self.directory = os.getcwd()
        else:
            self.directory = directory

    # get all the files in the provided directory with the file extension .java
    # returns a dictionary of all the files containing the full file path and the file name
    def get_all_files(self):
        print("Getting files in the path " + self.directory)

        file_list = []

        for root, directories, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".java"):
                    file_list.append(os.path.join(root, file))

        print("Found {} files in the path {}".format(len(file_list), self.directory))
        return file_list

    # get a list of SourceCodeMetadata for the comments found in the java file
    def get_comments(self, file_list):
        if file_list is None:
            file_list = self.get_all_files()

        if len(file_list) == 0:
            print("Did not find any files to read")
            return

        comments_data = {}
        for item in file_list:
            file = open(item, "r")
            comments_in_file = []
            data = None  # SourceCodeMetadata instance for this file
            file_text = ""

            for line in file:
                seq = (file_text, line)
                file_text = "".join(seq)

                line = line.strip().rstrip("\n")  # remove white spaces & /n at the beginning and end of the line
                is_multiline = False

                if line.startswith("/*"):
                    is_multiline = True
                    if data is None:
                        data = SourceCodeMetadata(line.lstrip("/*").rstrip("*/").strip())
                    else:
                        data.append_comment(line)

                if line.startswith("*"):
                    if data is not None:
                        is_multiline = True
                        data.append_comment(line.lstrip("*").strip())
                    else:
                        print("Omitted '{}' [Unknown comment - Starting with *] in file {}".format(line, item))

                if line.endswith("*/"):
                    is_multiline = True
                    if data is not None:
                        string = line.lstrip("/*").rstrip("*/").strip()
                        if data.comment != string:
                            data.append_comment(string)

                        comments_in_file.append(data)
                        data = None
                    else:
                        print("Omitted '{}' [Unknown Comment] in file {}".format(line, item))

                if not is_multiline:
                    code, separator, comment = line.partition("//")
                    if len(separator) is not 0:
                        comments_in_file.append(SourceCodeMetadata(comment))

            comments_data[item] = comments_in_file
            print("Found {} comments in file {}".format(len(comments_in_file), item))
            file.close()

            # tree = javalang.parse.parse(file_text)  # parse into a java source code file
            #
            # count = 0
            # for path, node in tree:
            #     print('path: {}'.format(path))
            #     if hasattr(node, 'documentation'):
            #         if hasattr(node, 'name'):
            #             print('name: {}'.format(node.name))
            #         print('documentation: {}'.format(node.documentation))
            #         count += 1
            #         print(" ")
            # print(count)

        return pd.Series(comments_data)


def main():
    colorama.init()
    inspector = FileInspector("/Users/Sudara/Offline/source-code-analyser-resources")
    file_list = inspector.get_all_files()
    comments_data = inspector.get_comments(file_list)
    comments = {}

    for key, value in comments_data.items():
        print(colorama.Fore.GREEN + "[FILE] : " + key)
        for item in value:
            print(colorama.Fore.YELLOW + "      [COMMENT] : " + item.comment + "\n")
            comments["tokenized"] = data_cleaning.clean_document(item)

    words = data_cleaning.clean_document()
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comments)

    true_k = 2
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind])


if __name__ == '__main__': main()
