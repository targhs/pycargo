from typing import List
from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment

import inspect

from pycargo import exceptions
from pycargo.types import IterableStrOrNone, IterableStr
from pycargo.styles import apply_style, header_style, required_header_style
from pycargo.fields import Field
from pycargo.classes import Cell, Row, Dataset


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

    def export_template(self, path: str, only: IterableStrOrNone = None):
        if only is None:
            only = self.fields

        fields = self.fields
        workbook = Workbook()
        sheet = workbook.active
        for idx, header in enumerate(only, start=1):
            cell = sheet.cell(column=idx, row=1, value=header)
            style = header_style
            comment_text = fields[header].comment
            if fields[header].required:
                style = required_header_style
            apply_style(cell, style)

            if comment_text:
                cell.comment = Comment(comment_text, author="")
        workbook.save(path)

    def load(self, path: str) -> Dataset:
        workbook = load_workbook(path)
        sheet = workbook.active
        rows = sheet.iter_rows(values_only=True)
        file_headers = next(rows)
        self._validate_headers(file_headers)

        data_rows = []
        for row in rows:
            cells = []
            for idx, value in enumerate(row):
                header = file_headers[idx]
                cells.append(Cell(header, value, self.fields[header]))
            data_rows.append(Row(cells))
        return Dataset(data_rows)

    def _validate_headers(self, headers: IterableStr):
        for header in headers:
            if header not in self.fields:
                raise exceptions.InvalidHeaderException(
                    f"Got unexpected field '{header}'"
                )
