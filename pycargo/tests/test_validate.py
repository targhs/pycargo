import pytest

from pycargo import validate
from pycargo.exceptions import ValidationException


class TestRequired:
    def test_none_value(self):
        with pytest.raises(ValidationException):
            validator = validate.Required()
            validator(None)

    def test_not_none_value(self):
        validator = validate.Required()
        validator("not none value")

    def test_none_value_with_custom_error_message(self):
        with pytest.raises(ValidationException) as excinfo:
            validator = validate.Required("This is required")
            validator(None)
        assert "This is required" in str(excinfo.value)


class TestEqual:
    def test_unequal_value(self):
        with pytest.raises(ValidationException):
            validator = validate.Equal(10)
            validator(12)

    def test_equal_value(self):
        validator = validate.Equal(10)
        validator(10)

    def test_custom_error_message(self):
        with pytest.raises(ValidationException) as excinfo:
            validator = validate.Equal(
                10, error="{value} is not equal to {other}."
            )
            validator(12)
        assert "12 is not equal to 10." in str(excinfo.value)


@pytest.fixture
def noneof_validator():
    return validate.NoneOf(
        [1, 2, 3, 4], error="{value} should not be in {iterable}."
    )


class TestNoneOf:
    def test_with_value_present(self, noneof_validator):
        with pytest.raises(ValidationException) as excinfo:
            noneof_validator(3)
        assert "3 should not be in [1, 2, 3, 4]." in str(excinfo.value)

    def test_with_value_not_present(self, noneof_validator):
        noneof_validator(6)

    def test_with_non_iterable(self):
        with pytest.raises(ValidationException):
            validator = validate.NoneOf(12)
            validator(7)


@pytest.fixture
def oneof_validator():
    return validate.OneOf(
        [1, 2, 3, 4], error="{value} should be in {choices}."
    )


class TestOneOf:
    def test_with_value_present(self, oneof_validator):
        oneof_validator(3)

    def test_with_value_not_present(self, oneof_validator):
        with pytest.raises(ValidationException) as excinfo:
            oneof_validator(6)
        assert "6 should be in [1, 2, 3, 4]." in str(excinfo.value)

    def test_with_non_iterable(self):
        with pytest.raises(ValidationException):
            validator = validate.OneOf(12)
            validator(7)


class TestRange:
    def test_min_with_inclusive_limit_and_lower_value(self):
        validator = validate.Range(min=10)
        with pytest.raises(ValidationException) as excinfo:
            validator(5)
        assert "Must be greater than or equal to 10." in str(excinfo.value)

    def test_min_with_inclusive_limit_and_equal_value(self):
        validator = validate.Range(min=10)
        validator(10)

    def test_min_with_inclusive_limit_and_higher_value(self):
        validator = validate.Range(min=10)
        validator(15)

    def test_max_with_inclusive_limit_and_lower_value(self):
        validator = validate.Range(max=10)
        validator(5)

    def test_max_with_inclusive_limit_and_equal_value(self):
        validator = validate.Range(max=10)
        validator(10)

    def test_max_with_inclusive_limit_and_higher_value(self):
        with pytest.raises(ValidationException) as excinfo:
            validator = validate.Range(max=10)
            validator(15)
        assert "Must be less than or equal to 10." in str(excinfo.value)

    def test_min_inclusive_max_inclusive(self):
        validator = validate.Range(min=10, max=20)
        validator(10)
        validator(20)
        validator(15)
        with pytest.raises(ValidationException) as excinfo:
            validator(5)
        assert (
            "Must be greater than or equal to 10 and less than or equal to 20."
            in str(excinfo.value)
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(25)

        assert (
            "Must be greater than or equal to 10 and less than or equal to 20."
            in str(excinfo.value)
        )

    def test_min_inclusive_max_exclusive(self):
        validator = validate.Range(min=10, max=20, max_inclusive=False)
        validator(10)
        validator(10)
        validator(19)

        with pytest.raises(ValidationException) as excinfo:
            validator(20)
        assert "Must be greater than or equal to 10 and less than 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(5)
        assert "Must be greater than or equal to 10 and less than 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(25)

        assert "Must be greater than or equal to 10 and less than 20." in str(
            excinfo.value
        )

    def test_min_exclusive_max_inclusive(self):
        validator = validate.Range(min=10, max=20, min_inclusive=False)
        validator(11)
        validator(20)

        with pytest.raises(ValidationException) as excinfo:
            validator(10)
        assert "Must be greater than 10 and less than or equal to 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(5)
        assert "Must be greater than 10 and less than or equal to 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(21)

        assert "Must be greater than 10 and less than or equal to 20." in str(
            excinfo.value
        )

    def test_min_exclusive_max_exclusive(self):
        validator = validate.Range(
            min=10, max=20, min_inclusive=False, max_inclusive=False
        )
        validator(11)
        validator(19)

        with pytest.raises(ValidationException) as excinfo:
            validator(10)
        assert "Must be greater than 10 and less than 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(20)
        assert "Must be greater than 10 and less than 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(5)
        assert "Must be greater than 10 and less than 20." in str(
            excinfo.value
        )

        with pytest.raises(ValidationException) as excinfo:
            validator(25)

        assert "Must be greater than 10 and less than 20." in str(
            excinfo.value
        )
