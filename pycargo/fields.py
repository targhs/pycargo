import re
from typing import Optional, Union, List, Callable

import validators

# Types
FuncOrFuncList = Optional[Union[List[Callable], Callable]]

# Fields
class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validation
    """

    _creation_index = 0  # For sorting

    def __init__(
        self, required: bool = False, validate: FuncOrFuncList = None
    ):
        self.required = required
        self._register_validators(validate)
        self._creation_index = Field._creation_index
        Field._creation_index += 1

    def __str__(self):
        return f"<Field>"

    def __repr__(self):
        return f"<Field>"

    def _register_validators(self, validate):
        self.validators = [self.validate_type]

        if validate:
            if callable(validate):
                self.validators.append(validate)
            elif isinstance(validate, list):
                self.validators + validate

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


class BooleanField(Field):
    def __str__(self):
        return f"<BooleanField>"

    def __repr__(self):
        return f"<BooleanField>"

    def validate_type(self, value):
        if isinstance(value, str):
            value = value.lower()
        if value not in ("true", "1", 1, "false", "0", 0):
            return f"{value} is not a valid boolean value"


class DomainField(StringField):
    def __str__(self):
        return f"<DomainField>"

    def __repr__(self):
        return f"<DomainField>"

    def validate_type(self, value):
        valid = validators.domain(value)
        if not valid:
            return "Invalid domain value"


class EmailField(StringField):
    def __str__(self):
        return f"<EmailField>"

    def __repr__(self):
        return f"<EmailField>"

    def validate_type(self, value):
        valid = validators.email(value)
        if not valid:
            return "Invalid email"


class UrlField(StringField):
    def __str__(self):
        return f"<UrlField>"

    def __repr__(self):
        return f"<UrlField>"

    def validate_type(self, value):
        valid = validators.url(value)
        if not valid:
            return "Invalid url"