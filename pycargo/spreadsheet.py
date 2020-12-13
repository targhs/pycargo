from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment

import inspect

from .fields import Field
from .classes import Cell, Row, Dataset


class SpreadSheetMeta(type):
    def __new__(cls, name, bases, dict_):
        fields = {
            field_name: field_value
            for field_name, field_value in dict_.items()
            if isinstance(field_value, Field)
        }
        for f in fields:
            del dict_[f]
        class_ = type.__new__(cls, name, bases, dict_)
        class_.fields = fields
        return class_


class SpreadSheet(metaclass=SpreadSheetMeta):
    @property
    def headers(self):
        headers = [name for name, field in self.fields.items()]
        return headers

    def export_template(self, path: str):
        fields = self.fields
        workbook = Workbook()
        sheet = workbook.active

        for idx, header in enumerate(fields, start=1):
            cell = sheet.cell(column=idx, row=1, value=header)
            cell.style = "Accent1"
            comment_text = fields[header].comment
            if comment_text:
                cell.comment = Comment(comment_text, author="")
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