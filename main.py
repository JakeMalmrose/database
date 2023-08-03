import time
import database as db
import os

def main():
    client = db.ConnectToMongoDB()
    # getting each file in long directory and adding it to the database (manually)
    for file in os.listdir("C:\\Users\\Jmalmrose\\Downloads\\people\\long"):
        with open(os.path.join("C:\\Users\\Jmalmrose\\Downloads\\people\\long", file), "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    id, firstName, lastName, hireYear = line.split(",")
                    firstName = firstName.strip()
                    lastName = lastName.strip()
                    hireYear = int(hireYear.strip())
                    print("adding employee " + id + " " + firstName)
                    db.AddEmployeeMongo(client, id, firstName, lastName, hireYear)






def time_task(method, *args):
    timeStart = time.perf_counter()
    method(*args)
    timeEnd = time.perf_counter()
    return (timeEnd - timeStart)*1000


main()

