import re


class VariableNormalizer:
    def __init__(self):
        pass

    def normalize_major(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name) if "major" in input_text.
        Else returns False.
        """
        major_re = re.compile(r'\s(C\.?S\.?C\.?|CS|Computer Science|SE|C\.?S\.?)[ ?]', flags=re.I)
        major_search = re.search(major_re, input_text)
        if major_search:
            major_match = major_search.group(1)
            return "CSC", major_match
        return False

    def normalize_season(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name) if "season" in input_text.
        Else returns False.
        """
        seasons_re = re.compile(r'\s(fall|winter|spring|summer)', flags = re.I)
        seasons_search = re.search(seasons_re, input_text)
        seasons = {"fall": "F", "winter": "W", "spring": "Sp", "summer": "Su"}
        if seasons_search:
            season_match = seasons_search.group(1)
            return seasons[season_match], season_match
        return False

    def normalize_num_units(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name) if "num-units" in input_text.
        Else returns False.
        """
        units_re = re.compile(r'([0-9]{1,2}) ?units?', flags=re.I)
        units_search = re.search(units_re, input_text)
        if units_search:
            units_match = int(units_search.group(1))
            return units_match, units_match

    def search_variables(self, input_text):
        """

        :param input_text: The user's question.
        :return: A dictionary that contains the variable-names found as keys and
        (variable-db-name, user's-variable-name) as values.
        """
        user_variables = {}
        normalization_paths = [
            ('major', self.normalize_major),
            ('season', self.normalize_season),
            ('num-units', self.normalize_num_units)
        ]

        for path_name, normalizer_function in normalization_paths:
            result = normalizer_function(input_text)
            if result:
                user_variables[path_name] = result
        return user_variables

