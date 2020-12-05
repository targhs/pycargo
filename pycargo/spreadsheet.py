from openpyxl import Workbook, load_workbook

import inspect

from . import fields


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
            cell = sheet.cell(
                column=col, row=1, value=f"{headers[col-1]}"
            )
            cell.style = "Accent1"
        workbook.save(path)        
