import os
import colorama
import javalang
import pandas as pd
from data_cleaning import DataCleaner
from code_meta_data import SourceCodeMetadata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


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
    data_cleaning = DataCleaner()

    file_list = inspector.get_all_files()
    comments_data = inspector.get_comments(file_list)
    comments = {}

    for key, value in comments_data.items():
        print(colorama.Fore.GREEN + "[FILE] : " + key)
        for item in value:
            item.print_comment()
            comments["tokenized"] = data_cleaning.clean_document(item)


if __name__ == '__main__':
    main()
