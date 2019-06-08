import re

"""Use this script to normalize the variables a user provides in order to match them with the database values.

"""

def normalize_major(major_input):
    """

    :param major_input: The user variable that is matched as 'major'.
    :return: The formatted name of the major in order for it the match the database's major categories.
    """
    if re.match(r'C\.?S\.?C\.?|CS|Computer Science|SE|C\.?S\.?', major_input, flags=re.I):
        return "CSC"
    else:
        print("Could not find %s in major."%(major_input))

def normalize_season(season_input):
    """

    :param season_input: The user variable that is matched as 'season'.
    :return: The formatted season name in order to match with the database's season categories.
    """
    season_dictionary = {"fall": "F", "winter": "W", "spring": "Sp", "summer": "Su"}
    lower_case_input = season_input.lower()
    return season_dictionary[lower_case_input]

def normalize_variables(user_variable, variable_name):
    """

    :param user_variable: The user's matched input to a variable.
    :param variable_name: The name of the variable which user variable matched to.
    :return:
    """
    if variable_name == "major":
        return normalize_major(user_variable)
    elif variable_name == "season":
        return normalize_season(user_variable)

