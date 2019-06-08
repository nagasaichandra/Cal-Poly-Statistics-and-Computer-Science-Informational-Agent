from src import variable_normalizer
from .database_connection import connection
import re
import json
from .variable_normalizer import normalize_variables


class QueryScanner:
    def __init__(self):
        self.user_variables_regex = self.read_json("user_variables.json")
        self.response_variables_queries = self.read_json("response_variables.json")
        self.user_query_variables_regex = self.read_json("user_query_variables.json")

    def read_json(self, filename):
        """ Reads the json files in the top directory and returns them as dictionary objects. """
        with open(filename, "r") as user_variables:
            variable_re_dict = json.load(user_variables)
            return variable_re_dict

    def search_user_variable(self, variable_name, question):
        """
        Searches for a variable in a user's question.
        Requires the name of a variable and the question the user gives.
        If the variable name is not present in the question, returns False.
        """
        matched_term = re.search(r'%s' % self.user_variables_regex[variable_name], question, flags=re.I)
        if matched_term:
            if len(matched_term.group()) > 0:
                return matched_term.group(1)
        return False

    def find_variables(self, question):
        """

        :param question: A string of the user's input question.
        :return:
        """
        vars_dictionary = {var: self.search_user_variable(var, question) for var in self.user_variables_regex.keys() if
                           self.search_user_variable(var, question)}
        return vars_dictionary

    def clean_user_question(self, question):
        """
        Replaces found variables with [variable_name].
        """
        question_clean = question
        user_variables = self.find_variables(question)
        for key, val in user_variables.items():
            replace_string = "%s" % (val)
            new_string = "[%s]" % (key)
            question_clean = question_clean.replace(replace_string, new_string)
        return question_clean, user_variables

    def clean_response_user_variables(self, response_text, user_variables=False, query_response = False):
        """

        :param response_text: The matched response to a user's question.
        :param user_variables: A dictionary of the variables found in a user's question. [variable-name] : user-variable.
        :return:
        """
        clean_response_text = response_text
        if user_variables:
            var_names = list(user_variables.keys())
            for var_name in var_names:
                if query_response:
                    var_replacement = normalize_variables(user_variables[var_name], var_name)
                else:
                    var_replacement = user_variables[var_name]
                print("Variable replacement: %s"%var_replacement)
                clean_response_text = self.replace_variable(clean_response_text, var_name, var_replacement)
        return clean_response_text

    def clean_response_query(self, response_text, user_variables=None):
        clean_response_text = self.clean_response_user_variables(response_text, user_variables)
        query_variables = self.find_within_brackets(clean_response_text)
        if query_variables:
            for query_var in query_variables:
                query_sub = self.response_variables_queries[query_var]
                # First clean query.
                clean_query = self.clean_response_user_variables(query_sub, user_variables, query_response = True)
                query_response_list = self.execute_query(clean_query)

                if query_response_list:
                    query_response = ', '.join(query_response_list)
                else:
                    query_response = "(could not find %s)"%(query_var)

                clean_response_text = self.replace_variable(clean_response_text, query_var, query_response)
        print(clean_response_text)

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
        with connection.cursor() as cursor:
            cursor.execute('''%s''' % query)
            response_list = cursor.fetchall()
            connection.commit()
        tuple_response = [list(response.values())[0] for response in response_list]
        if len(tuple_response) > 0:
            return tuple_response
        else:
            return False

    def answer_question(self, query, answer):
        user_variables = self.find_variables(query)
        return self.clean_response_query(answer, user_variables)


query_scanner = QueryScanner()
query_scanner.answer_question("What C.S. courses are there in winter?", "The [major] courses in [season] are [season-course-names].")