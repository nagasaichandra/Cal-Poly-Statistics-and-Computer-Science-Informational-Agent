import re
import sys
from database_connection import connection


variable_regex = re.compile(r'\[([^\]]+)\]')
question_regex = re.compile('(?:[0-9]+\.\s*)?([^\n\|]+(?:\|\s*[^\n\|]+)+)')


def normalize_variable_name(var):
    """ Normalizes a variable name to reduce the chance of the same variable having multiple names """
    return var.lower().replace(' ', '-')


def get_all_variables(text):
    """ Returns all variables within a section of text (variables are denoted by brackets []) """
    return re.findall(variable_regex, text)


def get_all_variables_normalized(text):
    """ Returns all variables within a section of text (variables are denoted by brackets [])
    The variables will be normalized and duplicates removed, then sorted in order. """
    return sorted(set((normalize_variable_name(var) for var in re.findall(variable_regex, text))))


def get_all_questions(text):
    """ Finds all the questions in a section of text. A question is a line of text that starts with a number """
    return re.findall(question_regex, text)


def reformat(questions, variables):
    """ Converts a list of questions and variables into formated text. 
    The variables in the questions will be normalized and then listed out (awaiting description comments for each) """
    formated_questions = '\n'.join((re.sub(variable_regex, lambda match: normalize_variable_name(
        match.group(0)), question) for question in questions))
    formated_variables = '\n'.join(('[{}]: '.format(var) for var in variables))
    return '{}\n\n{}'.format(formated_questions, formated_variables)


def reformat_file(input_filepath, output_filepath):
    """ Converts a file containing questions into a normalized output file with questions and variables """
    file_text = open(input_filepath).read()
    questions = diversify_questions(get_all_questions(file_text))
    variables = get_all_variables_normalized(file_text)
    open(output_filepath, 'w').write(reformat(questions, variables))

synonyms_list = {
    'GE': 'general education',
    'CSSE': 'computer science and software engineering',
    'CSC': 'Computer Science',
    'SE': 'Software Engineering',
    'CGPA': 'Cumulative Grade Point Average',
    'MS': 'Masters Degree',
    'BS': 'Bachelors Degree'
}
def diversify_questions(questions):
    """ Creates alternative versions of questions by replacing terms with synonyms, then adds them to the list """
    results = []
    for question in questions:
        results.append(question)
        variables = get_all_variables(question)
        parts = question.split('|')
        adjusted = parts[0]
        answer = parts[1]
        for i, variable in enumerate(variables):
            adjusted = adjusted.replace(variable, '{%d}' % i)
        for synonym in synonyms_list:
            if synonym in adjusted:
                adjusted = re.sub(synonym, synonyms_list[synonym], adjusted)
                adjusted = adjusted.format(*variables)
                results.append(adjusted + '|' + answer)

    return results

def ingest_questions(questions):
    with connection.cursor() as cursor:
        rows = [q.split('|') for q in questions]
        for row in rows:
            cursor.execute("INSERT INTO question (question_text, response) VALUES (%s, %s);", row)
        connection.commit()

def main():
    args = sys.argv[1:]
    if not args or len(args)  < 2:
        print("usage: inputfile outputfile")
        sys.exit(1)
    if (args[0] == "--ingest"):
        file_text = open(args[1]).read()
        questions = get_all_questions(file_text)
        ingest_questions(questions)
    else:
        reformat_file(args[0], args[1])

if __name__ == '__main__':
    main()
