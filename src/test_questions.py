from src.query_scanner import QueryScanner
from src.database_connection import make_connection
from src.questions import get_questions
from src.relevance_detector import RelevanceDetector
from main import answer_query
import sys
import traceback

qs = QueryScanner()
rd = RelevanceDetector()
connection = make_connection()

values = {
    'course-units': 2,
    'major': 'CSC',
    'season': 'Sp',
    'elective-type': 'Life Science Support Elective',
    'year-range': '2019 - 2020',
    'minor': 'Data Science minor',
    'class-level': 'junior',
    'division-level': 'upper',
    'ge-area': 'A',
    'num-units': 4
}


def sub_in_variables(question):
    question = question.replace('[', '{')
    question = question.replace(']', '}')
    return question.format(**values)


def test_all_question(questions, verbose=False):
    try:
        with connection.cursor() as cursor:
            for question, answer in questions:

                try:
                    subed_question = sub_in_variables(question)
                    matched_question, matched_answer, score, vars = rd.most_relevant_query(subed_question)
                    response = answer_query(sub_in_variables(question), False)
                    if matched_question != question:
                        print(
                            "------------------------------------------------------------------------------------",
                            file=sys.stderr)
                        print("Question '{}'".format(subed_question), file=sys.stderr)
                        print("Returned matched wrong question '{}' with score {} (should have matched '{}')".format(matched_question, score, question), file=sys.stderr)
                    elif 'could not find' in response:
                        print(
                            "------------------------------------------------------------------------------------",
                            file=sys.stderr)
                        print("Question '{}'".format(subed_question), file=sys.stderr)
                        print("Returned no results", file=sys.stderr)
                    elif verbose:
                        print(
                            "------------------------------------------------------------------------------------")
                        print("Question '{}'".format(subed_question))
                        print("Returned results", response)
                except Exception as exception:
                    print("------------------------------------------------------------------------------------",
                          file=sys.stderr)
                    print("Query '{}'".format(subed_question), file=sys.stderr)
                    print("Raised an exception", exception, '&', file=sys.stderr)
                    traceback.print_exc()
    finally:
        connection.close()


test_all_question(get_questions(), False)
