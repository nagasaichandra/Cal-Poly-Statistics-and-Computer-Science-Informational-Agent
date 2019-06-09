from src.query_scanner import QueryScanner
from src.database_connection import make_connection
import sys

qs = QueryScanner()
response_variables_queries = qs.response_variables_queries

connection = make_connection()

values = {
    'course-units': 2,
    'major': 'CSC',
    'season': 'Sp'
}


def test_all_queries(verbose=False):
    try:
        with connection.cursor() as cursor:
            for variable in response_variables_queries:
                query = response_variables_queries[variable]

                if query != "":
                    query = query.replace('[', '{')
                    query = query.replace(']', '}')
                    query = query.format(**values)
                    try:
                        cursor.execute(query)
                        results = cursor.fetchall()
                        if len(results) == 0:
                            print("------------------------------------------------------------------------------------",
                                  file=sys.stderr)
                            print("Query '{}'".format(query), file=sys.stderr)
                            print("Returned no results", file=sys.stderr)
                        elif verbose:
                            print("------------------------------------------------------------------------------------")
                            print("Query '{}'".format(query))
                            print("Returned results", results)
                    except:
                        print("------------------------------------------------------------------------------------",
                              file=sys.stderr)
                        print("Query '{}'".format(query), file=sys.stderr)
                        print("Raised an exception", file=sys.stderr)
    finally:
        connection.close()
