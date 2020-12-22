import inspect

from typing import Type, Optional, Any

from .fields import Field

OptionalField = Optional[Type[Field]]


class Cell:
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
        if self.type.required and self.value is None:
            self.errors.append("Required field")

        for validator in self.type.validators:
            result = validator(self.value)
            if result:
                self.errors.append(result)


class Row:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            assert isinstance(v, Cell)
            setattr(self, k, v)

    def __str__(self):
        return f"<Row>"

    def __repr__(self):
        return f"<Row>"

    def get_cells(self):
        members = inspect.getmembers(self)
        return members
        
    @property
    def errors(self) -> dict:
        cells = self.__dict__
        return {name: cell.errors for name, cell in cells.items() if cell.errors}


class Dataset:
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        return f"<Dataset({len(self.rows)})>"

    def __repr__(self):
        return f"<Dataset({len(self.rows)})>"

    def __getitem__(self, value):
        return self.rows[value]

    @property
    def errors(self) -> dict:
        return {
            idx: row.errors for idx, row in enumerate(self.rows) if row.errors
        }
