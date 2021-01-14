import typing

import pandas as pd
from openpyxl import Workbook
from openpyxl.comments import Comment

from pycargo import exceptions
from pycargo import utils
from pycargo.types import IterableStrOrNone, IterableStr
from pycargo.styles import apply_style, header_style, required_header_style
from pycargo.fields import Field
from pycargo.classes import RowIterator
from pycargo import validate


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

    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname} fields({utils.format_dict(self.fields)})>"

    @property
    def headers(self) -> typing.List:
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

            if self._is_field_required(header):
                style = required_header_style
            apply_style(cell, style)

            if comment_text:
                cell.comment = Comment(comment_text, author="")

    def _is_field_required(self, name: str) -> bool:
        field = self.fields[name]
        for validator in field.validators:
            if isinstance(validator, validate.Required):
                return True
        return False

    def export_template(self, path: str, only: IterableStrOrNone = None):
        self._write_headers(self.sheet, only)
        self.workbook.save(path)

    def load(self, path: str) -> None:
        df = pd.read_excel(path)
        self._validate_headers(df.columns)
        self.df = df.rename(columns=self.data_key_mapping)

    def rows(self):
        return RowIterator(self.df, self.fields)

    def _validate_headers(self, headers: IterableStr):
        for header in headers:
            if header not in self.data_key_mapping:
                raise exceptions.InvalidHeaderException(
                    f"Got unexpected field '{header}'"
                )
