from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter
from random import choices, randint


# Class of the corpus of our text
# Here we tokenize our text and prepare it to build a model
# And get statistic about it.
class Corpus:
    def __init__(self):
        self.tokens = []
        self.tokens_count = 0
        self.unique_tokens_count = 0
        self.bigrams = []
        self.number_of_bigrams = 0
        self.trigrams = []
        self.number_of_trigrams = 0

    def tokenize_dataset(self, filename: str, encoding: str):
        with open(filename, "r", encoding=encoding) as file_obj:
            text_from_file = file_obj.read()
        wst = WhitespaceTokenizer()
        self.tokens = wst.tokenize(text_from_file)
        self.tokens_count = len(self.tokens)
        self.unique_tokens_count = len(set(self.tokens))

    def make_trigrams(self):

        self.trigrams = [[" ".join(self.tokens[i:i+2]), self.tokens[i + 2]] for
                         i in range(self.tokens_count - 2)]

        self.number_of_trigrams = len(self.trigrams)
        return self.trigrams

    def make_bigrams(self):
        self.bigrams = [[self.tokens[i], self.tokens[i + 1]] for i in range(self.tokens_count - 1)]
        self.number_of_bigrams = len(self.bigrams)
        return self.bigrams


# Class of simple Markov Model
# Here we put some n-grams and get some sentence
class MarkovChainModel:
    def __init__(self):
        self.model = defaultdict(Counter)

    def build_model(self, ngrams):
        for elem in ngrams:
            self.model[elem[0]][elem[1]] += 1

    def getting_random_sentence(self, min_word_in_sentence, number_of_ngrams):

        sentence = [choices(list(self.model.keys()))[0]]

        while not sentence[0][0].isupper() or sentence[0].split()[0][-1] in "!?.":
            sentence[0] = choices(list(self.model.keys()))[0]
        current_word = sentence[0]
        if sentence[0][-1] in "!?.":
            word_count = 0
        else:
            word_count = 1

        # В цикле снизу иногда происходят зацикливания, причину пока не выяснил
        while True:
            next_word = choices(list(self.model[current_word].keys()),
                                list(self.model[current_word].values()))[0]

            # print(next_word, current_word)
            if next_word[-1] in '!.?':
                if word_count >= min_word_in_sentence:
                    sentence.append(next_word)
                    break
                elif word_count > 2:
                    if number_of_ngrams == 3:
                        del sentence[1:]
                        if sentence[0][-1] in "?!.":
                            word_count = 0
                        else:
                            word_count = 2
                    else:
                        sentence.pop(-1)
                        word_count -= 1
                        current_word = sentence[-1]
                    continue

            sentence.append(next_word)
            if number_of_ngrams == 3:
                current_word = " ".join([current_word.split()[-1], next_word])
            elif number_of_ngrams == 2:
                current_word = next_word
            word_count += 1
        return " ".join(sentence)


def main():
    corpora = Corpus()
    filename = input()
    corpora.tokenize_dataset(filename, "utf-8")
    bigrams = corpora.make_bigrams()
    trigrams = corpora.make_trigrams()
    model = MarkovChainModel()
    model.build_model(trigrams)
    # model.build_bigrams_model(bigrams)
    for i in range(10):
        print(model.getting_random_sentence(5, 3))


if __name__ == '__main__':
    main()
