from database import Database


# Grade display order: ascending by mark threshold (F, P, C, D, HD)
_GRADE_ORDER = ["F", "P", "C", "D", "HD"]


def _student_summary(student):
    """Return 'Name :: id --> GRADE:  grade - MARK: avg' for a student."""
    avg = student.get_average_mark()
    grade = student.get_grade()
    return (
        f"{student.name} :: {student.id} --> GRADE:  {grade} - MARK: {avg:.2f}"
    )


class AdminController:
    """Provides administrative operations: view, group, partition, remove, and clear students."""

    def admin_menu(self):
        """Display the admin system menu and dispatch to the chosen action."""
        while True:
            choice = input("        Admin System (c/g/p/r/s/x): ").strip()
            if choice == "c":
                self.clear_database()
            elif choice == "g":
                self.group_students()
            elif choice == "p":
                self.partition_students()
            elif choice == "r":
                self.remove_student()
            elif choice == "s":
                self.show_students()
            elif choice == "x":
                break
            else:
                print("        Invalid admin option")

    def show_students(self):
        """List all registered students with their ID and email."""
        print("        Student List")
        students = Database().load_students()
        if not students:
            print("                < Nothing to Display >")
            return
        for s in students:
            print(f"        {s.name} :: {s.id} --> Email: {s.email}")

    def group_students(self):
        """Group and display students by their current overall grade."""
        print("        Grade Grouping")
        students = Database().load_students()
        if not students:
            print("                < Nothing to Display >")
            return

        groups = {g: [] for g in _GRADE_ORDER}
        for s in students:
            groups[s.get_grade()].append(s)

        for grade in _GRADE_ORDER:
            group = groups[grade]
            if not group:
                continue
            pad = " " if grade == "HD" else "  "
            entries = ", ".join(_student_summary(s) for s in group)
            print(f"        {grade}{pad}--> [{entries}]")

    def partition_students(self):
        """Split students into PASS and FAIL groups and display each."""
        print("        PASS/FAIL Partition")
        students = Database().load_students()
        if not students:
            print("                < Nothing to Display >")
            return

        passing = [s for s in students if s.is_passing()]
        failing = [s for s in students if not s.is_passing()]

        fail_str = ", ".join(_student_summary(s) for s in failing) or "< none >"
        pass_str = ", ".join(_student_summary(s) for s in passing) or "< none >"

        print(f"        FAIL --> [{fail_str}]")
        print(f"        PASS --> [{pass_str}]")

    def remove_student(self):
        """Remove a student from the database by their student ID."""
        student_id = input("        Remove by ID: ").strip()
        db = Database()
        students = db.load_students()

        target = None
        for s in students:
            if s.id == student_id:
                target = s
                break

        if target is None:
            print(f"        Student {student_id} does not exist")
            return

        students.remove(target)
        db.save_students(students)
        print(f"        Removing Student {student_id} Account")

    def clear_database(self):
        """Prompt for confirmation then wipe all student records."""
        print("        Clearing students database")
        confirm = input("        Are you sure you want to clear the database (Y)ES/(N)O: ").strip()
        if confirm.upper() == "Y":
            Database().clear_students()
            print("        Students data cleared")
        # Any other input returns to admin menu
