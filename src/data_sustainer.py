import unittest
from database_connection import connection

class DataSustainer:
    """ Scrapes data from a source and puts in in the database"""

    def __init__(self):
        pass

    def create_tables(self):
        with connection.cursor() as cursor:
            cursor.execute(open('src/sql/createTables.sql').read())

class TestDataSustainer(unittest.TestCase):

    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)

if __name__ == "__main__":
    DataSustainer().create_tables()
    unittest.main()
