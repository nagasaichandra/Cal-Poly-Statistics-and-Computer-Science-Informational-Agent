import re

"""
Use this script to normalize the variables a user provides in order to match them with the database values.
"""

def normalize_major(major_input):
    if re.match(r'C\.?S\.?C\.?|CS|Computer Science|SE|C\.?S\.?', major_input, flags=re.I):
        return "CSC"
    else:
        print("Could not find %s in major."%(major_input))

def normalize_season(season_input):
    season_dictionary = {"fall": "F", "winter": "W", "spring": "Sp", "summer": "Su"}
    lower_case_input = season_input.lower()
    return season_dictionary[lower_case_input]

def normalize_variables(user_variable, variable_name):
    if variable_name == "major":
        return normalize_major(user_variable)
    elif variable_name == "season":
        return normalize_season(user_variable)

