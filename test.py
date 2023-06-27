import unittest
import database as db
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

    def test_PrintPeopleDetails(self):
        self.assertIsNotNone(db.PrintPeopleDetails(simple_path))

    def test_PrintEmployees(self):
        pass

if __name__ == '__main__':
    unittest.main()
