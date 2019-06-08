import unittest
from .database_connection import make_connection


class DataSustainer:
    """ Scrapes data from a source and puts in in the database"""

    def __init__(self):
        pass

    @staticmethod
    def create_tables():
        with make_connection() as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(open('src/sql/createTables.sql').read())
                    connection.commit()
            finally:
                connection.close()

    @staticmethod
    def delete_all_tables():
        with make_connection() as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT
                            table_name
                        FROM
                            information_schema.tables
                        WHERE
                            table_schema = 'project3';""")
                    table_names = [row['TABLE_NAME'] for row in cursor.fetchall()]
                    deletors = ['DROP TABLE IF EXISTS {};'.format(table_name) for table_name in table_names]
                    query = """SET FOREIGN_KEY_CHECKS = 0;
                    {}
                    SET FOREIGN_KEY_CHECKS = 1;""".format('\n'.join(deletors))
                    cursor.execute(query)
                    connection.commit()
            finally:
                connection.close()



class TestDataSustainer(unittest.TestCase):

    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)


if __name__ == "__main__":
    DataSustainer().create_tables()
    unittest.main()
