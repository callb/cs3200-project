import json
from Tkinter import *
import mysql.connector
from mysql.connector import errorcode
import random
from mbta_api import make_prediction, find_api_name

line_options = [
    "Blue",
    "Green-B",
    "Green-C",
    "Green-D",
    "Green-E",
    "Orange",
    "Red",
]

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

blue_line_stations = [
    "Wonderland",
    "Revere Beach",
    "Beachmont",
    "Suffolk Downs",
    "Orient Heights",
    "Wood Island",
    "Airport",
    "Maverick",
    "Aquarium",
    "Government Center",
    "Bowdoin"
]

green_line_b_stations = [
    "Park Street",
    "Boylston",
    "Arlington",
    "Copley",
    "Hynes Convention Center",
    "Kenmore",
    "Blandford Street",
    "Boston Univ. East",
    "Boston Univ. Center",
    "Boston Univ. West",
    "St. Paul Street",
    "Pleasant Street",
    "Babcock Street",
    "Packards Corner",
    "Harvard Ave.",
    "Griggs Street/Long Ave.",
    "Allston Street",
    "Warren Street",
    "Washington Street",
    "Sutherland Road",
    "Chiswick Road",
    "Chestnut Hill Ave.",
    "South Street",
    "Boston College"
]
green_line_c_stations = [
    "North Station",
    "Haymarket",
    "Government Center",
    "Park Street",
    "Boylston",
    "Arlington",
    "Copley",
    "Hynes Convention Center",
    "Kenmore",
    "St. Marys Street",
    "Hawes Street",
    "Kent Street",
    "St. Paul Street",
    "Coolidge Corner",
    "Summit Ave.",
    "Brandon Hall",
    "Fairbanks",
    "Washington Square",
    "Tappan Street",
    "Dean Road",
    "Englewood Ave.",
    "Cleveland Circle"
]
green_line_d_stations = [
    "Government Center",
    "Park Street",
    "Boylston",
    "Arlington",
    "Copley",
    "Hynes Convention Center",
    "Kenmore",
    "Fenway",
    "Longwood",
    "Brookline Village",
    "Brookline Hills",
    "Beaconsfield",
    "Reservoir",
    "Chestnut Hill",
    "Newton Centre",
    "Newton Highlands",
    "Eliot",
    "Waban",
    "Woodland",
    "Riverside"
]
green_line_e_stations = [
    "Lechmere",
    "Science Park",
    "North Station",
    "Haymarket",
    "Government Center",
    "Park Street",
    "Boylston",
    "Arlington",
    "Copley",
    "Prudential",
    "Symphony",
    "Northeastern University",
    "Museum of Fine Arts",
    "Longwood Medical Area",
    "Brigham Circle",
    "Fenwood Road",
    "Mission Park",
    "Riverway",
    "Back of the Hill",
    "Heath Street"
]
orange_line_stations = [
    "Oak Grove",
    "Malden Center",
    "Wellington",
    "Assembly",
    "Sullivan Square",
    "Community College",
    "North Station",
    "Haymarket",
    "State",
    "Downtown Crossing",
    "Chinatown",
    "Tufts Medical Center",
    "Back Bay",
    "Massachusetts Ave.",
    "Ruggles Station",
    "Roxbury Crossing",
    "Jackson Square",
    "Stony Brook",
    "Green Street",
    "Forest Hills"]

red_line_stations = [
    "Alewife",
    "Davis",
    "Porter Square",
    "Harvard Square",
    "Central Square",
    "Kendall/MIT",
    "Charles/MGH",
    "Park Street",
    "Downtown Crossing",
    "South Station",
    "Broadway",
    "Andrew",
    "JFK/UMass",
]

braintree_alewife_stations = [
    "North Quincy",
    "Wollaston",
    "Quincy Center",
    "Quincy Adams",
    "Braintree"
]

