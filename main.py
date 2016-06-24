#!/usr/bin/python

from database import *
from mbta_api import *


# make connection to db
conn = init_connection()


# station, line, direction, subline
line = "Orange"
stop = "Haymarket"
make_prediction(find_api_name(line, stop), line, "Northbound", "Oak Grove")
