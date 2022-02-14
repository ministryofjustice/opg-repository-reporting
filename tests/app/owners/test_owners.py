import unittest
from github.Repository import Repository
from parameterized import parameterized
from app.packages import Ownership


repo_name_prefix:str = 'ministryofjustice'

class TestOwnership(unittest.TestCase):
    """TestOwnership"""

    @parameterized.expand([
        ("small-valid-repo-set", [
            {
                'repo': Repository(None, {}, {'html_url': "opg-lpa"}, True ),
                'metadata': {
                    'owners': ["make-an-lpa"],
                    "dependencies": ["opg-data-lpa"]
                }
            },
            {
                'repo': Repository(None, {}, {'html_url': "opg-use-an-lpa"}, True ),
                'metadata': {
                    'owners': ["use-an-lpa"],
                    "dependencies": [
                        "opg-pdf-service",
                        "opg-data-lpa",
                        "opg-data-lpa-codes"
                    ]
                }
            },
            {
                'repo': Repository(None, {}, {'html_url': "opg-pdf-service"}, True ),
                'metadata': { 'owners': ["use-an-lpa"]}
            }
            
        ], 2)
    ])
    def test_add_owner_count(self, name:str, repos_with_metadata:list, owner_count:int):
        """Test .add """
        report:Ownership = Ownership()
        for repo_meta in repos_with_metadata:
            report.add( repo_meta.get('repo'), repo_meta.get('metadata') )
        # number of owners and number of keys should match owner count
        self.assertEqual(owner_count, len(report.owners))
        self.assertEqual(owner_count, len(report.owner_repositories.keys()))