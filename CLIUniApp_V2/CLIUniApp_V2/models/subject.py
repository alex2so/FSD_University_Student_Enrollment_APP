import random


class Subject:
    """Represents a university subject with a random ID, mark, and computed grade."""

    ID_DIGITS = 3

    def __init__(self, id=None, mark=None):
        self.id = id or self.generate_id()
        self.mark = mark if mark is not None else random.randint(25, 100)
        self.grade = self._calculate_grade()

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
                raise ValueError("Unable to generate a unique subject ID")

    def _calculate_grade(self):
        """Return grade string based on mark using the standard grade scale."""
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >= 65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "F"

    def to_dict(self):
        return {"id": self.id, "mark": self.mark}

    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get("id"), mark=data.get("mark"))
