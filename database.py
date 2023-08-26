import os
import csv
import pickle
import pymongo
import pymongo.errors
from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError
import redis

def ConnectToRedis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

def ConnectToRedisTestDrop():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()
    return r

def AddEmployeeRedis(r, id, firstName, lastName, hireYear):
    if r.exists(id):
        raise redis.exceptions.ResponseError("Employee " + str(id) + " already exists")
    else:
        r.set(id, firstName + "," + lastName + "," + str(hireYear))

def FindEmployeeRedis(r, id):
    if r.exists(id):
        return r.get(id)
    else:
        return None

def DeleteEmployeeRedis(r, id):
    if r.exists(id):
        r.delete(id)
    else:
        raise redis.exceptions.ResponseError("Employee " + str(id) + " does not exist")

def UpdateEmployeeRedis(r, id, firstName, lastName, hireYear):
    if r.exists(id):
        r.set(id, firstName + "," + lastName + "," + str(hireYear))
    else:
        raise redis.exceptions.ResponseError("Employee " + str(id) + " does not exist")


def ConnectToNeo4j():
    uri = "bolt://127.0.0.1:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password2"))
    driver.close()
    return driver

def ConnectToNeoTestDrop():
    uri = "bolt://127.0.0.1:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password2"))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()
    return driver

def AddEmployeeNeo(driver, id, firstName, lastName, hireYear):
    with driver.session() as session:
        session.run("CREATE (a:Employee {id: $id, firstName: $firstName, lastName: $lastName, hireYear: $hireYear})", {"id": id, "firstName": firstName, "lastName": lastName, "hireYear": hireYear})

def DeleteEmployeeNeo(driver, id):
    with driver.session() as session:
        session.run("MATCH (a:Employee {id: $id}) DETACH DELETE a", {"id": id})

def UpdateEmployeeNeo(driver, id, firstName, lastName, hireYear):
    with driver.session() as session:
        session.run("MATCH (a:Employee {id: $id}) SET a.firstName = $firstName, a.lastName = $lastName, a.hireYear = $hireYear", {"id": id, "firstName": firstName, "lastName": lastName, "hireYear": hireYear})

def PrintEmployeesNeo(driver):
    with driver.session() as session:
        result = session.run("MATCH (a:Employee) RETURN a.id, a.firstName, a.lastName, a.hireYear")
        for record in result:
            print("Id: " +str(record[0]) + ", Name: " + str(record[1]) + " " + str(record[2]) + ", Hire Year: " + str(record[3]))

def FindEmployeeNeo(driver, id):
    with driver.session() as session:
        result = session.run("MATCH (a:Employee {id: $id}) RETURN a.id, a.firstName, a.lastName, a.hireYear", {"id": id})
        for record in result:
            return record

def AddRelationshipNeo(driver, id1, id2, relationship):
    with driver.session() as session:
        session.run("MATCH (a:Employee {id: $id1}), (b:Employee {id: $id2}) CREATE (a)-[:" + relationship + "]->(b)", {"id1": id1, "id2": id2})

def DeleteRelationshipNeo(driver, id1, id2, relationship):
    with driver.session() as session:
        session.run("MATCH (a:Employee {id: $id1})-[r:" + relationship + "]->(b:Employee {id: $id2}) DELETE r", {"id1": id1, "id2": id2})

def GetRelationshipsNeo(driver, id):
    with driver.session() as session:
        result = session.run("MATCH (a:Employee {id: $id})-[r]->(b:Employee) RETURN r", {"id": id})
        relationships = []
        for record in result:
            relationships.append(record.values()[0].type)
        return relationships

def FindRelationshipsNeo(driver, id1, id2):
    with driver.session() as session:
        result = session.run("MATCH (a:Employee {id: $id1})-[r]->(b:Employee {id: $id2}) RETURN r", {"id1": id1, "id2": id2})
        relationships = []
        for relation in result:
            relationships.append(relation.values()[0].type)
        return relationships



def ConnectToMongoDB():
    client = pymongo.MongoClient("mongodb://localhost:2717/")
    return client["pythondatabase"]

def ConnectToMongoDBTestDrop():
    client = pymongo.MongoClient("mongodb://localhost:2717/")
    client.drop_database("testdatabase")
    return client["testdatabase"]

def AddEmployeeMongo(db, id, firstName, lastName, hireYear):
    collection = db["employees"]
    if FindEmployeeMongo(db, id):
        raise pymongo.errors.DuplicateKeyError("Employee " + str(id) + " already exists")
    employee = { "id": id, "firstName": firstName, "lastName": lastName, "hireYear": hireYear }
    collection.insert_one(employee)

def DeleteEmployeeMongo(db, id):
    collection = db["employees"]
    collection.delete_one({"id": id})

def UpdateEmployeeMongo(db, id, firstName, lastName, hireYear):
    collection = db["employees"]
    collection.update_one({"id": id}, {"$set": {"firstName": firstName, "lastName": lastName, "hireYear": hireYear}})

def PrintEmployeesMongo(db):
    collection = db["employees"]
    for x in collection.find():
        print(x)

def FindEmployeeMongo(db, id):
    collection = db["employees"]
    for x in collection.find({"id": id}):
        return x
    
#-----------------------------------------#

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
    
#-----------------------------------------#

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
        if file.endswith(".txt"):
            with open(os.path.join(path, file), 'r') as f:
                print(f.read())

def PrintPeopleDetailsSerialized(path): # im sorry but im not breaking my tests to read pickled files </3
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'rb') as f:
            emp = pickle.load(f)
            print(str(emp)) 

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
    dictionary = {}
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'rb') as f:
            emp = pickle.load(f)
            dictionary[emp.id] = emp
    return dictionary

def PrintAllEmployees(path):
    dictionary = GetAllEmployees(path)
    for key in dictionary: # i love for statements man
        print(dictionary[key])