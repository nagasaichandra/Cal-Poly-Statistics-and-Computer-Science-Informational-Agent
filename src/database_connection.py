import pymysql.cursors
import json
import sys

# Connect to the database
with open('db_config.json') as json_file:
    if not json:
        print('Could not read database configuration. Please create a db_config.json file with the login info')
        sys.exit(1)
    config = json.loads(json_file.read())


def make_connection():
    return pymysql.connect(host=config['host'],
                           user=config['user'],
                           ssl={'ca': './cacert.pem'},
                           password=config['password'],
                           db=config['db'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
