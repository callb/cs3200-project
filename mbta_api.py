#!/usr/bin/python

import requests, json, datetime

api_key = "wX9NwuHnZU2ToO7GmGR9uw"


# makes a prediction for a station time
def make_prediction(dest, line, direc, subline):
    query = "predictionsbystop"
    url = "http://realtime.mbta.com/developer/api/v2/" + query + "?api_key="
    url += api_key + "&stop=" + dest + "&format=json"

    response = requests.get(url)
    subway_data = parse_prediction(response, line, direc, subline)
    return subway_data


#parses prediction json response
def parse_prediction(response, line, direc, subline):
    data = response.json()["mode"]
    subway_data = None
    possible_trips = []
    times = []

    # boolean if left false, return empty array
    found = 0

    # search for subway data
    for x in data:
        if x["mode_name"] == "Subway":
            subway_data = x["route"]
            found = 1

    if found:
        found = 0
    else:
        return []

    # search subway data for correct line
    for x in subway_data:
        if x["route_id"] == line:
            subway_data = x["direction"]
            found = 1

    if found:
        found = 0
    else:
        return []

    #search for correct direction
    for x in subway_data:
        if x["direction_name"] == direc:
            subway_data = x["trip"]
            found = 1

    if found:
        found = 0
    else:
        return []
    # search for correct subline, store possible trips in string
    for x in subway_data:
        if x["trip_headsign"] == subline:
            possible_trips.append(x)

    print possible_trips

    # retreive possible times for station
    for trip in possible_trips:
        time = trip["pre_dt"]
        #if "Green" in line:
        #    time = trip["pre_dt"]
        #else:
        #    time = trip["sch_arr_dt"]
        # converts epoch timestamp to 24 hour timestamp
        time_format = "%H:%M"
        time = datetime.datetime.fromtimestamp(float(time)).strftime(time_format)
        # then converts to 12 hour time
        times.append(time)

    return times

# find the api name for a specific stop
def find_api_name(line, station):
        url = "http://realtime.mbta.com/developer/api/v2/stopsbyroute?api_key="
        url+= api_key + "&route=" + line + "&format=json"
        response = requests.get(url)
        api_name = parse_api_name(response, station)
        return api_name

# parse stopsbyroute request for the station api name
def parse_api_name(response, station):
    data = response.json()["direction"]
    for x in data:
        y = x["stop"]
        for y in x:
            stops = x["stop"]
            for stop in stops:
                if stop["parent_station_name"] == station:
                    return stop["parent_station"]
    return None
