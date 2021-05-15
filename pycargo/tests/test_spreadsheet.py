from openpyxl.workbook import workbook
import pytest

from openpyxl import Workbook

from pycargo.spreadsheet import SpreadSheet
from pycargo.exceptions import InvalidFieldException, InvalidHeaderException
from pycargo import fields
from pycargo import validate


@pytest.fixture
def simple_field_spreadsheet():
    class Foo(SpreadSheet):
        name = fields.StringField()
        code = fields.IntegerField(data_key="Sample Code")

    return Foo


@pytest.fixture
def required_field():
    return fields.StringField(validate=[validate.Required])


@pytest.fixture
def non_required_field():
    return fields.StringField()


class TestSpreadSheetMeta:
    def test_has_fields(self, simple_field_spreadsheet):
        assert len(simple_field_spreadsheet().fields)

    def test_field_datatypes(self, simple_field_spreadsheet):
        class_fields = simple_field_spreadsheet().fields
        assert type(class_fields["name"]) == fields.StringField
        assert type(class_fields["code"]) == fields.IntegerField

    def test_data_key_mapping(self, simple_field_spreadsheet):
        mapping = simple_field_spreadsheet().data_key_mapping
        assert mapping["Sample Code"] == "code"
        assert mapping["name"] == "name"


class TestFieldsForExport:
    def test_all_fields_for_export(self, simple_field_spreadsheet):
        actual = simple_field_spreadsheet().get_fields_for_export().keys()
        expected = {"name", "code"}
        assert actual == expected

    def test_some_fields_for_export(self, simple_field_spreadsheet):
        actual = simple_field_spreadsheet().get_fields_for_export(["name"]).keys()
        expected = {"name"}
        assert actual == expected

    def test_invalid_field_for_export(self, simple_field_spreadsheet):
        with pytest.raises(InvalidFieldException) as excinfo:
            simple_field_spreadsheet().get_fields_for_export(
                ["name", "wrong field"]
            ).keys()
        assert "wrong field" in str(excinfo.value)


@pytest.fixture()
def required_field_spreadsheet():
    class Foo(SpreadSheet):
        name = fields.StringField(validate=[validate.Required()])
        code = fields.IntegerField(data_key="Sample Code")
        key = fields.IntegerField(validate=[validate.Range(min=30)])

    return Foo


class TestIsFieldRequired:
    def test_required_field(self, required_field_spreadsheet):
        actual = required_field_spreadsheet().is_field_required("name")
        expected = True
        assert actual == expected

    def test_non_required_field_without_validations(self, required_field_spreadsheet):
        actual = required_field_spreadsheet().is_field_required("code")
        expected = False
        assert actual == expected

    def test_non_required_field_with_validations(self, required_field_spreadsheet):
        actual = required_field_spreadsheet().is_field_required("key")
        expected = False
        assert actual == expected


class TestRequiredField:
    def test_valid_field_names(self, required_field_spreadsheet):
        actual = required_field_spreadsheet().required_fields()
        expected = ["name"]
        assert actual == expected

    def test_with_no_required_fields(self, simple_field_spreadsheet):
        actual = simple_field_spreadsheet().required_fields()
        expected = []
        assert actual == expected


class TestUnexpectedHeader:
    def test_with_unexpected_header(self, simple_field_spreadsheet):
        with pytest.raises(InvalidHeaderException) as excinfo:
            simple_field_spreadsheet().check_unexpected_fields(
                ["name", "code", "no valid"]
            )
        assert "no valid" in str(excinfo.value)

    def test_with_no_unexpected_header(self, simple_field_spreadsheet):
        simple_field_spreadsheet().check_unexpected_fields(["name", "code"])

    def test_with_no_header(self, simple_field_spreadsheet):
        simple_field_spreadsheet().check_unexpected_fields([])


class TestCheckRequiredField:
    def test_with_no_required_field(self, required_field_spreadsheet):
        with pytest.raises(InvalidHeaderException) as excinfo:
            required_field_spreadsheet().check_required_fields(["code", "key"])
        assert "Required field" in str(excinfo.value)

    def test_with_required_field(self, required_field_spreadsheet):
        required_field_spreadsheet().check_required_fields(["code", "key", "name"])

    def test_with_no_header(self, required_field_spreadsheet):
        with pytest.raises(InvalidHeaderException) as excinfo:
            required_field_spreadsheet().check_required_fields([])
        assert "Required field" in str(excinfo.value)


@pytest.fixture
def data_key_spreadsheet():
    class Foo(SpreadSheet):
        name = fields.StringField()
        code = fields.IntegerField(data_key="Sample Code")
        place = fields.StringField(data_key="place")

    return Foo


class TestDataKeys:
    def test_field_without_data_key(self, data_key_spreadsheet):
        actual = data_key_spreadsheet().get_field_name("name")
        expected = "name"
        assert actual == expected

    def test_field_with_data_key(self, data_key_spreadsheet):
        actual = data_key_spreadsheet().get_field_name("Sample Code")
        expected = "code"
        assert actual == expected

    def test_field_with_same_data_key(self, data_key_spreadsheet):
        actual = data_key_spreadsheet().get_field_name("place")
        expected = "place"
        assert actual == expected

    def test_invalid_field(self, data_key_spreadsheet):
        with pytest.raises(KeyError) as excinfo:
            data_key_spreadsheet().get_field_name("Invalid_key")
        assert "Invalid_key" in str(excinfo.value)


@pytest.fixture
def empty_workbook():
    return Workbook()


class TestWriteheaders:
    def test_headers(self, empty_workbook, simple_field_spreadsheet):
        workbook = empty_workbook
        sheet = workbook.active
        ss = simple_field_spreadsheet()
        ss.write_headers(sheet, ["name", "code"])
        assert sheet["A1"], sheet["B1"] == ("name", "Sample Code")

    def test_comments(self, empty_workbook, simple_field_spreadsheet):
        workbook = empty_workbook
        sheet = workbook.active
        ss = simple_field_spreadsheet()
        ss.write_headers(sheet, ["name", "code"])
        assert sheet["A1"], sheet["B1"] == ("name", "Sample Code")
