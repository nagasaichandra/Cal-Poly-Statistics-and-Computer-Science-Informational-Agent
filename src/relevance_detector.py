import unittest

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from .questions import get_questions, get_variable_values
from .query_scanner import QueryScanner

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) or 0 for ss in synsets2])

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    score /= count
    return score


class RelevanceDetector:
    """ Determines if a question can be answered and what query it most closely matches """

    def __init__(self):
        self.questions = get_questions()
        self.query_scanner = QueryScanner()

    def get_subset_questions_list(self, variables_query):
        """

        :param query: User's input question.
        :return: Subset of questions with the same variables as the query.
        """
        variables_questions = [(question[0], question[1], self.query_scanner.find_within_brackets(question[0])) for question in self.questions]
        final_list = list(filter(lambda x: self.match_variables(variables_query, x[2]), variables_questions))
        return [(question[0], question[1]) for question in final_list]

    def match_variables(self, variables_query, variables_question):
        return set(variables_query.keys()) >= set(variables_question)

    def most_relevant_query(self, query):
        reformat_query = self.query_scanner.clean_user_question(query)
        subset_questions = self.get_subset_questions_list(reformat_query[1])

        return max(subset_questions, key=lambda question: sentence_similarity(reformat_query[0], question[0]))


class TestRelevanceDetector(unittest.TestCase):

    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
