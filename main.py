import database as db

simple_path = "C:/Users/JMalmrose/Downloads/people/simple/"
long_path = "C:/Users/JMalmrose/Downloads/people/long/"
base_path = "C:/Users/JMalmrose/Downloads/people/"

def main():
    db.PrintPeopleDetails(base_path + "simple/")
    db.PrintEmployees(simple_path)


main()

