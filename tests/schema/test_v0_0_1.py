from pprint import pp
import unittest
import pathlib
import json
from jsonschema import validate, ValidationError
from parameterized import parameterized

class Test_V0_0_1(unittest.TestCase):
    schema:dict

    def setUp(self):
        filepath:str = pathlib.Path(__file__).parent.parent.parent.joinpath("./schema/v0.0.1.json").resolve()
        file = open(filepath)
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
        except Exception as e:
            self.fail("Failed to validate data")



    @parameterized.expand([
        ("missing-required", { "dependencies": ["OtherRepo"]} ),
        ("min-owners-not-met", { "owners": [] }),
        ("owners-should-be-array", { "owners": "foo" }),
        ("owners-invalid-type", { "owners": [1, 2] }),
        ("dependencies-invalid-type", { "owners": [1, 2], "dependencies": 1 }),
    ])
    def test_schema_against_invalid_data(self, name:str, bad_instance:dict):
        """ Check a series of incorrectly formatted data will throw errors """
        with self.assertRaises(ValidationError) as context:
            validate(instance=bad_instance, schema=self.schema)
