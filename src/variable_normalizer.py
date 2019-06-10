import re
import unittest


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
            if units_match == 1:
                user_units = "%s unit"%units_match
            else:
                user_units = "%s units"%units_match
            return units_match, user_units
        return False

    def normalize_division_level(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name) if "division-level" in input_text.
        Else returns False.
        """
        division_re = re.compile(r'(upper|lower) division|(upper|lower) level', flags=re.I)
        division_search = re.search(division_re, input_text)
        if division_search:
            division_match = division_search.group(1)
            return division_match, division_match

    def normalize_class_level(self, input_text):
        class_re = re.compile(r'(freshman|sophmore|junior|senior)', flags=re.I)
        class_search = re.search(class_re, input_text)
        if class_search:
            class_match = class_search.group(1)
            return class_match, class_match + " class level "

    def normalize_ge_area(self, input_text):
        ge_re = re.compile(r'ge area ([abcdef|ABCDEF])|ge ([abcdef|ABCDEF])', flags=re.I)
        ge_search = re.search(ge_re, input_text)
        if ge_search:
            ge_match = ge_search.group(1)
            return ge_match, "GE AREA {}".format(ge_match)

    def normalize_minor(self, input_text):
        minor_ds_re = re.compile(r'data science minor|ds minor|data minor', flags=re.I)
        minor_search = re.search(minor_ds_re, input_text)
        if minor_search:
            return 'ds-minor', 'Data Science minor'

    def normalize_year_range(self, year_range):
        pass



    def normalize_support_elective(self, input_text):
        life_science = re.compile(r'(life sciences?)', flags=re.I)
        math_stat = re.compile(r'(\bmath|\bstat|\bstatistics|\bmathematics)', flags=re.I)
        physical_science = re.compile(r'(physical science)', flags=re.I)
        additional_science = re.compile(r'(additional science)', flags=re.I)
        support_courses = re.compile(r'(support courses?)', flags=re.I)

        normalization_support_paths = [
            ("Life Science Support Elective", life_science),
            ("Mathematics/Statistics Support elective", math_stat),
            ("Additional Science Support Elective 6", additional_science),
            ("Physical Science Support Elective", physical_science),
            ("SUPPORT COURSES", support_courses)
        ]

        for path, regex_compile in normalization_support_paths:
            user_search = re.search(regex_compile, input_text)
            if user_search:
                user_match = user_search.group(1)
                return (path, user_match)


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
            ('num-units', self.normalize_num_units),
            ('elective-type', self.normalize_support_elective),
            ('division-level', self.normalize_division_level),
            ('class-level', self.normalize_class_level),
            ('ge-area', self.normalize_ge_area),
            ('minor', self.normalize_minor)
        ]

        for path_name, normalizer_function in normalization_paths:
            result = normalizer_function(input_text)
            if result:
                user_variables[path_name] = result
        return user_variables


class TestVariableNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = VariableNormalizer()

    def test_num_units(self):
        units, user_input = self.normalizer.normalize_num_units("8 units")
        self.assertEqual(units, 8)
        self.assertEqual(user_input, "8 units")

        units, user_input = self.normalizer.normalize_num_units("4 units?")
        self.assertEqual(units, 4)
        self.assertEqual(user_input, "4 units")

        units, user_input = self.normalizer.normalize_num_units("1unit")
        self.assertEqual(units, 1)
        self.assertEqual(user_input, "1 unit")


if __name__ == "__main__":
    unittest.main()