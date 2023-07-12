import time
import database as db
import os

simple_path = "C:/Users/JMalmrose/Downloads/people/simple/"
long_path = "C:/Users/JMalmrose/Downloads/people/long/"
base_path = "C:/Users/JMalmrose/Downloads/people/"

def main():
    #timing the PrintPeopleDetails function
    print("Time to PrintPeopleDetails in simple directory: " + str(time_task(db.PrintPeopleDetails, simple_path)))

def time_task(method, *args):
    timeStart = time.perf_counter()
    method(*args)
    timeEnd = time.perf_counter()
    return timeEnd - timeStart


main()

