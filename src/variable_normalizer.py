import re

"""Use this script to normalize the variables a user provides in order to match them with the database values.

"""
class NormalizeUserInput():
    def __init__(self):
        pass

    def normalize_major(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name)
        """
        major_re = re.compile(r'\s(C\.?S\.?C\.?|CS|Computer Science|SE|C\.?S\.?)[ ?]', flags=re.I)
        major_search = re.search(major_re, input_text)
        if major_search:
            major_match = major_search.group(1)
            return "CSC", major_match
        return False

    def normalize_season(self, input_text):
        seasons_re = re.compile(r'\s(fall|winter|spring|summer)', flags = re.I)
        seasons_search = re.search(seasons_re, input_text)
        seasons = {"fall": "F", "winter": "W", "spring": "Sp", "summer": "Su"}
        if seasons_search:
            season_match = seasons_search.group(1)
            return seasons[season_match], season_match
        return False

    def search_variables(self, input_text):
        """

        :param input_text: The user's question.
        :return: A dictionary contains the variable-names found as keys and
        (variable-db-name, user's-variable-name) as values.
        """
        user_variables = {}
        normalized_major = self.normalize_major(input_text)
        normalized_season = self.normalize_season(input_text)

        if normalized_major:
            user_variables['major'] = normalized_major
        if normalized_season:
            user_variables['season'] = normalized_season

        return user_variables

normalize_input = NormalizeUserInput()
print(normalize_input.search_variables("Hello c.s. fall"))