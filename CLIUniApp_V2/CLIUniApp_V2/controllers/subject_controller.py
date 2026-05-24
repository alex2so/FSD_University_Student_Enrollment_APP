import re
from database import Database
from models import Subject


class SubjectController:
    """Handles subject enrolment, removal, display, and password changes for a student."""

    PASSWORD_REGEX = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

    def subject_menu(self, student):
        """Display the student course menu and dispatch to the chosen action."""
        while True:
            choice = input("        Student Course Menu (c/e/r/s/x): ").strip()
            if choice == "c":
                self.change_password(student)
            elif choice == "e":
                self.enrol(student)
            elif choice == "r":
                self.remove_subject(student)
            elif choice == "s":
                self.show_subjects(student)
            elif choice == "x":
                break
            else:
                print("        Invalid student course option")

    def enrol(self, student):
        """Enrol the student in a new randomly generated subject (max 4 subjects)."""
        if len(student.subjects) >= 4:
            print("        Students are allowed to enrol in 4 subjects only")
            return

        subject_id = Subject.generate_unique_id({s.id for s in student.subjects})
        subject = Subject(id=subject_id)
        student.subjects.append(subject)
        self._save_student(student)

        print(f"        Enrolling in Subject-{subject.id}")
        print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")

    def remove_subject(self, student):
        """Remove a subject from the student's enrolment by subject ID."""
        if not student.subjects:
            print("        No subjects to remove")
            return

        subject_id = input("        Remove Subject by ID: ").strip()

        target = None
        for s in student.subjects:
            if s.id == subject_id:
                target = s
                break

        if target is None:
            print(f"        Subject {subject_id} not found")
            return

        student.subjects.remove(target)
        self._save_student(student)

        print(f"        Dropping Subject-{target.id}")
        print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")

    def show_subjects(self, student):
        """Display all subjects the student is currently enrolled in."""
        print(f"        Showing {len(student.subjects)} subjects")
        for subject in student.subjects:
            space = " " if subject.grade == "HD" else "  "
            print(f"        [ Subject::{subject.id} -- mark = {subject.mark} -- grade = {space}{subject.grade} ]")

    def change_password(self, student):
        """Prompt the student to set a new validated password."""
        print("        Updating Password")
        while True:
            new_password = input("        New Password: ").strip()
            if not re.match(self.PASSWORD_REGEX, new_password):
                print("        Incorrect password format")
                continue

            while True:
                confirm = input("        Confirm Password: ").strip()
                if confirm != new_password:
                    print("        Password does not match - try again")
                else:
                    break

            student.password = new_password
            self._save_student(student)
            print("        Password updated successfully")
            break

    def _save_student(self, student):
        """Persist the updated student object by replacing it in the full student list."""
        db = Database()
        students = db.load_students()
        for i, s in enumerate(students):
            if s.id == student.id:
                students[i] = student
                break
        db.save_students(students)
