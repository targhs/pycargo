from datetime import datetime
from typing import Optional, Union, List, Callable, Any

import validators

# Types
FuncOrFuncList = Optional[Union[List[Callable], Callable]]
OptionalString = Optional[str]


# Fields
class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validation
    """

    _creation_index = 0  # For sorting

    def __init__(
        self,
        required: bool = False,
        validate: FuncOrFuncList = None,
        comment: Optional[str] = None,
        data_key: Optional[str] = None
    ):
        self.required = required
        self.comment = comment
        self.data_key = data_key
        self._register_validators(validate)
        self._creation_index = Field._creation_index
        Field._creation_index += 1

    def __str__(self):
        return "<Field>"

    def __repr__(self):
        return "<Field>"

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
        return "<IntegerField>"

    def __repr__(self):
        return "<IntegerField>"

    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, int) and value is not None:
            return "Value must be integer"


class DateTimeField(Field):
    def __str__(self):
        return "<DateTimeField>"

    def __repr__(self):
        return "<DateTimeField>"

    def validate_type(self, value: Any):
        if not isinstance(value, datetime):
            return f"{value} not a valid datetime"


class StringField(Field):
    def __str__(self):
        return "<StringField>"

    def __repr__(self):
        return "<StringField>"

    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, str) and value is not None:
            return "Value must be string"


class FloatField(Field):
    def __str__(self):
        return "<FloatField>"

    def __repr__(self):
        return "<FloatField>"

    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, float) and value is not None:
            return "Value must be float"


class BooleanField(Field):
    def __str__(self):
        return "<BooleanField>"

    def __repr__(self):
        return "<BooleanField>"

    def validate_type(self, value: Any) -> OptionalString:
        if isinstance(value, str):
            value = value.lower()
        if value not in ("true", "1", 1, "false", "0", 0):
            return f"{value} is not a valid boolean value"


class DomainField(StringField):
    def __str__(self):
        return "<DomainField>"

    def __repr__(self):
        return "<DomainField>"

    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.domain(value)
        if not valid:
            return "Invalid domain value"


class EmailField(StringField):
    def __str__(self):
        return "<EmailField>"

    def __repr__(self):
        return "<EmailField>"

    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.email(value)
        if not valid:
            return "Invalid email"


class UrlField(StringField):
    def __str__(self):
        return "<UrlField>"

    def __repr__(self):
        return "<UrlField>"

    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.url(value)
        if not valid:
            return "Invalid url"
