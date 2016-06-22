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
    "----------------------",
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
    "----------------------",
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
    "----------------------",
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
    "----------------------",
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
                    "------------------",
                    "Braintree Branch - North Quincy",
                    "Braintree Branch - Wollaston",
                    "Braintree Branch - Quincy Center",
                    "Braintree Branch - Quincy Adams",
                    "Braintree Branch - Braintree",
                    "------------------",
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

silverLineStations = [ "Silver" ]

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

        self.parent.title("MBTA Subway Route Planner")
        self.pack(fill=BOTH, expand=True)

        # Button
        newButton = Button(self, text="New route", command=self.newRouteCommand)
        newButton.grid(row=0, column=0)
        saveButton = Button(self, text="Save route", command=self.saveRouteCommand)
        saveButton.grid(row=0, column=1)
        loadButton = Button(self, text="Load existing route",command=self.loadRouteCommand)
        loadButton.grid(row=0, column=2)
        deleteButton = Button(self, text="Delete current route", command=self.deleteRouteCommand)
        deleteButton.grid(row=0, column=3)

        lineLabel = Label(self, text="Select an MBTA Subway Line")
        lineLabel.grid(row=1, column=1, columnspan=2, ipady=10)
        stationLabel = Label(self, text="Select a Station")
        stationLabel.grid(row=1, column=3, columnspan=2, ipady=10)

        departLine = StringVar(self)
        arriveLine = StringVar(self)

        departMessage = Label(self, text="Depart from: ")
        departMessage.grid(row=2, column=0)

        departLineMenu = OptionMenu(self, departLine, *lineOptions, command=self.onSelectDepartColor)
        departLineMenu.grid(row=2, column=1, columnspan=2, ipady=10)

        departTime = StringVar(value="(optional) Time of departure")
        departEntry = Entry(self, textvariable=departTime)
        departEntry.grid(row=2, column=5)

        arriveMessage = Label(self, text="Arrive at: ")
        arriveMessage.grid(row=3, column=0)

        arriveLineMenu = OptionMenu(self, arriveLine, *lineOptions, command=self.onSelectArriveColor)
        arriveLineMenu.grid(row=3, column=1, columnspan=2, ipady=10)

        arriveTime = StringVar(value="(optional) Time of arrival")
        arriveEntry = Entry(self, textvariable=arriveTime)
        arriveEntry.grid(row=3, column=5)

        updateButton = Button(self, text="Calculate route", command=self.updateRouteCommand)
        updateButton.grid(row=4, column=1, columnspan=4, ipady=10)

        #Menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)

        fileMenu.add_separator()

        fileMenu.add_command(label="Exit", command=self.onExit)

        menubar.add_cascade(label="File", menu=fileMenu)

    def newRouteCommand(self):
        print("New route request: To be written")

    def saveRouteCommand(self):
        print("Write route to database")

    def loadRouteCommand(self):
        print("Present all existing routes to user")

    def updateRouteCommand(self):
        print("Update times of arrival for current route, if any")

    def deleteRouteCommand(self):
        print("Delete current route from database, if stored")

    def onExit(self):
        self.disconnectFromDB()
        self.quit()

    # Function for the checkbutton
    def onClick(self):
        if self.var.get():
            self.master.title("Checkbutton")
        else:
            self.master.title("Deselected")

    # Function for the listbox
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)

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
        departStationMenu.grid(row=2, column=3, columnspan=2, ipady=10)

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
        arriveStationMenu.grid(row=3, column=3, columnspan=2, ipady=10)

def main():
    root = Tk()
    root.geometry("600x400+100+100")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()