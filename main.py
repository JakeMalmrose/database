import time
import database as db
import os

simple_path = "C:/Users/JMalmrose/Downloads/people/simple/"
long_path = "C:/Users/JMalmrose/Downloads/people/long/"
base_path = "C:/Users/JMalmrose/Downloads/people/"
serialized_path = "C:/Users/JMalmrose/Downloads/people/serialized/"

def main():
    #timing the PrintPeopleDetails function
    print("Time to PrintPeopleDetails in simple directory: " + str(time_task(db.PrintPeopleDetails, simple_path)))

    #serializing all employees in simple directory
    #db.SerializeAllEmployees(simple_path)

    #timing the PrintPeopleDetails function on serialized files
    print("Time print serialized files: " + str(time_task(db.PrintPeopleDetailsSerialized, simple_path + "serialized")))

def time_task(method, *args):
    timeStart = time.perf_counter()
    method(*args)
    timeEnd = time.perf_counter()
    return (timeEnd - timeStart)*1000


main()

