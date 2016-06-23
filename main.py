#!/usr/bin/python

from database import *
from mbta_api import *


# make connection to db
conn = init_connection()

# station, line, direction, subline
make_prediction("place-portr", "Red", "Southbound", "Braintree")
