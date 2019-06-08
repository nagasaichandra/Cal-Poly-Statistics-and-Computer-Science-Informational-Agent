from .database_connection import make_connection


def get_questions():
    """ Gets the questions and answers for each question in the questions table """
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT question_text, response FROM question;")
            return [(row['question_text'], row['response']) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_variable_values(variable):
    """ Returns the possible values of a variable in the variables table"""
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name, field_name FROM variable WHERE name = {};".format(variable))
            result = cursor.fetchone()
            cursor.execute("SELECT {table_name} FROM {field_name};".format(**result))
            return [row[result['field_name']] for row in cursor.fetchall()]
    finally:
        connection.close()
