from datetime import datetime
from typing import Optional, Union, List, Callable, Any
import validators

from pycargo.exceptions import ValidationException


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
        data_key: Optional[str] = None,
    ):
        self.required = required
        self.comment = comment
        self.data_key = data_key
        self.validators = []
        self._register_validators(validate)
        self._creation_index = Field._creation_index
        Field._creation_index += 1

    def __repr__(self):
        comment = f"'{self.comment}'" if self.comment else None
        return (
            f"<fields.{self.__class__.__name__}"
            f"(data_key='{self.data_key}', "
            f"comment={comment})>"
        )

    def _register_validators(self, validate):
        self.validators.append(self.validate_type)

        if validate:
            if callable(validate):
                self.validators.append(validate)
            elif isinstance(validate, list):
                self.validators.extend(validate)

    def validate_type(self):
        raise NotImplementedError

    def validate(self, value):
        errors = []
        for validator in self.validators:
            error = validator(value)
            if error:
                errors.append(error)
        return errors


class IntegerField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, int) and value is not None:
            raise ValidationException("Value must be integer")


class DateTimeField(Field):
    def validate_type(self, value: Any):
        if not isinstance(value, datetime):
            raise ValidationException(f"{value} not a valid datetime")


class StringField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, str) and value is not None:
            raise ValidationException("Value must be string")


class FloatField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, float) and value is not None:
            raise ValidationException("Value must be float")


class BooleanField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if isinstance(value, str):
            value = value.lower()
        if value not in ("true", "1", 1, "false", "0", 0):
            raise ValidationException(f"{value} is not a valid boolean value")


class DomainField(StringField):
    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.domain(value)
        if not valid:
            raise ValidationException("Invalid domain value")


class EmailField(StringField):
    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.email(value)
        if not valid:
            raise ValidationException("Invalid email")


class UrlField(StringField):
    def validate_type(self, value: Any) -> OptionalString:
        valid = validators.url(value)
        if not valid:
            raise ValidationException("Invalid url")
