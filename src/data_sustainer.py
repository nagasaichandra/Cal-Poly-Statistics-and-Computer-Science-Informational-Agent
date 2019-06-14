import unittest
from .database_connection import make_connection, config
from src.parse_questions import ingest_file_questions
from src.scrapers.scrape_all import scrape_all


class DataSustainer:
    """ Scrapes data from a source and puts in in the database"""

    def __init__(self):
        pass

    @staticmethod
    def initialize_database():
        """

        :param filename: The name of the .sql file under src/sql which creates the table. Default: createTables.
        :return:
        """
        DataSustainer.delete_all_tables()

        DataSustainer.create_tables('createTableBlended.sql')
        DataSustainer.create_tables('createTableCatalogue.sql')
        DataSustainer.create_tables('createTableChangeMajor.sql')
        DataSustainer.create_tables('createTableContact.sql')
        DataSustainer.create_tables('createTableDegrees.sql')
        DataSustainer.create_tables('createTableFlowchartLinks.sql')
        DataSustainer.create_tables('createTableGERequirements.sql')
        DataSustainer.create_tables('createTableMasters.sql')
        DataSustainer.create_tables('createTableMinor.sql')
        DataSustainer.create_tables('createTableObjectives.sql')
        DataSustainer.create_tables('createTableRequirements.sql')
        DataSustainer.create_tables('createTablesHonors.sql')
        DataSustainer.create_tables('createTablesICMA.sql')
        DataSustainer.create_tables('createTablesLevels.sql')
        DataSustainer.create_tables('createTableTransfer.sql')
        DataSustainer.create_tables('createTableProbation.sql')
        DataSustainer.create_tables('createTables.sql')


        ingest_file_questions('questions.txt')
        scrape_all()


    @staticmethod
    def create_tables(filename='createTables.sql'):
        """

        :param filename: The name of the .sql file under src/sql which creates the table. Default: createTables.
        :return:
        """
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(open('src/sql/%s' % filename).read())
                connection.commit()
        finally:
            connection.close()

    @staticmethod
    def delete_all_tables():
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
                   table_name
               FROM
                   information_schema.tables
               WHERE
                   table_schema = '{}';""".format(config['db']))
                table_names = [row['table_name'] for row in cursor.fetchall()]
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
