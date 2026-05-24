import random
from .subject import Subject


class Student:
    """Represents a university student with personal details and enrolled subjects."""

    ID_DIGITS = 6

    def __init__(self, name, email, password, id=None, subjects=None):
        self.id = id or self.generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects or []

    @classmethod
    def generate_id(cls):
        return str(random.randint(1, 10**cls.ID_DIGITS - 1)).zfill(cls.ID_DIGITS)

    @classmethod
    def generate_unique_id(cls, existing_ids=None):
        existing_ids = existing_ids or set()
        attempts = 0
        while True:
            candidate = cls.generate_id()
            if candidate not in existing_ids:
                return candidate
            attempts += 1
            if attempts > 1000000:
                raise ValueError("Unable to generate a unique student ID")

    def get_average_mark(self):
        """Return float average of all subject marks, or 0.0 if no subjects."""
        if not self.subjects:
            return 0.0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def get_grade(self):
        """Return grade string based on average mark using the standard grade scale."""
        avg = self.get_average_mark()
        if avg >= 85:
            return "HD"
        elif avg >= 75:
            return "D"
        elif avg >= 65:
            return "C"
        elif avg >= 50:
            return "P"
        else:
            return "F"

    def is_passing(self):
        """Return True if average mark is 50 or above."""
        return self.get_average_mark() >= 50

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [subject.to_dict() for subject in self.subjects],
        }

    @classmethod
    def from_dict(cls, data):
        subjects = [Subject.from_dict(item) for item in data.get("subjects", []) if isinstance(item, dict)]
        return cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
            id=data.get("id"),
            subjects=subjects,
        )
