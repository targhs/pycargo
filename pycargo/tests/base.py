from collections import namedtuple

from pycargo import fields


FieldValueMap = namedtuple("FieldValueMap", ["Field", "valid_values"])

field_value_mappings = [
    FieldValueMap(fields.StringField, ["valid"]),
    FieldValueMap(fields.IntegerField, [1]),
    FieldValueMap(fields.FloatField, [12.3]),
    FieldValueMap(
        fields.BooleanField, [True, False, 1, 0, "true", "false", "1", "0"]
    ),
    FieldValueMap(fields.DomainField, ["www.google.com"]),
    FieldValueMap(fields.EmailField, ["foo@bar.com"]),
    FieldValueMap(
        fields.UrlField,
        [
            "http://www.foo.com/",
            "https://www.foo.com",
            "http://foo.com",
            "https://foo.com",
        ],
    ),
]
