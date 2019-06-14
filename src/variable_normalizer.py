import re
import unittest


class VariableNormalizer:
    def __init__(self):
        pass

    # def normalize_major(self, input_text):
    #     """
    #
    #     :param input_text: A user's question.
    #     :return: A tuple indicating: (variable-db-name, user's-variable-name) if "major" in input_text.
    #     Else returns False.
    #     """
    #     major_re = [re.compile(r'\s(C\.?S\.?C\.?|CS|Computer Science|C\.?S\.?)[ ?]', flags=re.I),
    #                 re.compile(r'\s(SE|software engineering|software)[ ?]', flags=re.I)]
    #
    #     csc_search = re.search(major_re[0], input_text)
    #     if csc_search:
    #         major_match = csc_search.group(1)
    #         return "CSC", major_match
    #
    #     csc_search = re.search(major_re[1], input_text)
    #     if csc_search:
    #         major_match = csc_search.group(1)
    #         return "SE", major_match
    #
    #     return False

    def normalize_season(self, input_text):
        """

        :param input_text: A user's question.
        :return: A tuple indicating: (variable-db-name, user's-variable-name) if "season" in input_text.
        Else returns False.
        """
        seasons_re = re.compile(r'\s(fall|winter|spring|summer|Sp|F|W|Su)[\s?]', flags = re.I)
        seasons_search = re.search(seasons_re, input_text)
        seasons = {"fall": "F", "winter": "W", "spring": "Sp", "summer": "Su", "Sp": "Sp", "F":"F", "W":"W", "Su":"Su"}
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
            return division_match, division_match + " division"

    def normalize_class_level(self, input_text):
        class_re = re.compile(r'(freshman|sophmore|junior|senior)', flags=re.I)
        class_search = re.search(class_re, input_text)
        if class_search:
            class_match = class_search.group(1)
            return class_match, class_match + " student"

    def normalize_ge_area(self, input_text):
        ge_re = [re.compile(r'ge area ([abcdef|ABCDEF])', flags=re.I),
                 re.compile(r'ge ([abcdef|ABCDEF])', flags=re.I), re.compile(r'area ([abcdef|ABCDEF])[ ?]', flags=re.I)]
        for search_term in ge_re:
            ge_search = re.search(search_term, input_text)
            if ge_search:
                ge_match = ge_search.group(1)
                return ge_match.capitalize(), "GE AREA {}".format(ge_match)

    def normalize_major(self, input_text):
        bachelor_re = [re.compile(r'\s(C\.?S\.?C\.?|CS|Computer Science|C\.?S\.?)[ ?]', flags=re.I),
                    re.compile(r'\s(SE|software\sengineering|software)[ ?]', flags=re.I)]

        csc_search = re.search(bachelor_re[0], input_text)
        se_search = re.search(bachelor_re[1], input_text)

        if csc_search:
            return "CSC", "CSC"
        elif se_search:
            return "SE", "SE"

    def normalize_minor(self, input_text):
        minor_ds_re = re.compile(r'data science minor|ds minor|data minor', flags=re.I)
        minor_ds_search = re.search(minor_ds_re, input_text)

        minor_cs_re = re.compile(r'cs\sminor|CSC\sminor|computer\sscience\sminor|c\.s\.c\sminor|c\.s\.\sminor', flags=re.I)
        minor_cs_search = re.search(minor_cs_re, input_text)

        minor_art_re = re.compile(r'Computing\sfor\sInteractive\sArts\sminor|interactive\sminor|interactive\sarts\sminor|CIA\s|interactive\sminor', flags=re.I)
        minor_art_search = re.search(minor_art_re, input_text)

        ie_concentration_re = re.compile(r'Interactive\sEntertainment|\sIE\s|Interactive\sEnt', flags = re.I)
        ie_concentration_search = re.search(ie_concentration_re, input_text)

        if minor_ds_search:
            return 'Data Science minor', 'Data Science minor'
        elif minor_cs_search:
            return 'CSC minor', 'CSC minor'
        elif minor_art_search:
            return 'CIA', 'Computing for Interactive Arts minor'
        elif ie_concentration_search:
            return 'IE', 'Interactive Entertainment Concentration'

    def normalize_year_range(self, input_text):
        year_re = re.compile(r' (20[12][0-9])-?')
        year_search = re.search(year_re, input_text)
        if year_search:
            year_match = int(year_search.group(1))
            if year_match >= 2011 and year_match < 2013:
                return '2011 - 2013', '2011 - 2013'
            elif year_match >= 2013 and year_match < 2015:
                return '2013 - 2015', '2013 - 2015'
            elif year_match >= 2015 and year_match < 2017:
                return '2015 - 2017', '2015 - 2017'
            elif year_match >= 2017 and year_match < 2019:
                return '2017 - 2019', '2017 - 2019'
            elif year_match >= 2019 and year_match <= 2020:
                return '2019 - 2020', '2019 - 2020'



    def normalize_gpa(self, input_text):
        gpa_re = [re.compile(r'gpa of ([0-4]\.?[0-9]?[0-9]?)', flags=re.I),
                 re.compile(r'gpa ([0-4]\.?[0-9]?[0-9]?)', flags=re.I),
                 re.compile(r'([0-4]\.?[0-9]?[0-9]?) gpa', flags=re.I)]
        for search_term in gpa_re:
            gpa_search = re.search(search_term, input_text)
            if gpa_search:
                gpa_match = gpa_search.group(1)
                return (float(gpa_match), float(gpa_match))



    def normalize_support_elective(self, input_text):
        required = re.compile(r'(required?)', flags=re.I)
        approved = re.compile(r'(approved\selectives?)', flags=re.I)
        technical = re.compile(r'(technical)', flags=re.I)
        support = re.compile(r'(support)', flags=re.I)

        normalization_support_paths = [
            ("Required Course", required),
            ("Approved Elective", approved),
            ("Technical Elective", technical),
            ("Support Course", support)
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
            ('season', self.normalize_season),
            ('num-units', self.normalize_num_units),
            ('elective-type', self.normalize_support_elective),
            ('division-level', self.normalize_division_level),
            ('class-level', self.normalize_class_level),
            ('ge-area', self.normalize_ge_area),
            ('minor', self.normalize_minor),
            ('major', self.normalize_major),
            ('year-range', self.normalize_year_range)
        ]

        for path_name, normalizer_function in normalization_paths:
            result = normalizer_function(input_text)
            if result:
                user_variables[path_name] = result
        if "minor" in set(user_variables.keys()):
            if "major" in set(user_variables.keys()):
                user_variables.pop("major")
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