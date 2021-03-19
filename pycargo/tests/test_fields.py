import pytest

from .base import field_value_mappings
from pycargo import fields
from pycargo.exceptions import ValidationException


class TestField:
    @pytest.fixture
    def field(self):
        def _field(**kwargs):
            class FooField(fields.Field):
                def validate_type(self, val):
                    pass

            return FooField(**kwargs)

        return _field

    @pytest.fixture
    def always_passing_validator(self):
        def _always_passing_validator(val):
            pass

        return _always_passing_validator

    @pytest.fixture
    def always_failing_validator(self):
        def foo(val):
            raise ValidationException(f"Always raising error: {val}")

        return foo

    def test_data_key(self, field):
        sample_field = field(data_key="sample key")
        assert sample_field.data_key == "sample key"

    def test_comment(self, field):
        sample_field = field(comment="some comment")
        assert sample_field.comment == "some comment"

    def test_no_arguments(self, field):
        sample_field = field()
        assert sample_field.data_key == None
        assert sample_field.comment == None
        assert len(sample_field.validators) == 1

    def test_register_validators_with_validator(
        self, field, always_passing_validator
    ):
        fn = always_passing_validator
        sample_field = field(validate=fn)
        assert len(sample_field.validators) == 2
        assert sample_field.validators[1] == fn

    def test_register_validators_with_validators_list(
        self, field, always_passing_validator
    ):
        sample_field = field(
            validate=[
                always_passing_validator,
                always_passing_validator,
                always_passing_validator,
            ]
        )
        assert len(sample_field.validators) == 4

    def test_validations_with_no_error(self, field, always_passing_validator):
        f = field(
            validate=[always_passing_validator, always_passing_validator]
        )
        errors = f.validate("some value")
        assert errors == []

    def test_validations_with_errors(
        self, field, always_passing_validator, always_failing_validator
    ):
        f = field(
            validate=[
                always_passing_validator,
                always_failing_validator,
                always_failing_validator,
            ]
        )
        errors = f.validate("some value")
        assert errors == [
            "Always raising error: some value",
            "Always raising error: some value",
        ]


@pytest.fixture(params=field_value_mappings)
def foo(request):
    return request.param


def test_field_type_validation(foo):
    f = foo.Field()

    for val in foo.valid_values:
        assert f.validate_type(val) == None
