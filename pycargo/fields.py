from typing import Optional, Union, List, Callable


FuncOrFuncList = Optional[Union[List, Callable]]


class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validation
    """

    def __init__(
        self, required: bool = False, validate: FuncOrFuncList = None
    ):
        self.required = required
        self.validators = [self.validate_type]

        if validate:
            if callable(validate):
                self.validators.append(validate)
            elif isinstance(validate, list):
                self.validators + validate

    def __str__(self):
        return f"<Field>"

    def __repr__(self):
        return f"<Field>"

    def validate_type(self):
        raise NotImplementedError


class IntegerField(Field):
    def __str__(self):
        return f"<IntegerField>"

    def __repr__(self):
        return f"<IntegerField>"

    def validate_type(self, value):
        if not isinstance(value, int) and value is not None:
            return "Value must be integer"


class DateTimeField(Field):
    def __str__(self):
        return f"<DateTimeField>"

    def __repr__(self):
        return f"<DateTimeField>"

    def validate_type(self, value):
        return None


class StringField(Field):
    def __str__(self):
        return f"<StringField>"

    def __repr__(self):
        return f"<StringField>"

    def validate_type(self, value):
        if not isinstance(value, str) and value is not None:
            return "Value must be string"


class FloatField(Field):
    def __str__(self):
        return f"<FloatField>"

    def __repr__(self):
        return f"<FloatField>"

    def validate_type(self, value):
        if not isinstance(value, float) and value is not None:
            return "Value must be float"
