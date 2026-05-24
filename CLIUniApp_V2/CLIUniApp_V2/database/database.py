import json
from pathlib import Path
from models import Student


class Database:
    """Handles persistent storage of Student objects using JSON serialization."""

    FILE_PATH = Path(__file__).resolve().parent / "students.json"

    def load_students(self):
        """Load and return the list of Student objects from disk.

        Returns an empty list if the file does not exist, is empty, or contains invalid JSON.
        """
        if not self.FILE_PATH.exists():
            return []
        try:
            raw = self.FILE_PATH.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, list):
                return []
            return [Student.from_dict(item) for item in data if isinstance(item, dict)]
        except (json.JSONDecodeError, OSError):
            return []

    def save_students(self, students):
        """Overwrite students.json with the full list of Student objects."""
        data = [student.to_dict() for student in students]
        self.FILE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def clear_students(self):
        """Overwrite students.json with an empty list."""
        self.FILE_PATH.write_text("[]", encoding="utf-8")
