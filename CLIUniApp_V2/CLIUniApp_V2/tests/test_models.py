import unittest
from unittest.mock import patch

from models.student import Student
from models.subject import Subject


class TestStudentModel(unittest.TestCase):
    def test_generate_unique_id_avoids_duplicates(self):
        with patch("models.student.random.randint", side_effect=[1, 1, 2]):
            unique_id = Student.generate_unique_id({"000001"})
            self.assertEqual(unique_id, "000002")

    def test_to_from_dict_round_trip(self):
        student = Student("Alice Smith", "alice.smith@university.com", "Password123", id="000123")
        student.subjects.append(Subject(id="001", mark=90))

        restored = Student.from_dict(student.to_dict())

        self.assertEqual(restored.id, student.id)
        self.assertEqual(restored.name, student.name)
        self.assertEqual(restored.email, student.email)
        self.assertEqual(len(restored.subjects), 1)
        self.assertEqual(restored.subjects[0].mark, 90)

    def test_is_passing_and_grade_boundaries(self):
        student = Student("Test Student", "test.user@university.com", "Password123", id="000124")
        student.subjects = [Subject(id="001", mark=49), Subject(id="002", mark=51)]

        self.assertTrue(student.is_passing())
        self.assertEqual(student.get_grade(), "P")


class TestSubjectModel(unittest.TestCase):
    def test_generate_unique_id_avoids_duplicates(self):
        with patch("models.subject.random.randint", side_effect=[1, 1, 2]):
            unique_id = Subject.generate_unique_id({"001"})
            self.assertEqual(unique_id, "002")

    def test_grade_calculation(self):
        self.assertEqual(Subject(mark=90).grade, "HD")
        self.assertEqual(Subject(mark=80).grade, "D")
        self.assertEqual(Subject(mark=70).grade, "C")
        self.assertEqual(Subject(mark=60).grade, "P")
        self.assertEqual(Subject(mark=40).grade, "F")
