from ..database_connection import make_connection


def links_dict():
    cs_links = [('2011 - 2013', 'https://flowcharts.calpoly.edu/downloads/mymap/11-13.52CSCBSU.pdf'),
                ('2013 - 2015', 'https://flowcharts.calpoly.edu/downloads/mymap/13-15.52CSCBSU.pdf'),
                ('2015 - 2017', 'https://flowcharts.calpoly.edu/downloads/mymap/15-17.52CSCBSU.pdf'),
                ('2017 - 2019', 'https://flowcharts.calpoly.edu/downloads/mymap/17-19.52CSCBSU.pdf'),
                ('2019 - 2020', 'https://flowcharts.calpoly.edu/downloads/mymap/19-20.52CSCBSU.pdf')
                ]

    se_links = [('2011 - 2013', 'https://flowcharts.calpoly.edu/downloads/mymap/11-13.52SEBSU.pdf'),
                ('2013 - 2015', 'https://flowcharts.calpoly.edu/downloads/mymap/13-15.52SEBSU.pdf'),
                ('2015 - 2017', 'https://flowcharts.calpoly.edu/downloads/mymap/15-17.52SEBSU.pdf'),
                ('2017 - 2019', 'https://flowcharts.calpoly.edu/downloads/mymap/17-19.52SEBSU.pdf'),
                ('2019 - 2020', 'https://flowcharts.calpoly.edu/downloads/mymap/19-20.52SEBSU.pdf')]
    flowchart_dict = dict()
    flowchart_dict['cs-major'] = cs_links
    flowchart_dict['se-major'] = se_links

    return flowchart_dict


def ingest_flowcharts(links):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for major in links:
                for i in major:
                    cursor.execute('''INSERT INTO flowchart_links VALUES ("%s", "%s", "%s");''', (major,
                                                                                                   i[0], i[1]))
            connection.commit()
    finally:
        connection.close()


def remove_content():
    '''Removes all rows from the flowchart_links table '''
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT question_text, response FROM question;")
            connection.commit()
    finally:
        connection.close()


def flowchart_links():
    remove_content()
    links = links_dict()
    ingest_flowcharts(links)


if __name__ == '__main__':
    flowchart_links()
