import inspect

from typing import Hashable, Type, Optional, Any

from .fields import Field


OptionalField = Optional[Type[Field]]


class Cell:
    """
    This represents as a cell in excel.
    Errors occured when validating do not raise exceptions,
    the are added to errors list.
    """

    def __init__(self, value: Any, field_type: OptionalField = None):
        self.value = value
        self.type = field_type
        self.errors = []
        self.validate()

    def __str__(self):
        return f"<Cell {self.value}>"

    def __repr__(self):
        return f"<Cell {self.value}>"

    def validate(self):
        # Check for required field
        if self.type.required and self.value is None:
            self.errors.append("Required field")

        # Check custom field validators
        for validator in self.type.validators:
            result = validator(self.value)
            if result:
                self.errors.append(result)


class Row:
    """
    This represents a single row of the dataset.
    Consists one or more cells.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            assert isinstance(v, Cell)
            setattr(self, k, v)

    def __str__(self):
        return f"<Row>"

    def __repr__(self):
        return f"<Row>"

    @property
    def errors(self) -> dict:
        cells = self.__dict__
        return {
            name: cell.errors for name, cell in cells.items() if cell.errors
        }


class Dataset:
    """
    Represents a container for the Rows.
    """

    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        return f"<Dataset({len(self.rows)})>"

    def __repr__(self):
        return f"<Dataset({len(self.rows)})>"

    def __getitem__(self, value: Hashable) -> Any:
        return self.rows[value]

    @property
    def errors(self) -> dict:
        return {
            idx: row.errors for idx, row in enumerate(self.rows) if row.errors
        }
