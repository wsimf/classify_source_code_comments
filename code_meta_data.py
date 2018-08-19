import colorama


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

    def print_comment(self):
        print(colorama.Fore.YELLOW + "      [COMMENT] : " + self.comment + "\n")
