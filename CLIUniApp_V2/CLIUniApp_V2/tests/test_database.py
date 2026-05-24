import tempfile
import unittest
from pathlib import Path

from database.database import Database
from models.student import Student
from models.subject import Subject


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name) / "students.json"
        self.original_path = Database.FILE_PATH
        Database.FILE_PATH = self.test_path
        self.database = Database()

    def tearDown(self):
        Database.FILE_PATH = self.original_path
        self.temp_dir.cleanup()

    def test_save_and_load_students(self):
        student = Student("Alice Smith", "alice.smith@university.com", "Password123", id="000123")
        student.subjects.append(Subject(id="001", mark=90))

        self.database.save_students([student])
        loaded_students = self.database.load_students()

        self.assertEqual(len(loaded_students), 1)
        self.assertEqual(loaded_students[0].id, student.id)
        self.assertEqual(loaded_students[0].subjects[0].mark, 90)

    def test_clear_students_writes_empty_list(self):
        self.database.save_students([])
        self.database.clear_students()

        self.assertEqual(self.test_path.read_text(encoding="utf-8"), "[]")

    def test_load_invalid_json_returns_empty(self):
        self.test_path.write_text("not valid json", encoding="utf-8")
        self.assertEqual(self.database.load_students(), [])
