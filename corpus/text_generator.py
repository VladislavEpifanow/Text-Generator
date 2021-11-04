from nltk.tokenize import WhitespaceTokenizer


# Class of the corpus of our text
# Here we tokenize our text and prepare it to build a model
# And get statistic about it.
class Corpus:
    def __init__(self):
        self.tokens = []
        self.tokens_count = 0
        self.unique_tokens_count = 0

    def tokenize_dataset(self, filename: str, encoding: str):
        with open(filename, "r", encoding=encoding) as file_obj:
            text_from_file = file_obj.read()
        wst = WhitespaceTokenizer()
        self.tokens = wst.tokenize(text_from_file)
        self.tokens_count = len(self.tokens)
        self.unique_tokens_count = len(set(self.tokens))

    def print_statistics(self):
        print("Corpus statistics")
        print("All tokens:", self.tokens_count)
        print("Unique tokens:", self.unique_tokens_count)


def main():
    corpora = Corpus()
    filename = input()
    corpora.tokenize_dataset(filename, "utf-8")
    corpora.print_statistics()
    #Open Tokens Loop
    while True:
        index = input()
        if index == "exit":
            break
        try:
            print(corpora.tokens[int(index)])
        except ValueError:
            print("Type Error. Please input an integer.")
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")


if __name__ == '__main__':
    main()