import re
from database import Database
from models import Student
from controllers.subject_controller import SubjectController


class StudentController:
    """Handles student registration and login."""

    EMAIL_REGEX = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
    PASSWORD_REGEX = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"
    NAME_REGEX = r"^[A-Za-z]+(?: [A-Za-z]+)+$"

    def student_menu(self):
        """Display the student system menu and dispatch to login or register."""
        while True:
            choice = input("        Student System (l/r/x): ").strip()
            if choice == "l":
                self.login()
            elif choice == "r":
                self.register()
            elif choice == "x":
                break
            else:
                print("        Invalid student option")

    def register(self):
        """Register a new student after validating name, email, password, and uniqueness."""
        print("        Student Sign Up")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not re.match(self.EMAIL_REGEX, email) or not re.match(self.PASSWORD_REGEX, password):
                print("        Incorrect email or password format")
                continue

            db = Database()
            students = db.load_students()

            for existing in students:
                if existing.email == email:
                    print(f"        Student with email {email} already exists")
                    return

            name = input("        Name: ").strip()
            if not re.match(self.NAME_REGEX, name):
                print("        Incorrect name format. Please enter a first and last name using letters only.")
                continue

            student_id = Student.generate_unique_id({s.id for s in students})
            student = Student(name=name, email=email, password=password, id=student_id)
            students.append(student)
            db.save_students(students)
            print(f"        Enrolling Student {name}")
            break

    def login(self):
        """Authenticate a student by email and password, then open their course menu."""
        print("        Student Sign In")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not re.match(self.EMAIL_REGEX, email) or not re.match(self.PASSWORD_REGEX, password):
                print("        Incorrect email or password format")
                continue

            db = Database()
            students = db.load_students()

            found = None
            for s in students:
                if s.email == email and s.password == password:
                    found = s
                    break

            if found is None:
                print("        Student does not exist")
                return

            SubjectController().subject_menu(found)
            break
