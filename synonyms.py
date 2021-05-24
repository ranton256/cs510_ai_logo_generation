from nltk.corpus import wordnet


class Synonyms:
    def __init__(self):
        pass

    def get_synonyms(self, word) -> list:
        """Returns a list of synonyms for the given word.
        This function takes a string word and look up for its synonyms.
        """
        synonyms = []

        # Iterates over each synonym and append it to the synonyms list
        for syn in wordnet.synsets(word):
            for lm in syn.lemmas():
                synonyms.append(lm.name())

        return synonyms