ashmont_alewife_stations = [
    "Savin Hill",
    "Fields Corner",
    "Shawmut",
    "Ashmont"
]

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.depart_station_menu = None
        self.arrive_station_menu = None
        self.start_line = StringVar(self)
        self.end_line = StringVar(self)
        self.start_subline = StringVar(self)
        self.end_subline = StringVar(self)
        self.start_station = StringVar(self)
        self.end_station = StringVar(self)
        self.output_box = Text(self)
        self.initUI()
        self.cnx = self.connectToDB()

    def connectToDB(self):
        try:
            cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='MBTA_Subway')
            print("Connection opened.")
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied: bad username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Connection failed: Database does not exist.")
            else:
                print(err)
    def disconnectFromDB(self):
        self.cnx.close()
        print("Connection closed.")

    def initUI(self):

        self.parent.title("MBTA Subway Route Planner")
        self.pack(fill=BOTH, expand=True)

        # Buttons for CRUD
        new_button = Button(self, text="New route", command=self.newRouteCommand)
        new_button.grid(row=0, column=0)
        save_button = Button(self, text="Save route", command=self.saveRouteCommand)
        save_button.grid(row=0, column=1)
        load_button = Button(self, text="Load existing route",command=self.loadRouteCommand)
        load_button.grid(row=0, column=2)
        delete_button = Button(self, text="Delete current route", command=self.deleteRouteCommand)
        delete_button.grid(row=0, column=3)

        # Column label to indication Station selection
        line_label = Label(self, text="Select an MBTA Subway Line", fg="blue")
        line_label.grid(row=1, column=1, pady=10)

        # Column label to indicate Station selection
        station_label = Label(self, text="Select a Station", fg="blue")
        station_label.grid(row=1, column=2, pady=10)

        # Row label
        depart_row_message = Label(self, text="Depart from: ")
        depart_row_message.grid(row=2, column=0)

        # MBTA Line drop-down menu for starting station
        depart_line_menu = OptionMenu(self, self.start_line, *line_options, command=self.onSelectDepartColor)
        depart_line_menu.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        depart_line_menu.config(width=8)

        # Departure time entry box
        depart_time = StringVar(value="(optional) Time of departure")
        depart_entry = Entry(self, textvariable=depart_time)
        depart_entry.grid(row=2, column=3)
        depart_entry.config(width=20)

        # Row label
        arrive_row_message = Label(self, text="Arrive at: ")
        arrive_row_message.grid(row=3, column=0)

        # MBTA Line drop-down menu for ending station
        arrive_line_menu = OptionMenu(self, self.end_line, *line_options, command=self.onSelectArriveColor)
        arrive_line_menu.grid(row=3, column=1, padx=5, pady=10, sticky="w")
        arrive_line_menu.config(width=8)

        # Arrival time entry box
        arrive_time = StringVar(value="(optional) Time of arrival")
        arrive_entry = Entry(self, textvariable=arrive_time)
        arrive_entry.grid(row=3, column=3)
        arrive_entry.config(width=20)

        # Output box
        self.output_box.grid(row=5, column=1, columnspan=3)
        self.output_box.config(state=DISABLED, height=10)

        # Button to retrieve times for current route
        update_button = Button(self, text="Calculate route", command=self.updateRouteCommand)
        update_button.grid(row=4, column=1, columnspan=4, padx=5, pady=10)

        # Scrollbar for Output box
        scrollbar = Scrollbar(self, command=self.output_box.yview)
        scrollbar.grid(row=5, column=4, sticky='nsew')
        self.output_box['yscrollcommand'] = scrollbar.set

        #Menu
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar)
        file_menu.add_command(label="Exit", command=self.onExit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def newRouteCommand(self):
        if self.arrive_station_menu is not None:
            self.arrive_station_menu.destroy()
        if self.depart_station_menu is not None:
            self.depart_station_menu.destroy()
        self.output_box.config(state=NORMAL)
        self.output_box.delete('1.0', END)
        self.output_box.insert(END, "New route request\n")
        self.output_box.config(state=DISABLED)

    def saveRouteCommand(self):
        user = self.cnx.user
        firstcolor = self.start_line
        firstsubline = self.start_subline
        firststation = self.start_station
        secondcolor = self.end_line
        secondsubline = self.end_subline
        secondstation = self.end_station

        self.output_box.config(state=NORMAL)
        stmt = "INSERT INTO Track (user, first_color, first_subline, first_station, " \
                "dest_color, dest_subline, dest_station) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                % (user, firstcolor.get(), firstsubline, firststation.get(), secondcolor.get(), secondsubline, secondstation.get())
        print stmt
        self.cnx.cmd_query(query=stmt)
        self.output_box.insert(END, "Saved track with given depart and arrive stations.")
        self.output_box.config(state=DISABLED)

    def loadRouteCommand(self):
        self.output_box.config(state=NORMAL)
        self.output_box.insert(END, "Load existing routes from database\n")
        self.output_box.config(state=DISABLED)

    def updateRouteCommand(self):
        depart_sublines = None
        arrive_sublines = None

        if self.start_line.get() == "Blue":
            depart_sublines = random.choice(blue_sublines)
        elif self.start_line.get() == "Red":
            depart_sublines = random.choice(red_sublines)
        elif self.start_line.get() == "Green-B":
            depart_sublines = random.choice(green_b_sublines)
        elif self.start_line.get() == "Green-C":
            depart_sublines = random.choice(green_c_sublines)
        elif self.start_line.get() == "Green-D":
            depart_sublines = random.choice(green_d_sublines)
        elif self.start_line.get() == "Green-E":
            depart_sublines = random.choice(green_e_sublines)
        else:
            depart_sublines = random.choice(orange_sublines)

        if self.end_line.get() == "Blue":
            arrive_sublines = random.choice(blue_sublines)
        elif self.end_line.get() == "Red":
            arrive_sublines = random.choice(red_sublines)
        elif self.end_line.get() == "Green-B":
            arrive_sublines = random.choice(green_b_sublines)
        elif self.end_line.get() == "Green-C":
            arrive_sublines = random.choice(green_c_sublines)
        elif self.end_line.get() == "Green-D":
            arrive_sublines = random.choice(green_d_sublines)
        elif self.end_line.get() == "Green-E":
            arrive_sublines = random.choice(green_e_sublines)
        else:
            arrive_sublines = random.choice(orange_sublines)

        if self.depart_station_menu is not None:
            line = self.start_line.get()
            station = self.start_station.get()
            self.output_box.config(state=NORMAL)
            self.output_box.insert(END, "Finding first station...\n")
            depart_predict = make_prediction(find_api_name(line, station), line,
                                        directions_dict.get(depart_sublines), depart_sublines)
            self.output_box.insert(END, "Next train at " + station + ": " + str(depart_predict[0]) + "\n")
            self.output_box.config(state=DISABLED)

        if self.arrive_station_menu is not None:
            line = self.end_line.get()
            station = self.end_station.get()
            self.output_box.config(state=NORMAL)
            self.output_box.insert(END, "Finding second station...\n")
            arrive_predict = make_prediction(find_api_name(line, station), line,
                                        directions_dict.get(arrive_sublines), arrive_sublines)
            self.output_box.insert(END, "Next train at " + station + ": " + str(arrive_predict[0]) + "\n")
            self.output_box.config(state=DISABLED)


    def deleteRouteCommand(self):
        self.output_box.config(state=NORMAL)
        stmt = "DELETE FROM Track WHERE first_station=\"" + self.start_station.get() + \
               "\" AND dest_station=\"" + self.end_station.get() + "\""
        self.cnx.cmd_query(query=stmt)
        self.output_box.insert(END, "Deleted track with given depart and arrive stations.\n")
        self.output_box.config(state=DISABLED)

    def onExit(self):
        self.disconnectFromDB()
        self.quit()

    def onSelectDepartColor(self, current_line):
        station_options = []

        if (current_line == "Blue"):
            station_options = blue_line_stations
            self.start_subline = random.choice(blue_sublines)
        elif (current_line == "Green-B"):
            station_options = green_line_b_stations
            self.start_subline = random.choice(green_b_sublines)
        elif (current_line == "Green-C"):
            station_options = green_line_c_stations
            self.start_subline = random.choice(green_c_sublines)
        elif (current_line == "Green-D"):
            station_options = green_line_d_stations
            self.start_subline = random.choice(green_d_sublines)
        elif (current_line == "Green-E"):
            station_options = green_line_e_stations
            self.start_subline = random.choice(green_e_sublines)
        elif (current_line == "Red"):
            station_options = red_line_stations
            self.start_subline = random.choice(red_sublines)
        else:
            station_options = orange_line_stations
            self.start_subline = random.choice(orange_sublines)

        depart_station_menu = OptionMenu(self, self.start_station, *station_options)
        if self.depart_station_menu is not None:
            self.depart_station_menu.destroy()
        self.depart_station_menu = depart_station_menu
        self.depart_station_menu.grid(row=2, column=2, padx=5, pady=10, sticky="w")


    def onSelectArriveColor(self, current_line):
        station_options = []

        if (current_line == "Blue"):
            station_options = blue_line_stations
            self.end_subline = random.choice(blue_sublines)
        elif (current_line == "Green-B"):
            station_options = green_line_b_stations
            self.end_subline = random.choice(green_b_sublines)
        elif (current_line == "Green-C"):
            station_options = green_line_c_stations
            self.end_subline = random.choice(green_c_sublines)
        elif (current_line == "Green-D"):
            station_options = green_line_d_stations
            self.end_subline = random.choice(green_d_sublines)
        elif (current_line == "Green-E"):
            station_options = green_line_e_stations
            self.end_subline = random.choice(green_e_sublines)
        elif (current_line == "Red"):
            station_options = red_line_stations
            self.end_subline = random.choice(red_sublines)
        else:
            station_options = orange_line_stations
            self.end_subline = random.choice(orange_sublines)

        arrive_station_menu = OptionMenu(self, self.end_station, *station_options)
        if self.arrive_station_menu is not None:
            self.arrive_station_menu.destroy()
        self.arrive_station_menu = arrive_station_menu
        self.arrive_station_menu.grid(row=3, column=2, padx=5, pady=10, sticky="w")

def main():
    root = Tk()
    root.geometry("800x500+100+100")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()