import pytest
import pycargo

from pycargo.spreadsheet import SpreadSheet
from pycargo.exceptions import InvalidFieldException
from pycargo import fields


@pytest.fixture
def simple_field_spreadsheet():
    class Foo(SpreadSheet):
        name = fields.StringField()
        code = fields.IntegerField(data_key="Sample Code")

    return Foo


def test_has_fields(simple_field_spreadsheet):
    assert len(simple_field_spreadsheet.fields)


def test_field_datatypes(simple_field_spreadsheet):
    class_fields = simple_field_spreadsheet.fields
    assert type(class_fields["name"]) == fields.StringField
    assert type(class_fields["code"]) == fields.IntegerField


def test_data_key_mapping(simple_field_spreadsheet):
    mapping = simple_field_spreadsheet.data_key_mapping
    assert mapping["Sample Code"] == "code"
    assert mapping["name"] == "name"


def test_all_fields_for_export(simple_field_spreadsheet):
    actual = simple_field_spreadsheet().get_fields_for_export().keys()
    expected = {"name", "code"}
    assert actual == expected


def test_some_fields_for_export(simple_field_spreadsheet):
    actual = simple_field_spreadsheet().get_fields_for_export(["name"]).keys()
    expected = {"name"}
    assert actual == expected


def test_invalid_field_for_export(simple_field_spreadsheet):
    with pytest.raises(InvalidFieldException) as excinfo:
        simple_field_spreadsheet().get_fields_for_export(
            ["name", "wrong field"]
        ).keys()
    assert "wrong field" in str(excinfo.value)
