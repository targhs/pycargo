from typing import List, Type
from openpyxl import Workbook, load_workbook, workbook, worksheet
from openpyxl.comments import Comment

from pycargo import exceptions
from pycargo.types import IterableStrOrNone, IterableStr
from pycargo.styles import apply_style, header_style, required_header_style
from pycargo.fields import Field
from pycargo.classes import Cell, Row, Dataset


class SpreadSheetMeta(type):
    def __new__(cls, name, bases, dict_):
        """Add all the Fields of the spreadsheet
        into the fields attribute and remove their references
        Also creates a data_key_mapping attribute that
        keeps a mapping of data_key of the field and their
        actual names
        """
        fields = {
            field_name: field_value
            for field_name, field_value in dict_.items()
            if isinstance(field_value, Field)
        }
        class_ = type.__new__(cls, name, bases, dict_)
        class_.fields = fields
        class_.data_key_mapping = {}
        for key, value in fields.items():
            del dict_[key]
            class_.data_key_mapping[value.data_key or key] = key
        return class_


class SpreadSheet(metaclass=SpreadSheetMeta):
    def __init__(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    @property
    def headers(self) -> List:
        headers = [name for name, field in self.fields.items()]
        return headers

    def get_field_name(self, name: str) -> str:
        return self.data_key_mapping[name]

    def _write_headers(self, sheet, only: IterableStrOrNone = None):
        all_fields = self.fields
        if only is None:
            fields = self.fields
        else:
            fields = {
                field_name: all_fields[field_name] for field_name in only
            }

        for idx, header in enumerate(fields, start=1):
            value = fields[header].data_key or header
            cell = sheet.cell(column=idx, row=1, value=value)
            style = header_style
            comment_text = fields[header].comment
            if fields[header].required:
                style = required_header_style
            apply_style(cell, style)

            if comment_text:
                cell.comment = Comment(comment_text, author="")

    def export_template(self, path: str, only: IterableStrOrNone = None):
        self._write_headers(self.sheet, only)
        self.workbook.save(path)

    def load(self, path: str) -> Type[Dataset]:
        workbook = load_workbook(path)
        sheet = workbook.active
        rows = sheet.iter_rows(values_only=True)
        file_headers = next(rows)
        self.data = self._load_rows(rows, file_headers)
        return self.data

    def _load_rows(self, rows, headers: IterableStr) -> Type[Dataset]:
        self._validate_headers(headers)
        data_rows = []
        for row in rows:
            cells = {}
            for idx, value in enumerate(row):
                header = self.get_field_name(headers[idx])
                cells[header] = Cell(value, self.fields[header])
            data_rows.append(Row(**cells))
        return Dataset(data_rows)

    def _validate_headers(self, headers: IterableStr):
        for header in headers:
            if header not in self.data_key_mapping:
                raise exceptions.InvalidHeaderException(
                    f"Got unexpected field '{header}'"
                )
