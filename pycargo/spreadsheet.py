from openpyxl import Workbook, load_workbook

import inspect

from . import fields
from .classes import Cell, Row, Dataset


class SpreadSheetMeta(type):
    def __new__(cls, name, bases, dict_):
        class_ = type.__new__(cls, name, bases, dict_)
        class_.fields = {
            field_name: field_value
            for field_name, field_value in dict_.items()
            if isinstance(field_value, fields.Field)
        }
        return class_


class SpreadSheet(metaclass=SpreadSheetMeta):
    @property
    def headers(self):
        headers = [name for name, field in self.fields.items()]
        return headers

    def export_template(self, path: str):
        headers = self.headers
        workbook = Workbook()
        sheet = workbook.active

        for col in range(1, len(headers) + 1):
            cell = sheet.cell(column=col, row=1, value=f"{headers[col-1]}")
            cell.style = "Accent1"
        workbook.save(path)

    def load(self, path: str) -> Dataset:
        workbook = load_workbook(path)
        sheet = workbook.active
        rows = sheet.iter_rows(values_only=True)
        file_headers = next(rows)

        data_rows = []
        for row in rows:
            cells = []
            for idx, value in enumerate(row):
                header = file_headers[idx]
                cells.append(Cell(header, value, self.fields[header]))
            data_rows.append(Row(cells))
        return Dataset(data_rows)