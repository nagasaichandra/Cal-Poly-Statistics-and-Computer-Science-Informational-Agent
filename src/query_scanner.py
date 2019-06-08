from src import variable_normalizer
from .database_connection import make_connection
import re
import json
from .variable_normalizer import VariableNormalizer


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
        Replaces found variables with [variable_name].
        """
        question_clean = question
        user_variables = self.normalize_input.search_variables(question)
        for key, val in user_variables.items():
            replace_string = "%s" % (val[1])
            new_string = "[%s]" % (key)
            question_clean = question_clean.replace(replace_string, new_string)
        return question_clean, user_variables

    def clean_response_user_variables(self, response_text, user_variables, query_response=False):
        """

        :param response_text: The matched response to a user's question or the raw query if query_response = True.
        :param user_variables: A dictionary of the variables found in a user's question. [variable-name] : (variable-db-name, user's-variable-name)
        :param query_response: Boolean, indicate whether we want to substitute variables in a query.
        :return:
        """
        clean_response_text = response_text
        var_names = list(user_variables.keys())
        for var_name in var_names:
            if query_response:
                var_replacement = user_variables[var_name][0]
            else:
                var_replacement = user_variables[var_name][1]
            clean_response_text = self.replace_variable(clean_response_text, var_name, var_replacement)

        return clean_response_text

    def clean_response_query(self, response_text, user_variables=None):
        clean_response_text = self.clean_response_user_variables(response_text, user_variables)
        query_variables = self.find_within_brackets(clean_response_text)
        if query_variables:
            for query_var in query_variables:
                query_sub = self.response_variables_queries[query_var]
                # First clean query.
                clean_query = self.clean_response_user_variables(query_sub, user_variables, query_response=True)
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

