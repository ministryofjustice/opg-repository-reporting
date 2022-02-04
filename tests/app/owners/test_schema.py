import unittest
from app import Schema

class TestSchema(unittest.TestCase):
    """TestSchema"""
    
    def test_versions_found_correctly(self):
        """ Make sure versions in the file dir are found """
        versions = Schema.versions()
        self.assertGreater(len(versions.keys()), 0)
        
    def test_get_returns_correctly(self):
        """Test .get call with real version"""
        found:dict = Schema.get("v0.0.1")
        self.assertIsNotNone(found)
        self.assertIsInstance(found, dict)
        self.assertTrue(found.get('$id', False))
        
    def test_valid(self):
        """ test .valid"""
        valid:bool = Schema.valid({"$schema": "v0.0.1", "owners": ["test"]})
        self.assertTrue(valid)
