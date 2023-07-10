import unittest
import database as db
import tempfile
import os
import sys
import io
import pickle
#simple_path = "C:/Users/Draupniyr/Downloads/Assignment 1 - data-1/people/simple"
#cant use simple path here

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
        pass

    def test_GetAllEmployees(self):
        pass

    def test_PrintAllEmployees(self):
        pass

if __name__ == '__main__':
    unittest.main()
