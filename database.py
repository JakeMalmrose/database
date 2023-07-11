import os
import csv
import pickle

class employee:
    def __init__(self, id, firstName, lastName, hireYear):
        if not id: # checking to make sure the ID is not empty or none
            raise ValueError("ID is required")
        self.id = id
        self.firstName = str(firstName).strip() # we store csv with whitespace, so we need to strip it
        self.lastName = str(lastName).strip()
        self.hireYear = int(str(hireYear).strip())

    
    def __str__(self):
        return str(self.id) + " " + self.firstName + " " + self.lastName + " " + str(self.hireYear)
    
    
def AddEmployee(path, id, firstName, lastName, hireYear):
    with open(os.path.join(path, str(id) + ".txt"), "w") as f:
        f.write(str(id) + ", " + firstName + ", " + lastName + ", " + str(hireYear))

def DeleteEmployee(path, id):
    os.remove(os.path.join(path, str(id) + ".txt"))

def UpdateEmployee(path, id, firstName, lastName, hireYear):
    if not os.path.exists(os.path.join(path, str(id) + ".txt")):
        raise FileNotFoundError("Employee " + str(id) + " does not exist")
    with open(os.path.join(path, str(id) + ".txt"), "w") as f:
        f.write(str(id) + ", " + firstName + ", " + lastName + ", " + str(hireYear))    

def SerializeAllEmployees(path):
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                id, firstName, lastName, hireYear = row
                emp = employee(id, firstName, lastName, hireYear)
                if not os.path.exists(path + "serialized"): # need to create directory if not already there
                    os.mkdir(path + "serialized")
                PickleSerializeEmployee(emp, path + "serialized")

def PickleSerializeEmployee(employee, path):
    with open(os.path.join(path, str(employee.id) + ".pickle"), 'wb') as f:
        pickle.dump(employee, f)
        f.close()

def GetSerializedEmployee(path, id):
    with open(os.path.join(path, str(id) + ".pickle"), 'rb') as f:
        emp = pickle.load(f)
        f.close()
        return emp

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
                print(str(emp))
            
def FindEmployeeByLastName(path, lastName):
    # look through all serialized employees and return the first one with the given last name
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'rb') as f:
            emp = pickle.load(f)
            if emp.lastName == lastName:
                return emp
    return None

def FindAllEmployeesByLastName(path, lastName):
    employees = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'rb') as f:
            emp = pickle.load(f)
            if emp.lastName == lastName:
                employees.append(emp)
    return employees

def GetAllEmployees(path):
    pass

def PrintAllEmployees(path):
    pass