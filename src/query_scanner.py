from src import variable_normalizer
from .database_connection import make_connection
import re
import json
from .variable_normalizer import VariableNormalizer
import unittest


class QueryScanner:
    def __init__(self):
        self.normalize_input = VariableNormalizer()
        self.response_variables_queries = self.read_json("response_variables.json")

    def read_json(self, filename):
        """ Reads the json files in the top directory and returns them as dictionary objects. """
        with open(filename, "r") as user_variables:
            variable_re_dict = json.load(user_variables)
            return variable_re_dict

    def clean_user_question(self, question):
        """

        :param question: A user's question.
        :return: Returns the question with variables replaced by [variable_name] and a dictionary
        of user's variables.
        """
        question_clean = question
        user_variables = self.normalize_input.search_variables(question)
        for key, val in user_variables.items():
            replace_string = "%s" % (val[1])
            new_string = "[%s]" % (key)
            question_clean = question_clean.replace(replace_string, new_string)
        return question_clean, user_variables

    def clean_response_user_variables(self, response_text, user_variables):
        """

        :param response_text: The response to a user's question with all variables in brackets.
        Important: Response variables must also be in brackets.

        :param user_variables: A dictionary of {variable-name: (variable-db-name, user-variable),..}
        :return: The response text cleaned of user-variables.
        """
        clean_response_text = response_text
        var_names = list(user_variables.keys())
        for var_name in var_names:
            var_replacement = user_variables[var_name][1]
            clean_response_text = self.replace_variable(clean_response_text, var_name, var_replacement)
        return clean_response_text

    def clean_query_user_variables(self, query_text, user_variables):
        """

        :param query_text: The select statement with user_variables in brackets.
        :param user_variables:  A dictionary of {variable-name: (variable-db-name, user-variable),..}
        :return: A query with its user variables replaced by the variable-db-name.
        """
        clean_query_text = query_text
        var_names = list(user_variables.keys())
        for var_name in var_names:
            var_replacement = user_variables[var_name][0]
            clean_query_text = self.replace_variable(clean_query_text, var_name, var_replacement)
        return clean_query_text

    def clean_response_query(self, response_text, user_variables):
        """

        :param response_text: The response text with user-variables and response-variables in brackets.
        :param user_variables:
        :return:
        """
        clean_response_text = self.clean_response_user_variables(response_text, user_variables)
        query_variables = self.find_within_brackets(clean_response_text)
        if query_variables:
            for query_var in query_variables:
                query_sub = self.response_variables_queries[query_var]
                # First clean query.
                clean_query = self.clean_query_user_variables(query_sub, user_variables)
                query_response_list = self.execute_query(clean_query)

                if query_response_list:
                    query_response = ', '.join(query_response_list)
                else:
                    query_response = "(could not find %s)" % (query_var)

                clean_response_text = self.replace_variable(clean_response_text, query_var, query_response)

        return clean_response_text

    def find_within_brackets(self, text):
        """

        :param text:
        :return: A list of variable names that are inside of brackets in text.
        """
        return re.findall(r'\[(.*?)\]', text)

    def replace_variable(self, text, variable_name, substitution):
        """

        :param text: A text with the variable-name in brackets.
        :param variable_name: The variable-name to substitute.
        :param substitution: The value to subsitute [variable-name] to.
        :return: The cleaned text, with [variable-name] substituted with substition.
        """
        variable_re_string = r'\[{}\]'.format(variable_name).replace("'", "")
        clean_text = re.sub(r'' + variable_re_string, substitution, text)
        return clean_text

    def execute_query(self, query):
        connection = make_connection()
        with connection.cursor() as cursor:
            try:
                cursor.execute('''%s'''% query)
                response_list = cursor.fetchall()
                connection.commit()
                tuple_response = [list(response.values())[0] for response in response_list]
                if len(tuple_response) > 0:
                    return tuple_response
                else:
                    return False
            finally:
                connection.close()

    def answer_question(self, query, answer):
        user_variables = self.normalize_input.search_variables(query)
        return self.clean_response_query(answer, user_variables)


class TestQueryScanner(unittest.TestCase):
    def setUp(self):
        self.query_scanner = QueryScanner()

    def test_clean_user_question(self):
        user_question = "What are the cs courses?"
        clean_question = "What are the [major] courses?"
        self.assertEqual(self.query_scanner.clean_user_question(user_question)[0], clean_question)

        user_question = "What are the C.S courses in winter?"
        clean_question = "What are the [major] courses in [season]?"
        self.assertEqual(self.query_scanner.clean_user_question(user_question)[0], clean_question)

    def test_clean_response_user_variables(self):
        user_vars = {"major" : ("CSC", "c.s.c")}
        response = "The [major] courses are [major-courses]."
        clean_response = "The c.s.c courses are [major-courses]."
        self.assertEqual(self.query_scanner.clean_response_user_variables(response, user_vars), clean_response)

    def test_replace_variable(self):
        original_text = "The [major] courses are."
        clean_text = "The CSC courses are."
        self.assertEqual(self.query_scanner.replace_variable(original_text, "major", "CSC"), clean_text)




if __name__ == "__main__":
    unittest.main()