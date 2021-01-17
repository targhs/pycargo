from typing import Optional, Union, List, Callable, Any

import validators
import pandas as pd
import numpy as np

from pycargo.exceptions import ValidationException


# Types
FuncOrFuncList = Optional[Union[List[Callable], Callable]]
OptionalString = Optional[str]


# Fields
class Field:
    """
    Base class for fields. Includes all the required
    attributes and methods for validation.
    data_key is the external representation of the Field which
    is used at the time of export and import.
    """

    _creation_index = 0  # For sorting

    def __init__(
        self,
        validate: FuncOrFuncList = None,
        comment: Optional[str] = None,
        data_key: Optional[str] = None,
    ):
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

    def _register_validators(self, validate: Union[List[Callable], Callable]):
        """Method to set self.validators for the
        field.
        """
        self.validators.append(self.validate_type)
        if validate:
            if callable(validate):
                self.validators.append(validate)
            elif isinstance(validate, list):
                self.validators.extend(validate)

    def validate_type(self):
        """Method to be overriden by other fields
        that checks the type of the field and
        should raise ValidationException if the
        type check fails.
        """
        raise NotImplementedError

    def validate(self, value: Any) -> List:
        """Method to check value against
        the validators and return list of errors
        """
        errors = []
        for validator in self.validators:
            error = validator(value)
            if error:
                errors.append(error)
        return errors


class IntegerField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, np.int64):
            raise ValidationException("Value must be integer")


class DateTimeField(Field):
    def validate_type(self, value: Any):
        if not isinstance(value, pd.Timestamp):
            raise ValidationException(f"{value} not a valid datetime")


class DateField(Field):
    def validate_type(self, value: Any):
        if not isinstance(value, pd.Timestamp):
            raise ValidationException(f"{value} not a valid date")

        for v in [value.hour, value.minute, value.second]:
            if v != 0:
                raise ValidationException(
                    f"{value} is a datetiem and not date."
                )


class StringField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, str):
            raise ValidationException("Value must be string")


class FloatField(Field):
    def validate_type(self, value: Any) -> OptionalString:
        if not isinstance(value, float):
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
