#!/usr/bin/python

from sqlalchemy import create_engine

def init_connection():

    # Connection settings
    settings = {
        'userName': "root",           # The name of the MySQL account to use (or empty for anonymous)
        'password': "",           # The password for the MySQL account (or empty for anonymous)
        'serverName': "localhost",    # The name of the computer running MySQL
        'portNumber': 3306,           # The port of the MySQL server (default is 3306)
        'dbName': "MBTA_Subway",      # The name of the database we are testing with (this default is installed with MySQL)
    }

    conn = create_engine('mysql://{0[userName]}:{0[password]}@{0[serverName]}:{0[portNumber]}/{0[dbName]}'.format(settings))
    print 'Connected to database'
    return conn


def query_db(conn):
    query = "SELECT subline FROM {}".format("Line")
    for s in conn.execute(query):
        print s[0]
