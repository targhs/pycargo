from openpyxl import Workbook, load_workbook

import inspect

from . import fields
from .classes import Cell, Row, Dataset


class SpreadSheet:
    def __init__(self):
        self._register_fields()

    def _register_fields(self):
        members = inspect.getmembers(self)
        self.fields = {
            name: value
            for name, value in members
            if isinstance(value, fields.Field)
        }

    @property
    def headers(self):
        headers = [name for name, field in self.fields.items()]
        headers.reverse()
        return headers

    def export_template(self, path):
        headers = self.headers
        workbook = Workbook()
        sheet = workbook.active

        for col in range(1, len(headers) + 1):
            cell = sheet.cell(column=col, row=1, value=f"{headers[col-1]}")
            cell.style = "Accent1"
        workbook.save(path)

    def load(self, path):
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