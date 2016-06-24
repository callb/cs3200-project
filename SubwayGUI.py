from Tkinter import *
import mysql.connector
from mysql.connector import errorcode

lineOptions = [
    "Blue",
    "Green",
    "Orange",
    "Red",
    "Silver"
]

blueLineStations = [
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

greenLineStations = [
    "Lechmere",
    "Science Park",
    "North Station",
    "Haymarket",
    "Government Center",
    "Park Street",
    "Boylston Street",
    "Arlington",
    "Copley",
    "B, C, D - Hynes Convention Center",
    "B, C, D - Kenmore",
    "B - Blandford Street",
    "B - Boston University East",
    "B - Boston University Center",
    "B - Boston University West",
    "B - St. Paul Street",
    "B - Pleasant Street",
    "B - Babcock Street",
    "B - Packards Corner",
    "B - Harvard Avenue",
    "B - Griggs Street/Long Avenue",
    "B - Allston Street",
    "B - Warren Street",
    "B - Washington Street",
    "B - Sutherland Road",
    "B - Chiswick Road",
    "B - Chestnut Hill Avenue",
    "B - South Street",
    "B - Boston College",
    "C - St. Marys Street",
    "C - Hawes Street",
    "C - Kent Street",
    "C - St. Paul Street",
    "C - Coolidge Corner",
    "C - Summit Avenue",
    "C - Brandon Hall",
    "C - Fairbanks",
    "C - Washington Square",
    "C - Tappan Street",
    "C - Dean Road",
    "C - Englewood Avenue",
    "C - Cleveland Circle",
    "D - Fenway",
    "D - Longwood",
    "D - Brookline Village",
    "D - Brookline Hills",
    "D - Beaconsfield",
    "D - Reservoir",
    "D - Chestnut Hill",
    "D - Newton Centre",
    "D - Newton Highlands",
    "D - Eliot",
    "D - Waban",
    "D - Woodland",
    "D - Riverside",
    "E - Prudential",
    "E - Symphony",
    "E - Northeastern University",
    "E - Museum of Fine Arts",
    "E - Longwood Medical Area",
    "E - Brigham Circle",
    "E - Fenwood Road",
    "E - Mission Park",
    "E - Riverway",
    "E - Back of the Hill",
    "E - Heath Street"
]

orangeLineStations = [ "Oak Grove",
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
                       "Massachusetts Avenue",
                       "Ruggles Station",
                       "Roxbury Crossing",
                       "Jackson Square",
                       "Stony Brook",
                       "Green Street",
                       "Forest Hills"]

redLineStations = [ "Alewife",
                    "Davis",
                    "Porter Square",
                    "Harvard Square",
                    "Central Square",
                    "Kendall",
                    "Charles/MGH",
                    "Park Street",
                    "Downtown Crossing",
                    "South Station",
                    "Broadway",
                    "Andrew",
                    "JFK/UMass",
                    "Braintree Branch - North Quincy",
                    "Braintree Branch - Wollaston",
                    "Braintree Branch - Quincy Center",
                    "Braintree Branch - Quincy Adams",
                    "Braintree Branch - Braintree",
                    "Ashmont Branch - Savin Hill",
                    "Ashmont Branch - Fields Corner",
                    "Ashmont Branch - Shawmut",
                    "Ashmont Branch - Ashmont",
                    "Mattapan Branch - Cedar Grove",
                    "Mattapan Branch - Butler",
                    "Mattapan Branch - Milton",
                    "Mattapan Branch - Central Avenue",
                    "Mattapan Branch - Valley Road",
                    "Mattapan Branch - Capen Street",
                    "Mattapan Branch - Mattapan",]

silverLineStations = [
    "SL1, SL2, SL4 - South Station",
    "SL1, SL2 - Courthouse",
    "SL1, SL2 - World Trade Center",
    "SL1, SL2 - Silver Line Way",
    "SL1 - Logan Airport Terminal A",
    "SL1 - Logan Airport Terminal B south",
    "SL1 - Logan Airport Terminal B north",
    "SL1 - Logan Airport Terminal C",
    "SL1 - Logan Airport Terminal E",
    "SL1 - Seaport Hotel",
    "SL2 - 306 Northern Avenue",
    "SL2 - Northern Avenue & Harbor Street",
    "SL2 - Northern Avenue & Tide Street",
    "SL2 - 21 Dry Dock Avenue",
    "SL2 - 25 Dry Dock Avenue",
    "SL2 - 88 Black Falcon Avenue",
    "SL2 - Design Center",
    "SL4, SL5 - Dudley Square",
    "SL4, SL5 - Melnea Cass Boulevard",
    "SL4, SL5 - Lenox Street",
    "SL4, SL5 - Massachusetts Avenue",
    "SL4, SL5 - Worcester Square",
    "SL4, SL5 - Newton Street",
    "SL4, SL5 - Union Park Street",
    "SL4, SL5 - East Berkeley Street",
    "SL4, SL5 - Herald Street",
    "SL4, SL5 - Tufts Medical Center",
    "SL4, SL5 - Chinatown",
    "SL5 - Boylston",
    "SL5 - Downtown Crossing"
]

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()
        self.cnx = self.connectToDB()

    def connectToDB(self):
        try:
            cnx = mysql.connector.connect(user='root', password='root', \
                    host='127.0.0.1', database='MBTA_Subway')
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

        self.departStation = None
        self.arriveStation = None

        self.parent.title("MBTA Subway Route Planner")
        self.pack(fill=BOTH, expand=True)

        # Buttons for CRUD
        newButton = Button(self, text="New route", command=self.newRouteCommand)
        newButton.grid(row=0, column=0)
        saveButton = Button(self, text="Save route", command=self.saveRouteCommand)
        saveButton.grid(row=0, column=1)
        loadButton = Button(self, text="Load existing route",command=self.loadRouteCommand)
        loadButton.grid(row=0, column=2)
        deleteButton = Button(self, text="Delete current route", command=self.deleteRouteCommand)
        deleteButton.grid(row=0, column=3)

        # Column label to indication Station selection
        lineLabel = Label(self, text="Select an MBTA Subway Line", fg="blue")
        lineLabel.grid(row=1, column=1, pady=10)

        # Column label to indicate Station selection
        stationLabel = Label(self, text="Select a Station", fg="blue")
        stationLabel.grid(row=1, column=2, pady=10)

        # Row label
        departMessage = Label(self, text="Depart from: ")
        departMessage.grid(row=2, column=0)

        # MBTA Line drop-down menu for starting station
        departLine = StringVar(self)
        departLineMenu = OptionMenu(self, departLine, *lineOptions, command=self.onSelectDepartColor)
        departLineMenu.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        departLineMenu.config(width=8)

        # Departure time entry box
        departTime = StringVar(value="(optional) Time of departure")
        departEntry = Entry(self, textvariable=departTime, fg="gray")
        departEntry.grid(row=2, column=3)
        departEntry.config(width=20)

        # Row label
        arriveMessage = Label(self, text="Arrive at: ")
        arriveMessage.grid(row=3, column=0)

        # MBTA Line drop-down menu for ending station
        arriveLine = StringVar(self)
        arriveLineMenu = OptionMenu(self, arriveLine, *lineOptions, command=self.onSelectArriveColor)
        arriveLineMenu.grid(row=3, column=1, padx=5, pady=10, sticky="w")
        arriveLineMenu.config(width=8)

        # Arrival time entry box
        arriveTime = StringVar(value="(optional) Time of arrival")
        arriveEntry = Entry(self, textvariable=arriveTime, fg="gray")
        arriveEntry.grid(row=3, column=3)
        arriveEntry.config(width=20)

        # Button to retrieve times for current route
        updateButton = Button(self, text="Calculate route", command=self.updateRouteCommand)
        updateButton.grid(row=4, column=1, columnspan=4, padx=5, pady=10)

        # Output box
        self.outputBox = Text(self)
        self.outputBox.grid(row=5, column=1, columnspan=3)
        self.outputBox.config(state=DISABLED, height=10)

        # Scrollbar for Output box
        scrollb = Scrollbar(self, command=self.outputBox.yview)
        scrollb.grid(row=5, column=4, sticky='nsew')
        self.outputBox['yscrollcommand'] = scrollb.set

        #Menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

    def newRouteCommand(self):
        if self.arriveStation != None:
            self.arriveStation.destroy()
        if self.departStation != None:
            self.departStation.destroy()
        self.outputBox.config(state=NORMAL)
        self.outputBox.delete('1.0', END)
        self.outputBox.insert(END, "New route request\n")
        self.outputBox.config(state=DISABLED)

    def saveRouteCommand(self):
        print("Write route to database")

    def loadRouteCommand(self):
        print("Present all existing routes to user")

    def updateRouteCommand(self):
        self.outputBox.config(state=NORMAL)
        self.outputBox.insert(END, "Update times of arrival for current route, if any\n")
        self.outputBox.config(state=DISABLED)

    def deleteRouteCommand(self):
        self.outputBox.config(state=NORMAL)
        self.outputBox.insert(END, "Delete current route from database, if stored\n")
        self.outputBox.config(state=DISABLED)

    def onExit(self):
        self.disconnectFromDB()
        self.quit()

    def onSelectDepartColor(self, currentLine):
        currentStation = StringVar(self)

        if (currentLine == "Blue"):
            stationOptions = blueLineStations
        elif (currentLine == "Green"):
            stationOptions = greenLineStations
        elif (currentLine == "Red"):
            stationOptions = redLineStations
        elif (currentLine == "Orange"):
            stationOptions = orangeLineStations
        else:
            stationOptions = silverLineStations

        departStationMenu = OptionMenu(self, currentStation, *stationOptions)
        if self.departStation != None:
            self.departStation.destroy()
        self.departStation = departStationMenu
        self.departStation.grid(row=2, column=2, padx=5, pady=10, sticky="w")


    def onSelectArriveColor(self, currentLine):
        currentStation = StringVar(self)

        if (currentLine == "Blue"):
            stationOptions = blueLineStations
        elif (currentLine == "Green"):
            stationOptions = greenLineStations
        elif (currentLine == "Red"):
            stationOptions = redLineStations
        elif (currentLine == "Orange"):
            stationOptions = orangeLineStations
        else:
            stationOptions = silverLineStations

        arriveStationMenu = OptionMenu(self, currentStation, *stationOptions)
        if self.arriveStation != None:
            self.arriveStation.destroy()
        self.arriveStation = arriveStationMenu
        self.arriveStation.grid(row=3, column=2, padx=5, pady=10, sticky="w")

def main():
    root = Tk()
    root.geometry("800x500+100+100")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
