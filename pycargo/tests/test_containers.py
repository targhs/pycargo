from dataclasses import dataclass, field
from typing import Any, Optional

import pytest

from pycargo import containers
from pycargo.exceptions import ValidationException


@dataclass
class MockField:
    validators: list = field(default_factory=list)
    type: Optional[Any] = None


@dataclass
class MockCell:
    value: Any = None
    errors: list = field(default_factory=list)
    type: MockField = None


def is_equal_to_10(value):
    if value != 10:
        raise ValidationException("Should be equal to 10")


def always_raising_error(value):
    raise ValidationException("Error")


@pytest.fixture
def mock_field():
    return MockField(validators=[is_equal_to_10])


@pytest.fixture
def row_cells():
    return {
        "name": MockCell(errors=["some error"]),
        "code": MockCell(errors=["Invalid code", "Old code"]),
        "added_on": MockCell(errors=[]),
    }


class TestCell:
    def test_validate_with_no_validators(self):
        cell = containers.Cell(10, MockField(validators=[]))
        assert len(cell.errors) == 0

    def test_validate_with_errors(self, mock_field):
        cell = containers.Cell(20, mock_field)
        assert cell.errors[0] == "Should be equal to 10"

    def test_validate_with_no_errors(self, mock_field):
        cell = containers.Cell(10, mock_field)
        assert len(cell.errors) == 0


class TestRow:
    def test_errors(self, row_cells):
        r = containers.Row(row_cells)
        assert r.errors == {
            "name": ["some error"],
            "code": ["Invalid code", "Old code"],
        }

    def test_as_dict_with_erros(self):
        cells = {
            "code": MockCell(
                value=12, type=MockField(), errors=["not valid", "some error"]
            ),
            "name": MockCell(
                value="Some name", type=MockField(), errors=["this is invalid"]
            ),
        }
        row = containers.Row(cells)
        actual = row.as_dict()
        expected = {
            "code": 12,
            "name": "Some name",
            "errors": {
                "code": ["not valid", "some error"],
                "name": ["this is invalid"],
            },
        }
        assert actual == expected

    def test_as_dict_without_errors(self):
        cells = {
            "code": MockCell(
                value=12,
                type=MockField(),
            ),
            "name": MockCell(value="Some name", type=MockField()),
        }
        row = containers.Row(cells)
        actual = row.as_dict()
        expected = {
            "code": 12,
            "name": "Some name",
            "errors": {},
        }
        assert actual == expected


class TestGetRowObj:
    def test_with_same_keys(self):
        data = {"code": 1, "name": "Foo"}
        field_mapping = {
            "code": MockField(type=int),
            "name": MockField(type=str),
        }
        actual = containers.get_row_obj(data, field_mapping)
        assert actual.as_dict().keys() == {"code", "name", "errors"}

    def test_with_extra_data_key(self):
        data = {"code": 1, "name": "Foo", "extra_key": "extra value"}
        field_mapping = {
            "code": MockField(type=int),
            "name": MockField(type=str),
        }
        actual = containers.get_row_obj(data, field_mapping)
        assert actual.as_dict().keys() == {"code", "name", "errors"}

    def test_with_fewer_keys(self):
        data = {"code": 1, "name": "Foo"}
        field_mapping = {
            "code": MockField(type=int),
            "name": MockField(type=str),
            "status": MockField(type=str),
        }
        actual = containers.get_row_obj(data, field_mapping)
        assert actual.as_dict().keys() == {"code", "name", "status", "errors"}
