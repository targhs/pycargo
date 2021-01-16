import typing

import pandas as pd
from openpyxl import Workbook
from openpyxl.workbook.workbook import Worksheet
from openpyxl.comments import Comment

from pycargo import exceptions
from pycargo import utils
from pycargo.types import IterableStrOrNone, IterableStr
from pycargo.styles import (
    Style,
    apply_style,
    header_style,
    required_header_style,
)
from pycargo.fields import Field
from pycargo.containers import RowIterator
from pycargo import validate


class SpreadSheetMeta(type):
    def __new__(cls, name, bases, dict_):
        """Add all the Fields of the spreadsheet
        into the fields attribute and remove their references
        Also creates a data_key_mapping attribute that
        keeps a mapping of data_key of the field and their
        actual names.
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
        pass

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"<{classname} fields({utils.format_dict(self.fields)})>"

    def _get_fields_for_export(
        self, field_names: IterableStr = None
    ) -> typing.Dict[str, typing.Type[Field]]:
        """Method to return fields for exporting
        as template header. If None is passed as
        field_names then all the fields are exported
        else it returns a dictionary of field_names and
        field objects
        """
        all_fields = self.fields
        if field_names is None:
            return self.fields
        return {
            field_name: all_fields[field_name] for field_name in field_names
        }

    def _get_header_style(self, field_name: str) -> typing.Type[Style]:
        """Header styles differ depending upon the field is
        required or not. By default, required fields are
        exported with a red background and optional fields
        have a green background.
        """
        if self._is_field_required(field_name):
            return required_header_style
        return header_style

    def _write_headers(
        self, sheet: typing.Type[Worksheet], only: IterableStrOrNone = None
    ) -> None:
        """Method to write headers to the excel file.
        It takes a sheet object and a field names to write.
        This also applies the header styles and add comments
        to the headers if any.
        """
        fields = self._get_fields_for_export(only)
        for idx, header in enumerate(fields, start=1):
            value = fields[header].data_key or header
            cell = sheet.cell(column=idx, row=1, value=value)
            apply_style(cell, self._get_header_style(header))
            comment_text = fields[header].comment
            if comment_text:
                cell.comment = Comment(comment_text, author="")

    def _is_field_required(self, name: str) -> bool:
        """Checks whether the field is required or not.
        A field is required if it has validate.Required validator.
        """
        field = self.fields[name]
        for validator in field.validators:
            if isinstance(validator, validate.Required):
                return True
        return False

    def _required_fields(self) -> typing.List[str]:
        """Method to return field names of required fields"""
        return [
            field_name
            for field_name in self.fields
            if self._is_field_required(field_name)
        ]

    def _validate_headers(self, headers: IterableStr) -> None:
        self._check_unexpected_fields(headers)
        self._check_required_fields(headers)

    def _check_unexpected_fields(self, headers: IterableStr) -> None:
        """Method to check if any unexpected header is given in
        the excel. Raises InvalidHeaderException it finds any.
        """
        for header in headers:
            if header not in self.fields:
                raise exceptions.InvalidHeaderException(
                    f"Got unexpected field '{header}'"
                )

    def _check_required_fields(self, headers: IterableStr) -> None:
        """Check whether all the required fields are provided
        in the excel sheet or not. If a required field is missing,
        raise InvalidHeaderException.
        """
        data_key_mapping_alt = {
            name: data_key for data_key, name in self.data_key_mapping.items()
        }
        for field_name in self._required_fields():
            if field_name not in headers:
                raise exceptions.InvalidHeaderException(
                    f"Required field "
                    f"'{data_key_mapping_alt[field_name]}' not given"
                )

    @property
    def headers(self) -> typing.List:
        headers = [name for name, field in self.fields.items()]
        return headers

    def get_field_name(self, name: str) -> str:
        """Field objects have data_key which is the external
        representation of field's name. This data_key is used
        as the header name in output and input of excel files.

        Method takes the external representation name 'data_key'
        and returns the actual name of the field.
        """
        return self.data_key_mapping[name]

    def export_template(
        self, path: str, only: IterableStrOrNone = None
    ) -> None:
        """Export template as excel file for the user to
        the given path. field names given in only are exported
        to the file.
        """
        workbook = Workbook()
        sheet = workbook.active
        self._write_headers(sheet, only)
        workbook.save(path)

    def load(self, path: str) -> None:
        """Load data from the excel file to dataframe.
        Also rename the dataframe's headers from their external
        representations to their actual field names.
        File headers are also validated on load.
        """
        df = pd.read_excel(path)
        self.df = df.rename(columns=self.data_key_mapping)
        self._validate_headers(self.df.columns)

    def rows(self) -> typing.Type[RowIterator]:
        """This can be used for iterating over the loaded rows.
        Rows are lazy loaded i.e they aren't loaded till the time they
        are accessed.
        """
        return RowIterator(self.df, self.fields)
