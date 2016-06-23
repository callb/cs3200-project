#!/usr/bin/python

from sqlalchemy import create_engine
from mbta_api import *

# create the connection to the databse
def init_connection():

    # Connection settings
    settings = {
        'userName': "root",           # The name of the MySQL account to use (or empty for anonymous)
        'password': "",               # The password for the MySQL account (or empty for anonymous)
        'serverName': "localhost",    # The name of the computer running MySQL
        'portNumber': 3306,           # The port of the MySQL server (default is 3306)
        'dbName': "MBTA_Subway",      # The name of the database we are testing with (this default is installed with MySQL)
    }

    conn = create_engine('mysql://{0[userName]}:{0[password]}@{0[serverName]}:{0[portNumber]}/{0[dbName]}'.format(settings))
    print 'Connected to database'
    return conn

# populates the database with the subway information
def populate_data(conn):
    lines = ["Red", "Orange", "Blue"] #, "Green-B", "Green-C", "Green-D", "Green-E"]
    red_sublines = ["Ashmont", "Braintree", "Alewife"]
    blue_sublines = ["Wonderland", "Bowdoin"]
    orange_sublines = ["Oak Grove", "Forest Hills"]
    green_b_sublines = ["Lechmere", "Boston College"]
    green_c_sublines = ["Lechmere", "Cleveland Circle"]
    green_d_sublines = ["Lechmere", "Riverside"]
    green_e_sublines = ["Lechmere", "Heath Street"]
    directions_dict = {"Wonderland": "Eastbound", "Bowdoin": "Westbound",
    "Ashmont": "Southbound", "Braintree": "Southbound", "Alewife": "Northbound",
    "Forest Hills": "Southbound", "Oak Grove": "Northbound"}

    # first delete all stale data from before
    delete_stmt = "DELETE FROM Line"
    conn.execute(delete_stmt)

    for line in lines:
        sublines = None
        if line == "Red":
            sublines = red_sublines
        if line == "Blue":
            sublines = blue_sublines
        if line == "Orange":
            sublines = orange_sublines

        # Green lines

        for sl in sublines:
            direction = directions_dict[sl]
            insert_stmt = "INSERT INTO Line (color, subline, direction) VALUES ("
            insert_stmt += "'" + line + "', '" + sl + "', '" + direction +"');"
            conn.execute(insert_stmt)








def query_db(conn):
    query = "SELECT * FROM {}".format("Line")
    for s in conn.execute(query):
        print s[0]

conn = init_connection()
populate_data(conn)
query_db(conn)
