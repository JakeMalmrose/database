import os
import csv

class employee:
    # Required fields are an employee ID, first and last name, and their age stored in birth year
    # Possible but not required fields are salary and employment date
    def __init__(self, id, firstName, lastName, hireYear):
        if not id: # checking to make sure the ID is not empty or none
            raise ValueError("ID is required")
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.hireYear = hireYear

    
    def toString(self):
        return str(self.id) + " " + self.firstName + " " + self.lastName + " " + str(self.hireYear)
    


def PrintPeopleDetails(path):
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
            
        


