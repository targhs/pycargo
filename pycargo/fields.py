from typing import Optional


class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validation
    """

    def __init__(self, required: bool = False):
        self.required = required

    def __str__(self):
        return f"<Field>"

    def __repr__(self):
        return f"<Field>"


class IntegerField(Field):
    def __str__(self):
        return f"<IntegerField>"

    def __repr__(self):
        return f"<IntegerField>"


class DateTimeField(Field):
    def __str__(self):
        return f"<DateTimeField>"

    def __repr__(self):
        return f"<DateTimeField>"


class StringField(Field):
    def __str__(self):
        return f"<StringField>"

    def __repr__(self):
        return f"<StringField>"
