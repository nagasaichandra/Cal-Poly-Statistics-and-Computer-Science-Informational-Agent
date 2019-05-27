import re
import sys

variable_regex = re.compile(r'\[([^\]]+)\]')
question_regex = re.compile('(?:[0-9]+\.\s*)?([^\n\|]+(?:\|\s*[^\n\|]+)+)')


def normalize_variable_name(var):
    """ Normalizes a variable name to reduce the chance of the same variable having multiple names """
    return var.lower().replace(' ', '-')


def get_all_variables(text):
    """ Returns all variables within a section of text (variables are denoted by brackets []) """
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
    variables = get_all_variables(file_text)
    open(output_filepath, 'w').write(reformat(questions, variables))

synonyms_list = {
    'GE': 'general education'
}
def diversify_questions(questions):
    results = []
    for question in questions:
        results.append(question)
        variables = get_all_variables(question)
        for i, variable in enumerate(variables):
            question.replace(variable, '{%d}' % i)
        for synonym in synonyms_list:
            if synonym in question:
                adjusted = re.sub(synonym, synonyms_list[synonym], question)
                adjusted.format(*variables)
                results.append(adjusted)

    return results


def main():
    args = sys.argv[1:]
    if not args or len(args)  < 2:
        print("usage: inputfile outputfile")
        sys.exit(1)
    reformat_file(args[0], args[1])

if __name__ == '__main__':
    main()
