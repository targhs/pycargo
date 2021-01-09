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
    def __init__(self, message: str = None):
        self.message = message or "Required field"

    def _repr_args(self) -> str:
        return f"message='{self.message}'"

    def __call__(self, value) -> None:
        if pd.isnull(value):
            raise ValidationException(self.message)
