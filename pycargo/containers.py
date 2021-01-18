from typing import Type, Optional, Any, Dict

import pandas as pd

from pycargo.exceptions import ValidationException
from pycargo.fields import Field


OptionalField = Optional[Type[Field]]
FieldsDict = Dict[str, Type[Field]]


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

    def __repr__(self):
        value = None if pd.isna(self.value) else self.value
        return f"<Cell {value}>"

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

    def __repr__(self):
        return f"<Row cells({self.cells})>"

    def __getitem__(self, key):
        return self.cells[key]

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


def get_row_obj(row_data: dict, fields: FieldsDict) -> Type[Row]:
    cells = {}
    for key in fields:
        cells[key] = Cell(row_data.get(key), fields[key])
    return Row(cells)


class RowIterator:
    def __init__(self, df: Type[pd.DataFrame], fields: dict):
        self.df = df
        self.fields = fields
        self.total_rows = len(df)

    def __repr__(self):
        return f"<RowIterator({self.total_rows})>"

    def __iter__(self):
        self.row = 0
        return self

    def __next__(self) -> Type[Row]:
        if self.row < self.total_rows:
            result = dict(self.df.iloc[self.row])
            self.row += 1
            return get_row_obj(result, self.fields)
        else:
            raise StopIteration
