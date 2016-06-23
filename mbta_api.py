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
    print json.dumps(subway_data, indent=4)


#parses prediction json response
def parse_prediction(response, line, direc, subline):
    data = response.json()["mode"]
    print data
    subway_data = None
    possible_trips = []
    times = []
    # search for subway data
    for x in data:
        if x["mode_name"] == "Subway":
            subway_data = x["route"]

    # search subway data for correct line
    print subway_data
    for x in subway_data:
        if x["route_id"] == line:
            subway_data = x["direction"]

    #search for correct direction
    for x in subway_data:
        if x["direction_name"] == direc:
            subway_data = x["trip"]

    # search for correct subline, store possible trips in string
    for x in subway_data:
        if x["trip_headsign"] == subline:
            possible_trips.append(x)

    # retreive possible times for station
    for trips in possible_trips:
        time = trips["sch_arr_dt"]
        # converts epoch timestamp to 24 hour timestamp
        time = datetime.datetime.fromtimestamp(float(time)).strftime("%c")
        time = time.split(" ")[3]
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
