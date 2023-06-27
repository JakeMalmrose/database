import unittest
import database as db
import tempfile
import os
import sys
import io
simple_path = "C:/Users/Draupniyr/Downloads/Assignment 1 - data-1/people/simple"

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
        self.assertEqual(testEmp.toString(), "1 John Doe 2019")

class testDatabase(unittest.TestCase):
    def test_PrintPeopleDetails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("Test content 1")
            with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
                f.write("Test content 2")

            # need all this stuff so we can grab the output of the PrintPeopleDetails function
            captured_output = io.StringIO()
            sys.stdout = captured_output
            db.PrintPeopleDetails(tmpdir)

        self.assertIn("Test content 1", captured_output.getvalue())
        self.assertIn("Test content 2", captured_output.getvalue())

    def test_PrintEmployees(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("1, John, Doe, 2019")
            with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
                f.write("2, Jane, Doe, 2019")

            # changing sys.stdout again so we can look at it
            captured_output = io.StringIO()
            sys.stdout = captured_output
            db.PrintEmployees(tmpdir)

        self.assertIn("1 John Doe 2019", captured_output.getvalue())
        self.assertIn("2 Jane Doe 2019", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
