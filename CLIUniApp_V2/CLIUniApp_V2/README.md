# CLIUniApp
A CLI university management system built in Python.

## Requirements
- Python 3.12+
- No external libraries needed

## How to Run
```
cd CLIUniApp
python3 main.py
```

## Storage
- Student data is stored in `database/students.json`.
- JSON storage avoids unsafe pickling and keeps the data portable.

## Tests
Run tests with:
```
python -m unittest discover -s tests
```

## Group Members and Contributions
- Member 1: models/student.py, models/subject.py
- Member 2: database/database.py, controllers/student_controller.py, controllers/subject_controller.py
- Member 3: controllers/admin_controller.py, main.py
