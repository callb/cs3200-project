#!/usr/bin/python

from database import *
from mbta_api import *


# make connection to db
conn = init_connection()


# station, line, direction, subline
line = "Orange"
stop = "Ruggles"
make_prediction(find_api_name(line, stop), line, "Southbound", "Forest Hills")
