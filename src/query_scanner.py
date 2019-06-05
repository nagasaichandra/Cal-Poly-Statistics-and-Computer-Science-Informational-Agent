from .database_connection import connection
import re
import json

# "What are the [major] courses?|The [major] courses are [major-courses]."
# variable_re_dict = {'class-level': '(senior|junior|sophmore|freshman)',
#                     #'concentration': 'REMOVE THIS VARIABLE.',
#                     #'course': '#TODO',
#                     'course-units': '([0-9]+) unit[s]*',
#                     'division-level': '(upper|lower)(-| )division',
#                     #'elective-name': '#TODO',
#                     'elective-type': '(support|free|restricted) elective',
#                     # 'ge-area': 'z',
#                     'gpa': 'gpa of ([0-4][.]?[0-9]+)',
#                     # 'gpa-number': 'z',
#                     # 'honor-name': 'z',
#                     'major': '(CSSE|CompSci|Computer Science|SE|CSC|CS)',
#                     # 'minor': 'z',
#                     # 'num-units': 'z',
#                     # 'season': '(fall|winter|spring|summer)',
#                     # 'subject': 'z',
#                     'year-range': 'z'}
#
# variable_query_dict = {'major-courses' : '''SELECT course_name FROM course WHERE course_area like "%[major]";'''}
with open("user_variables.json", "r") as user_variables:
    variable_re_dict = json.load(user_variables)

with open("response_variables.json", "r") as response_variables:
    variable_query_dict = json.load(response_variables)


def apply_re(variable_name, question):
    matched_term = re.search(r'%s' % variable_re_dict[variable_name], question, flags=re.I)
    if matched_term:
        return matched_term.group(0)


def find_variables(question):
    vars_dictionary = {var: apply_re(var, question) for var in variable_re_dict.keys() if apply_re(var, question)}
    return vars_dictionary


# TODO: Map Computer Science to CS.
# TODO: Create clean text class.
# question = "What are the CSC courses?"
# answer = "The [major] courses are [major-courses]."

def clean_response_user_variables(response_text, user_variables=None):
    clean_response_text = response_text
    if user_variables:
        var_names = list(user_variables.keys())
        for var_name in var_names:
            var_subs = user_variables[var_name]
            clean_response_text = replace_variable(clean_response_text, var_name, var_subs)
    return clean_response_text


def clean_response_query(response_text, user_variables=None):
    clean_response_text = clean_response_user_variables(response_text, user_variables)
    query_variables = re.findall(r'\[(.*?)\]', clean_response_text)
    if query_variables:
        for query_var in query_variables:
            query_sub = variable_query_dict[query_var]
            # First clean query.
            clean_query = clean_response_user_variables(query_sub, user_variables)
            query_response_list = execute_query(clean_query)
            query_response = ', '.join(query_response_list)

            clean_response_text = replace_variable(clean_response_text, query_var, query_response)

    return clean_response_text


def replace_variable(text, variable_name, substitution):
    variable_re_string = r'\[{}\]'.format(variable_name).replace("'", "")
    clean_text = re.sub(r'' + variable_re_string, substitution, text)
    return clean_text


def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute('''%s''' % query)
        response_list = cursor.fetchall()
        connection.commit()
    tuple_response = [list(response.values())[0] for response in response_list]
    return tuple_response


def answer_question(query, answer):
    user_variables = find_variables(query)
    return clean_response_query(answer, user_variables)


question_asked = "What are the CSC courses?"
print("Question asked: %s" % (question_asked))
print()
print(answer_question(question_asked, "The [major] courses are [major-courses]."))
