import pandas as pd

from pycargo.exceptions import ValidationException


class Validator:
    pass


class Required(Validator):
    def __init__(self, message: str = None):
        self.message = message or "Required field"

    def __call__(self, value):
        if pd.isnull(value):
            raise ValidationException(self.message)