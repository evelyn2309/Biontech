import csv
import sqlite3
from sqlite3 import OperationalError

conn = sqlite3.connect('csc455_HW3.db')
c = conn.cursor()

dbfile = "PLZ.sql"

def openFile(csvfile):
    with open(csvfile, encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")

        for row in csvreader:
            #print(row)
            #print(row[0].split(";")[1])
            return(executeScriptsFromFile(dbfile, row[0].split(";")[1]))

def writeFile(input, output, res):
    # Open the input_file in read mode and output_file in write mode
    with open(input, 'r') as read_obj, \
            open(output, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj, delimiter=';')
        # Read each row of the input csv file as list
        counter = 0
        r_geo = []

        for row in csv_reader:
            if counter == 0:
                row.append('Long')
                row.append('Lat')
                new = row[0].split(";")[0], row[0].split(";")[1], row[0].split(";")[2], 'Long', 'Lat'
                csv_writer.writerow(new)
            else:
                for (plz, city, long, lat) in res:
                    if plz == row[0].split(";")[1]:
                        #print(row[0].split(";")[0], counter, plz, long, lat)
                        #print((long, lat))
                        r_geo.append((long, lat))
                        new = row[0].split(";")[0], row[0].split(";")[1], row[0].split(";")[2], long, lat
                        #print(new)
                        csv_writer.writerow(new)


                        continue


            counter+=1


def executeScriptsFromFile(file, postcode):
    # Open and read the file as a single buffer
    fd = open(file, 'r')
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

res = openFile("Adressen.csv")
#print(res)

writeFile("Adressen.csv", "BiontechAddressList.csv", res)
