import time
import database as db
import os

def main():
    client = db.ConnectToMongoDB()
    db.PrintEmployeesMongo(client)
    print("Adding employee")
    db.AddEmployeeMongo(client, 3, "John", "Doe", 2019)
    db.PrintEmployeesMongo(client)
    print("Finding employee")
    print(db.FindEmployeeMongo(client, 3))
    print("Updating employee")
    db.UpdateEmployeeMongo(client, 3, "John", "Cena", 2023)
    db.PrintEmployeesMongo(client)
    print("Deleting employee")
    db.DeleteEmployeeMongo(client, 3)
    db.PrintEmployeesMongo(client)






def time_task(method, *args):
    timeStart = time.perf_counter()
    method(*args)
    timeEnd = time.perf_counter()
    return (timeEnd - timeStart)*1000


main()

