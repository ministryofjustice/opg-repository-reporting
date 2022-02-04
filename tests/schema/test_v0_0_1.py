import unittest
import pathlib
import json
from jsonschema import validate, ValidationError
from parameterized import parameterized

class TestV001(unittest.TestCase):
    """ Test the v0.0.1 schema """
    schema:dict

    def setUp(self):
        filepath:str = pathlib.Path(__file__).parent.parent.parent.joinpath("./schema/v0.0.1.json").resolve()
        file = open(filepath, 'r', encoding='utf-8')
        self.schema = json.load(file)
        file.close()


    @parameterized.expand([
        ("valid-only-owners", {"owners": ["test"] }),
        ("valid-owners-and-empty-dependencies", {"owners": ["test"], "dependencies": [] }),
        ("valid-owners-and-dependencies", {"owners": ["foo"], "dependencies": ["bar"] }),
        ("valid-extra-keys-ignored", {"owners": ["foo"], "dependencies": ["bar"], "ignore-me": "test" })
    ])
    def test_schema_against_valid_data(self, name:str, instance:dict):
        """ Check that valid data correctly validates """
        try:
            validate(instance=instance, schema=self.schema)
        except Exception:
            self.fail(f"Failed to validate data {name}")



    @parameterized.expand([
        ("missing-required", { "dependencies": ["OtherRepo"]} ),
        ("min-owners-not-met", { "owners": [] }),
        ("owners-should-be-array", { "owners": "foo" }),
        ("owners-invalid-type", { "owners": [1, 2] }),
        ("dependencies-invalid-type", { "owners": [1, 2], "dependencies": 1 }),
    ])
    def test_schema_against_invalid_data(self, name:str, bad_instance:dict):
        """ Check a series of incorrectly formatted data will throw errors """
        with self.assertRaises(ValidationError):
            print(f"validating {name}")
            validate(instance=bad_instance, schema=self.schema)
