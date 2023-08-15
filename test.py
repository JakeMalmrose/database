import unittest
import database as db
import tempfile
import os
import sys
import io
import pickle
import pymongo
import pymongo.errors
import neo4j
import neo4j.exceptions
#simple_path = "C:/Users/Draupniyr/Downloads/Assignment 1 - data-1/people/simple"
#cant use simple path here

class TestNeo4j(unittest.TestCase):
    def test_ConnectToNeo4j(self):
        db.ConnectToNeoTestDrop()

    def test_AddEmployee(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        self.assertTrue(db.FindEmployeeNeo(driver, 1))
        
    def test_AddRelationship(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        db.AddEmployeeNeo(driver, 2, "Jane", "Doe", 2019)
        db.AddRelationshipNeo(driver, 1, 2, "FRIENDS_WITH")
        self.assertTrue(db.FindRelationshipsNeo(driver, 1, 2))
    
    def test_FindRelationships(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        db.AddEmployeeNeo(driver, 2, "Jane", "Doe", 2019)
        db.AddRelationshipNeo(driver, 1, 2, "FRIENDS_WITH")
        db.AddRelationshipNeo(driver, 1, 2, "WORKS_WITH")
        self.assertEqual(db.FindRelationshipsNeo(driver, 1, 2), ["FRIENDS_WITH", "WORKS_WITH"])

    def test_FindEmployee(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        employee = db.FindEmployeeNeo(driver, 1)
        self.assertEqual(employee["a.id"], 1)
        self.assertEqual(employee["a.firstName"], "John")
        self.assertEqual(employee["a.lastName"], "Doe")
        self.assertEqual(employee["a.hireYear"], 2019)
    
    def test_DeleteEmployee(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        db.DeleteEmployeeNeo(driver, 1)
        self.assertFalse(db.FindEmployeeNeo(driver, 1))
    
    def test_DeleteRelationship(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        db.AddEmployeeNeo(driver, 2, "Jane", "Doe", 2019)
        db.AddRelationshipNeo(driver, 1, 2, "FRIENDS_WITH")
        db.DeleteRelationshipNeo(driver, 1, 2, "FRIENDS_WITH")
        self.assertFalse(db.FindRelationshipsNeo(driver, 1, 2))
        
    def test_UpdateEmployee(self):
        driver = db.ConnectToNeoTestDrop()
        db.AddEmployeeNeo(driver, 1, "John", "Doe", 2019)
        db.UpdateEmployeeNeo(driver, 1, "John", "Cena", 2032)
        employee = db.FindEmployeeNeo(driver, 1)
        self.assertEqual(employee["a.firstName"], "John")
        self.assertEqual(employee["a.lastName"], "Cena")
        self.assertEqual(employee["a.hireYear"], 2032)
        

class TestMongoDB(unittest.TestCase):
    def test_ConnectToMongoDB(self):
        db.ConnectToMongoDBTestDrop()
    
    def test_AddEmployeeMongo(self):
        client = db.ConnectToMongoDBTestDrop()
        db.AddEmployeeMongo(client, 1, "John", "Doe", 2019)
        self.assertTrue(db.FindEmployeeMongo(client, 1))
        self.assertRaises(pymongo.errors.DuplicateKeyError, db.AddEmployeeMongo, client, 1, "John", "Doe", 2019)
    
    def test_FindEmployeeMongo(self):
        client = db.ConnectToMongoDBTestDrop()
        db.AddEmployeeMongo(client, 1, "John", "Doe", 2022)
        db.AddEmployeeMongo(client, 2, "Chris", "Hansen", 2012)
        employee = db.FindEmployeeMongo(client, 2)
        self.assertEqual(employee["id"], 2)
        self.assertEqual(employee["firstName"], "Chris")
        self.assertEqual(employee["lastName"], "Hansen")
        self.assertEqual(employee["hireYear"], 2012)

    def test_UpdateEmployeeMongo(self):
        client = db.ConnectToMongoDBTestDrop()
        db.AddEmployeeMongo(client, 1, "Beans", "Doe", 2019)
        db.UpdateEmployeeMongo(client, 1, "John", "Cena", 2032)
        employee = db.FindEmployeeMongo(client, 1)
        self.assertEqual(employee["firstName"], "John")
        self.assertEqual(employee["lastName"], "Cena")
        self.assertEqual(employee["hireYear"], 2032)
    
    def test_DeleteEmployeeMongo(self):
        client = db.ConnectToMongoDBTestDrop()
        db.AddEmployeeMongo(client, 1, "John", "Doe", 2019)
        db.DeleteEmployeeMongo(client, 1)
        self.assertFalse(db.FindEmployeeMongo(client, 1))
    
    

class TestEmployee(unittest.TestCase):
    def test_employee_init(self):
        testEmp = db.employee(1, "John", "Doe", 2019)

        self.assertEqual(testEmp.id, 1)
        self.assertEqual(testEmp.firstName, "John")
        self.assertEqual(testEmp.lastName, "Doe")
        self.assertEqual(testEmp.hireYear, 2019)
        self.assertRaises(ValueError, db.employee, None, "John", "Doe", 2019)
        self.assertRaises(ValueError, db.employee, "", "John", "Doe", 2019)

    def test_employee_toString(self):
        testEmp = db.employee(1, "John", "Doe", 2019)
        self.assertEqual(str(testEmp), "1 John Doe 2019")

class testDatabase(unittest.TestCase):
    def test_PrintPeopleDetails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # need all this stuff so we can grab the output of the PrintPeopleDetails function
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("Test content 1")
            with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
                f.write("Test content 2")
            db.PrintPeopleDetails(tmpdir)

        self.assertIn("Test content 1", captured_output.getvalue())
        self.assertIn("Test content 2", captured_output.getvalue())

    def test_PrintEmployees(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # changing sys.stdout again so we can look at it
            captured_output = io.StringIO()
            sys.stdout = captured_output

            with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("1, John, Doe, 2019")
            with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
                f.write("2, Jane, Doe, 2019")
            db.PrintEmployees(tmpdir)

        self.assertIn("1 John Doe 2019", captured_output.getvalue())
        self.assertIn("2 Jane Doe 2019", captured_output.getvalue())

    def test_AddEmployee(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db.AddEmployee(tmpdir, 1, "John", "Doe", 2019)
            with open(os.path.join(tmpdir, "1.txt"), "r") as f:
                self.assertEqual(f.read(), "1, John, Doe, 2019")

    def test_DeleteEmployee(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.txt"), "w") as f:

                f.write("1, John, Doe, 2019")
            db.DeleteEmployee(tmpdir, 1)

            self.assertFalse(os.path.exists(os.path.join(tmpdir, "1.txt")))

    def test_UpdateEmployee(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.txt"), "w") as f: # create file and write sample employee
                f.write("1, John, Doe, 2019")

            db.UpdateEmployee(tmpdir, 1, "John", "ButWithNoH", 2003) # change their name and hire year

            with open(os.path.join(tmpdir, "1.txt"), "r") as f:
                self.assertEqual(f.read(), "1, John, ButWithNoH, 2003")
            # check to make sure you cant update a non-existent employee
            self.assertRaises(FileNotFoundError, db.UpdateEmployee, tmpdir, 2, "John", "ButWithNoH", 2003)

    def test_SerializeAllEmployees(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.txt"), "w") as f:
                f.write("1, John, Doe, 2019")
            with open(os.path.join(tmpdir, "2.txt"), "w") as f:
                f.write("2, Jane, Doe, 2019")
            db.SerializeAllEmployees(tmpdir)
            self.assertTrue(os.path.isfile(os.path.join(tmpdir + "serialized", "1.pickle")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir + "serialized", "2.pickle")))

    def test_GetSerializedEmployee(self):
        # function should de-serialize the employee at the path given
        # and return the employee object
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.pickle"), "wb") as f:
                pickle.dump(db.employee(1, "John", "Doe", 2019), f)
            emp = db.GetSerializedEmployee(tmpdir, 1)
            self.assertEqual(emp.id, 1)
            self.assertEqual(emp.firstName, "John")
            self.assertEqual(emp.lastName, "Doe")
            self.assertEqual(emp.hireYear, 2019)

    def test_PickleSerializeEmployee(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db.PickleSerializeEmployee(db.employee(1, "John", "Doe", 2019), tmpdir)
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "1.pickle")))

    def test_FindEmployeeByLastName(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.pickle"), "wb") as f:
                pickle.dump(db.employee(1, "John", "Doe", 2019), f)
            with open(os.path.join(tmpdir, "2.pickle"), "wb") as f:
                pickle.dump(db.employee(2, "Jane", "Cena", 2010), f)

            emp = db.FindEmployeeByLastName(tmpdir, "Cena")
            
            self.assertEqual(emp.id, 2)
            self.assertEqual(emp.firstName, "Jane")
            self.assertEqual(emp.lastName, "Cena")
            self.assertEqual(emp.hireYear, 2010)

    def test_FindAllEmployeesByLastName(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.pickle"), "wb") as f:
                pickle.dump(db.employee(1, "Gerald", "Mcgee", 2019), f)
            with open(os.path.join(tmpdir, "2.pickle"), "wb") as f:
                pickle.dump(db.employee(2, "John", "Cena", 2010), f)
            with open(os.path.join(tmpdir, "3.pickle"), "wb") as f:
                pickle.dump(db.employee(3, "Jimbo", "Cena", 2012), f)
            with open(os.path.join(tmpdir, "4.pickle"), "wb") as f:
                pickle.dump(db.employee(4, "John", "Cenot", 2015), f)

            emps = db.FindAllEmployeesByLastName(tmpdir, "Cena")

            self.assertEqual(len(emps), 2)
            self.assertEqual(emps[0].id, 2)
            self.assertEqual(emps[0].firstName, "John")
            self.assertEqual(emps[0].lastName, "Cena")
            self.assertEqual(emps[0].hireYear, 2010)
            self.assertEqual(emps[1].id, 3)
            self.assertEqual(emps[1].firstName, "Jimbo")


    def test_GetAllEmployees(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.pickle"), "wb") as f:
                pickle.dump(db.employee(1, "Gerald", "Mcgee", 2019), f)
            with open(os.path.join(tmpdir, "2.pickle"), "wb") as f:
                pickle.dump(db.employee(2, "John", "Cena", 2010), f)
            with open(os.path.join(tmpdir, "3.pickle"), "wb") as f:
                pickle.dump(db.employee(3, "Jimbo", "Cena", 2012), f)
            with open(os.path.join(tmpdir, "4.pickle"), "wb") as f:
                pickle.dump(db.employee(4, "John", "Cenot", 2015), f)

            emps = db.GetAllEmployees(tmpdir)

            self.assertEqual(len(emps), 4)
            self.assertEqual(emps[1].id, 1)
            self.assertEqual(emps[1].firstName, "Gerald")
            self.assertEqual(emps[1].lastName, "Mcgee")
            self.assertEqual(emps[1].hireYear, 2019)
            self.assertEqual(emps[2].id, 2)
            self.assertEqual(emps[2].firstName, "John")
            self.assertEqual(emps[3].id, 3)
            self.assertEqual(emps[3].firstName, "Jimbo")
            self.assertEqual(emps[4].id, 4)
            self.assertEqual(emps[4].firstName, "John")

    def test_PrintAllEmployees(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "1.pickle"), "wb") as f:
                pickle.dump(db.employee(1, "Gerald", "Mcgee", 2019), f)
            with open(os.path.join(tmpdir, "2.pickle"), "wb") as f:
                pickle.dump(db.employee(2, "John", "Cena", 2010), f)
            with open(os.path.join(tmpdir, "3.pickle"), "wb") as f:
                pickle.dump(db.employee(3, "Jimbo", "Cena", 2012), f)
            with open(os.path.join(tmpdir, "4.pickle"), "wb") as f:
                pickle.dump(db.employee(4, "John", "Cenot", 2015), f)
            
            captured_output = io.StringIO()
            sys.stdout = captured_output

            db.PrintAllEmployees(tmpdir)

            self.assertIn("1 Gerald Mcgee 2019", captured_output.getvalue())
            self.assertIn("2 John Cena 2010", captured_output.getvalue())
            self.assertIn("3 Jimbo Cena 2012", captured_output.getvalue())
            self.assertIn("4 John Cenot 2015", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
