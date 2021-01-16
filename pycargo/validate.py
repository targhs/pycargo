import typing
import pandas as pd

from pycargo.exceptions import ValidationException


class Validator:
    def __repr__(self) -> str:
        args = self._repr_args()
        args = "{},".format(args) if args else ""
        return f"<{self.__class__.__name__}({args})>"

    def _repr_args(self) -> str:
        return ""


class Required(Validator):
    default_message = "Required field"

    def __init__(self, error: str = None):
        self.error = error or self.default_message

    def _format_error(self, value) -> str:
        return self.error

    def __call__(self, value) -> None:
        if pd.isnull(value):
            raise ValidationException(self.error)


class Range(Validator):
    message_min = "Must be {min_op} {{min}}."
    message_max = "Must be {max_op} {{max}}."
    message_all = "Must be {min_op} {{min}} and {max_op} {{max}}."

    message_gte = "greater than or equal to"
    message_gt = "greater than"
    message_lte = "less than or equal to"
    message_lt = "less than"

    def __init__(
        self,
        min: int = None,
        max: int = None,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        error: typing.Optional[str] = None,
    ):
        self.min = min
        self.max = max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.error = error

        self.message_min = self.message_min.format(
            min_op=self.message_gte if self.min_inclusive else self.message_gt
        )
        self.message_max = self.message_max.format(
            max_op=self.message_lte if self.max_inclusive else self.message_lt
        )
        self.message_all = self.message_all.format(
            min_op=self.message_gte if self.min_inclusive else self.message_gt,
            max_op=self.message_lte if self.max_inclusive else self.message_lt,
        )

    def _repr_args(self) -> str:
        return (
            f"min={self.min!r}, "
            f"max={self.max!r}, "
            f"min_inclusive={self.min_inclusive!r}, "
            f"max_inclusive={self.max_inclusive!r}"
        )

    def _format_error(self, value: typing.Any, message: str) -> str:
        return (self.error or message).format(
            input=value, min=self.min, max=self.max
        )

    def __call__(self, value: typing.Any):
        if self.min is not None and (
            value < self.min if self.min_inclusive else value <= self.min
        ):
            message = (
                self.message_min if self.max is None else self.message_all
            )
            raise ValidationException(self._format_error(value, message))

        if self.max is not None and (
            value > self.max if self.max_inclusive else value >= self.max
        ):
            message = (
                self.message_max if self.min is None else self.message_all
            )
            raise ValidationException(self._format_error(value, message))


class Equal(Validator):

    default_message = "Must be equal to {other}"

    def __init__(
        self,
        comparable,
        error: typing.Optional[str] = None,
    ):
        self.comparable = comparable
        self.error = error or self.default_message

    def _repr_args(self) -> str:
        return f"comparable={self.comparable!r}"

    def _format_error(self, value):
        return self.error.format(value=value, other=self.comparable)

    def __call__(self, value):
        if value != self.comparable:
            raise ValidationException(self._format_error(value))


class OneOf(Validator):
    default_message = "Must be one of {choices}"

    def __init__(
        self, choices: typing.Iterable, error: typing.Optional[str] = None
    ):
        self.choices = choices
        self.error = error or self.default_message

    def _repr_args(self) -> str:
        return f"choices={self.choices!r}"

    def _format_error(self, value) -> str:
        return self.error.format(choices=self.choices, value=value)

    def __call__(self, value):
        try:
            if value not in self.choices:
                raise ValidationException(self._format_error(value))
        except TypeError as err:
            raise ValidationException(self._format_error(value)) from err


class NoneOf(Validator):
    default_message = "Must be none of {iterable}"

    def __init__(
        self, iterable: typing.Iterable, error: typing.Optional[str] = None
    ):
        self.iterable = iterable
        self.error = error or self.default_message

    def _repr_args(self) -> str:
        return f"iterable={self.iterable!r}"

    def _format_error(self, value: typing.Any) -> str:
        return self.error.format(iterable=self.iterable, value=value)

    def __call__(self, value):
        try:
            if value in self.iterable:
                raise ValidationException(self._format_error(value))
        except TypeError as err:
            raise ValidationException(self._format_error(value)) from err
