from typing import Hashable, Type, Optional, Any

import pandas as pd

from pycargo.exceptions import ValidationException
from pycargo.fields import Field


OptionalField = Optional[Type[Field]]


class Cell:
    """
    This represents as a cell in excel.
    Errors occured when validating do not raise exceptions,
    the are added to errors list.
    """

    def __init__(self, value: Any, field_type: OptionalField):
        self.value = value
        self.type = field_type
        self.errors = []
        self.validate()

    def __str__(self):
        return f"<Cell {self.value}>"

    def __repr__(self):
        return f"<Cell {self.value}>"

    def validate(self):
        for validator in self.type.validators:
            try:
                validator(self.value)
            except ValidationException as exc:
                self.errors.append(exc.message)


class Row:
    """
    This represents a single row of the dataset.
    Consists one or more cells.
    """

    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        return f"<Row>"

    def __repr__(self):
        return f"<Row>"

    @property
    def errors(self) -> dict:
        return {
            name: cell.errors
            for name, cell in self.cells.items()
            if cell.errors
        }

    def as_dict(self):
        data = {"errors": {}}
        for field_name, field_value in self.cells.items():
            data[field_name] = field_value.value
            if errors := field_value.errors:
                data["errors"][field_name] = errors
        return data


def get_row_obj(row_data, fields):
    cells = {}
    for key, value in row_data.items():
        cells[key] = Cell(value, fields[key])
    return Row(cells)


class RowIterator:
    def __init__(self, df, fields):
        self.df = df
        self.fields = fields
        self.total_rows = len(df)

    def __iter__(self):
        self.row = 0
        return self

    def __next__(self):
        if self.row < self.total_rows:
            result = dict(self.df.iloc[self.row])
            self.row += 1
            return get_row_obj(result, self.fields)
        else:
            raise StopIteration
