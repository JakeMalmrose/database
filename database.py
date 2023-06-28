import os
import csv

class employee:
    def __init__(self, id, firstName, lastName, hireYear):
        if not id: # checking to make sure the ID is not empty or none
            raise ValueError("ID is required")
        self.id = id
        self.firstName = str(firstName).strip() # we store csv with whitespace, so we need to strip it
        self.lastName = str(lastName).strip()
        self.hireYear = int(str(hireYear).strip())

    
    def toString(self):
        return str(self.id) + " " + self.firstName + " " + self.lastName + " " + str(self.hireYear)
    


def PrintPeopleDetails(path):
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            print(f.read())

def PrintEmployees(path):
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                id, firstName, lastName, hireYear = row
                emp = employee(id, firstName, lastName, hireYear)
                print(emp.toString())
            
        


