from typing import Optional


class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validatin
    """

    def __init__(self, required: bool = False):
        self.required = required


class IntegerField(Field):
    pass


class DateTimeField(Field):
    pass


class StringField(Field):
    pass