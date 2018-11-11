import os
from code_meta_data import SourceCodeMetadata


class JavaFileInspector:

    def __init__(self, directory=None):
        if directory is None:
            self.directory = os.getcwd()
        else:
            self.directory = directory

    # get all the files in the provided directory with the file extension .java
    # returns a dictionary of all the files containing the full file path and the file name
    def __get_all_files(self):
        print("Getting files in the path " + self.directory)
        file_list = []

        for root, directories, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".java"):
                    file_list.append(os.path.join(root, file))

        print("Found {} files in the path {}".format(len(file_list), self.directory))
        return file_list

    @staticmethod
    def __get_comments_in_file(file):
        comments_in_file = []  # array to hold all comments in the file
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
                    print("Omitted '{}' [Unknown comment - Starting with *] in file {}".format(line, file))

            if line.endswith("*/"):
                is_multiline = True
                if data is not None:
                    string = line.lstrip("/*").rstrip("*/").strip()
                    if data.comment != string:
                        data.append_comment(string)

                    comments_in_file.append(data)
                    data = None
                else:
                    print("Omitted '{}' [Unknown Comment] in file {}".format(line, file))

            if not is_multiline:
                code, separator, comment = line.partition("//")
                if len(separator) is not 0:
                    comments_in_file.append(SourceCodeMetadata(comment))

        return comments_in_file

    # get a list of SourceCodeMetadata for the comments found in the java file
    def get_comments(self):
        file_list = self.__get_all_files()
        if len(file_list) == 0:
            print("Did not find any files to read")
            return

        comments_data = {}
        for item in file_list:
            file = open(item, "r")
            comments_data[item] = JavaFileInspector.__get_comments_in_file(file)
            print("Found {} comments in file {}".format(len(comments_data[item]), item))
            file.close()

        return comments_data
