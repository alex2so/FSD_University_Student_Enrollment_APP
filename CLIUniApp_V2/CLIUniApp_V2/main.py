from controllers import StudentController, AdminController


def main():
    """Entry point: display the top-level university menu and route to admin or student system."""
    while True:
        choice = input("University System: (A)dmin, (S)tudent, or X : ").strip()
        if choice.upper() == "A":
            AdminController().admin_menu()
        elif choice.upper() == "S":
            StudentController().student_menu()
        elif choice.upper() == "X":
            print("Thank You")
            break
        else:
            print("Invalid top-level option")


if __name__ == "__main__":
    main()
