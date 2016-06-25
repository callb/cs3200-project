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

    print "Populating database..."

    # lines
    lines = ["Red", "Orange", "Blue", "Green-B", "Green-C", "Green-D", "Green-E"]

    #sublines
    red_sublines = ["Ashmont", "Braintree", "Alewife"]
    blue_sublines = ["Wonderland", "Bowdoin"]
    orange_sublines = ["Oak Grove", "Forest Hills"]
    green_b_sublines = ["Park Street", "Boston College"]
    green_c_sublines = ["North Station", "Cleveland Circle"]
    green_d_sublines = ["Government Center", "Riverside"]
    green_e_sublines = ["Lechmere", "Heath Street"]

    # dictionary for corresponding direction of sublines
    directions_dict = {"Wonderland": "Eastbound", "Bowdoin": "Westbound",
    "Ashmont": "Southbound", "Braintree": "Southbound", "Alewife": "Northbound",
    "Forest Hills": "Southbound", "Oak Grove": "Northbound",
    "Park Street": "Eastbound", "North Station": "Eastbound",
    "Lechmere": "Eastbound", "Government Center": "Eastbound",
    "Boston College": "Westbound", "Cleveland Circle": "Westbound",
    "Riverside": "Westbound", "Heath Street": "Westbound"}

    # stops for each line
    red_line_stops = ["Alewife", "Davis", "Porter", "Harvard",
     "Central", "Kendall/MIT", "Charles/MGH", "Park Street", "Downtown Crossing",
     "South Station", "Broadway", "Andrew", "JFK/Umass"]
    braintree_alewife_stops = ["North Quincy", "Wollaston", "Quincy Center",
    "Quincy Adams", "Braintree"]
    ashmont_alewife_stops = ["Savin Hill", "Fields Corner", "Shawmut",
     "Ashmont"]
    blue_line_stops = ["Bowdoin", "Government Center", "State Street", "Aquarium",
    "Maverick", "Airport", "Wood Island", "Orient Heights", "Suffolk Downs",
    "Beachmont", "Revere Beach", "Wonderland"]
    orange_line_stops = ["Oak Grove", "Malden Center", "Wellington",
     "Assembly", "Sullivan Square", "Community College", "North Station",
     "Haymarket", "State Street", "Downtown Crossing", "Chinatown",
     "Tufts Medical Center", "Back Bay", "Massachusetts Ave.", "Ruggles",
     "Roxbury Crossing", "Jackson Square", "Stony Brook", "Green Street",
      "Forest Hills"]
    green_b_line_stops = ["Park Street", "Boylston", "Arlington",
    "Copley", "Hynes Convention Center", "Kenmore", "Blandford Street",
    "Boston Univ. East", "Boston Univ. Central", "Boston Univ. West",
    "Saint Paul Street", "Pleasant Street", "Babcock Street", "Packards Corner",
    "Harvard Ave.", "Griggs Street", "Allston Street", "Warren Street",
    "Washington Street", "Sutherland Road", "Chiswick Road",
    "Chestnut Hill Ave.", "South Street", "Boston College"]
    green_c_line_stops = ["North Station", "Haymarket", "Government Center",
    "Park Street", "Boylston", "Arlington", "Copley", "Hynes Convention Center",
    "Kenmore", "Saint Mary Street", "Hawes Street", "Kent Street",
    "Saint Paul Street", "Coolidge Corner", "Summit Ave.", "Brandon Hall",
    "Fairbanks Street", "Washington Square", "Tappan Street", "Dean Road",
    "Englewood Ave.", "Cleveland Circle"]
    green_d_line_stops = ["Government Center", "Park Street", "Boylston",
    "Arlington", "Copley", "Hynes Convention Center", "Kenmore", "Fenway",
    "Longwood", "Brookline Village", "Brookline Hills", "Beaconsfield",
    "Reservoir", "Chestnut Hill", "Newton Centre", "Newton Highlands", "Eliot",
    "Waban", "Woodland", "Riverside"]
    green_e_line_stops = ["Lechmere", "Science Park", "North Station",
    "Haymarket", "Government Center", "Park Street", "Boylston", "Arlington",
    "Copley", "Prudential", "Symphony", "Northeastern University",
    "Museum of Fine Arts", "Longwood Medical Area", "Brigham Circle",
    "Fenwood Road", "Mission Park", "Riverway", "Back of the Hill", "Heath Street"]



    # first delete all stale data from before
    delete_stmt = "DELETE FROM Station"
    conn.execute(delete_stmt)

    for line in lines:
        sublines = None
        stops = None
        if line == "Red":
            sublines = red_sublines
        if line == "Blue":
            sublines = blue_sublines
        if line == "Orange":
            sublines = orange_sublines
        if line == "Green-B":
            sublines = green_b_sublines
        if line == "Green-C":
            sublines = green_c_sublines
        if line == "Green-D":
            sublines = green_d_sublines
        if line == "Green-E":
            sublines = green_e_sublines

        # inserts records for Lines table
        for subline in sublines:
            direction = directions_dict[subline]

            # use the correct list of stops for that subline
            if subline == "Alewife":
                stops = red_line_stops
            if subline == "Braintree":
                stops = red_line_stops
                stops = stops + braintree_alewife_stops
            if subline == "Ashmont":
                stops = red_line_stops
                stops = stops + ashmont_alewife_stops
            if subline == "Bowdoin" or subline == "Wonderland":
                stops = blue_line_stops
            if subline == "Forest Hills" or subline == "Oak Grove":
                stops = orange_line_stops
            if subline == "Park Street" or subline == "Boston College":
                stops = green_b_line_stops
            if subline == "North Station" or subline == "Cleveland Circle":
                stops = green_c_line_stops
            if subline == "Government Center" or subline == "Riverside":
                stops = green_d_line_stops
            if subline == "Lechmere" or subline == "Heath":
                stops = green_e_line_stops

            for stop in stops:
                if not stop == subline:
                    api_name = find_api_name(line, stop)
                    times = make_prediction(api_name, line, direction, subline)
                    time_1 = 'NULL'
                    time_2 = 'NULL'
                    time_3 = 'NULL'
                    if times:
                        time_1 = times[0]
                        if len(times) >= 2:
                            time_2 = times[1]
                            if len(times) >= 3:
                                time_3 = times[2]

                    print stop
                    print line
                    print direction
                    print subline
                    print times

                    insert_stmt = "INSERT INTO Station (color, subline,"
                    insert_stmt += "direction, station_name, arrival_time_1, "
                    insert_stmt += "arrival_time_2,  arrival_time_3) VALUES ("
                    insert_stmt += "'" + line + "', '" + subline + "', '"
                    insert_stmt += direction + "', '" + stop + "', '" + time_1
                    insert_stmt +=  "', '" + time_2 + "', '" + time_3 + "');"
                    conn.execute(insert_stmt)
    print "Database updates complete"


def query_db(conn):
    query = "SELECT * FROM {}".format("Line")
    for s in conn.execute(query):
        print s[0]

conn = init_connection()
populate_data(conn)
#query_db(conn)
