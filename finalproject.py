import math

def clean_text(txt):
    """Clean the text and return a list of words."""
    punctuation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
    for symbol in punctuation:
        txt = txt.replace(symbol, '')
    return txt.lower().split()

def stem(s):
    """Return the stem of a word."""
    cases = {
        "ies": "y",
        "es": "",
        "s": "",
    }
    for case, replacement in cases.items():
        if s.endswith(case):
            return s[:len(s) - len(case)] + replacement
    return s

def compare_dictionaries(d1, d2):
    if d1 == {}:
        return -50

    total = sum(d1.values())
    score = 0
    for key, value in d2.items():
        if key in d1:
            probability = d1[key] / total
            score += math.log(probability) * value
        else:
            default_probability = 0.5 / total
            score += math.log(default_probability) * value

    return score

class TextModel:
    def __init__(self, model_name):
        """Initialize the TextModel object."""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.first_letters = {}
        self.additional_feature = {}


    def __repr__(self):
        """Return a string representation of the TextModel."""
        return (f"text model name: {self.name}\n"
                f"  number of words: {len(self.words)}\n"
                f"  number of word lengths: {len(self.word_lengths)}\n"
                f"  number of stems: {len(self.stems)}\n"
                f"  number of sentence lengths: {len(self.sentence_lengths)}\n"
                f"  number of first letters: {len(self.first_letters)}\n"
                f"  number of additional features: {len(self.additional_feature)}") 


    def add_string(self, s):
        sentences = s.split(".")
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        for sentence in sentences:
            words = clean_text(sentence)
            sentence_length = len(words)

            if sentence_length in self.sentence_lengths:
                self.sentence_lengths[sentence_length] += 1
            else:
                self.sentence_lengths[sentence_length] = 1

            for word in words:
                word_stem = stem(word)
                if word_stem in self.stems:
                    self.stems[word_stem] += 1
                else:
                    self.stems[word_stem] = 1

                if word in self.words:
                    self.words[word] += 1
                else:
                    self.words[word] = 1

                word_length = len(word)
                if word_length in self.word_lengths:
                    self.word_lengths[word_length] += 1
                else:
                    self.word_lengths[word_length] = 1

                if word in self.additional_feature:
                    self.additional_feature[word] += 1
                else:
                    self.additional_feature[word] = 1
                
    def add_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf8', errors='ignore') as file:
                text = file.read()
                self.add_string(text)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def save_model(self):
        words_filename = f"{self.name}_words.txt"
        with open(words_filename, 'w') as words_file:
            for key, value in self.words.items():
                words_file.write(f"{key}:{value}\n")

        lengths_filename = f"{self.name}_word_lengths.txt"
        with open(lengths_filename, 'w') as lengths_file:
            for key, value in self.word_lengths.items():
                lengths_file.write(f"{key}:{value}\n")

        stems_filename = f"{self.name}_stems.txt"
        with open(stems_filename, 'w') as stems_file:
            for key, value in self.stems.items():
                stems_file.write(f"{key}:{value}\n")

        sentence_lengths_filename = f"{self.name}_sentence_lengths.txt"
        with open(sentence_lengths_filename, 'w') as sentence_lengths_file:
            for key, value in self.sentence_lengths.items():
                sentence_lengths_file.write(f"{key}:{value}\n")
        print("Saved sentence_lengths:", self.sentence_lengths)

        additional_feature_filename = f"{self.name}_additional_feature.txt"
        with open(additional_feature_filename, 'w') as additional_file:
            for key, value in self.additional_feature.items():
                additional_file.write(f"{key}:{value}\n")

    def read_model(self):
        words_filename = f"{self.name}_words.txt"
        try:
            with open(words_filename, 'r') as words_file:
                self.words = {}
                for line in words_file:
                    key, value = line.strip().split(':')
                    self.words[key] = int(value)
        except FileNotFoundError:
            print(f"Words file '{words_filename}' not found.")

        lengths_filename = f"{self.name}_word_lengths.txt"
        try:
            with open(lengths_filename, 'r') as lengths_file:
                self.word_lengths = {}
                for line in lengths_file:
                    key, value = line.strip().split(':')
                    self.word_lengths[key] = int(value)
        except FileNotFoundError:
            print(f"Word lengths file '{lengths_filename}' not found.")

        stems_filename = f"{self.name}_stems.txt"
        try:
            with open(stems_filename, 'r') as stems_file:
                self.stems = {}
                for line in stems_file:
                    key, value = line.strip().split(':')
                    self.stems[key] = int(value)
        except FileNotFoundError:
            print(f"Stems file '{stems_filename}' not found.")

        sentence_lengths_filename = f"{self.name}_sentence_lengths.txt"
        try:
            with open(sentence_lengths_filename, 'r') as sentence_lengths_file:
                self.sentence_lengths = {}
                for line in sentence_lengths_file:
                    key, value = line.strip().split(':')
                    self.sentence_lengths[int(key)] = int(value)
        except FileNotFoundError:
            print(f"Sentence lengths file '{sentence_lengths_filename}' not found.")
        print("Read sentence_lengths:", self.sentence_lengths) 

        additional_feature_filename = f"{self.name}_additional_feature.txt"
        try:
            with open(additional_feature_filename, 'r') as additional_file:
                self.additional_feature = {}
                for line in additional_file:
                    key, value = line.strip().split(':')
                    self.additional_feature[key] = int(value)
        except FileNotFoundError:
            print(f"Additional feature file '{additional_feature_filename}' not found.")


    def similarity_scores(self, other):
        """Computes and returns a list of similarity scores."""
        scores = []
        scores.append(compare_dictionaries(other.words, self.words))
        scores.append(compare_dictionaries(other.word_lengths, self.word_lengths))
        scores.append(compare_dictionaries(other.stems, self.stems))
        scores.append(compare_dictionaries(other.sentence_lengths, self.sentence_lengths))
        scores.append(compare_dictionaries(other.first_letters, self.first_letters))
        return scores

    def classify(self, source1, source2):
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print(f"scores for {source1.name}: {scores1}")
        print(f"scores for {source2.name}: {scores2}")
        
        source1_higher = 0
        source2_higher = 0
        
        for score1, score2 in zip(scores1, scores2):
            if score1 > score2:
                source1_higher += 1
            else:
                source2_higher += 1
        
        if source1_higher > source2_higher:
            print(f"{self.name} is more likely to have come from {source1.name}")
        else:
            print(f"{self.name} is more likely to have come from {source2.name}")

# Example usage:
def run_tests():
    """ your docstring goes here """
    source1 = TextModel('John')
    source1.add_file('/Users/alicialin/Desktop/CS111/Final Project/JohnGreen.txt')

    source2 = TextModel('Hank')
    source2.add_file('/Users/alicialin/Desktop/CS111/Final Project/HankGreen.txt')

    new1 = TextModel('Beautiful')
    new1.add_file('/Users/alicialin/Desktop/CS111/Final Project/LookingForAlaska.txt')
    new1.classify(source1, source2)

if __name__ == "__main__":
    run_tests()