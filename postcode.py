import sqlite3
from sqlite3 import OperationalError

conn = sqlite3.connect('csc455_HW3.db')
c = conn.cursor()

import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('1000x1000')
        self.configure(bg='black')
        self.bind("<F5>", self.toggleFullScreen)

        self.label_postcode = tk.Label(self, text="Please enter Postcode", font=("Arial Bold", 50), fg = "white", bg = "black")
        self.label_lon = tk.Label(self, text="", font=("Arial Bold", 50), fg  = "red", bg = "black")
        self.label_lat = tk.Label(self, text="", font=("Arial Bold", 50), fg  = "red", bg = "black")



        self.label_postcode.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.label_lon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.label_lat.place(relx=0.5, rely=0.4, anchor=tk.CENTER)



        self.txt = tk.Entry(self, width=10, font=("Arial Bold", 50), fg = "white", bg = "black")
        self.txt.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.txt.focus()

        self.btn = tk.Button(self, text="Get Geodata", command=self.clicked, font = ("Arial Bold", 100), fg = "grey", bg = "black")
        self.btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.style = ttk.Style()
        self.style.theme_use('default')

    def clicked(self):
        res = self.executeScriptsFromFile("PLZ.sql", self.txt.get())
        lat = res[0][2]
        lon = res[0][3]
        self.label_lat.configure(text=lat)
        self.label_lon.configure(text=lon)


    def executeScriptsFromFile(self, filename, postcode):
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            #try:
            c.execute(command)
            #print(command)
            result = c.execute("SELECT * FROM PLZ WHERE PLZ = %s;" % postcode).fetchall()
            return result


            #except OperationalError as msg:
                #print ("Command skipped: ", str(msg))


    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.attributes("-fullscreen", self.fullScreenState)


if __name__ == "__main__":
    app = App()
    app.mainloop()