
# tool
class tool:
    name = None
    category_and_locations = [
        {'filename': 'Makefile', 'category': 'makefile'},
        {'filename': '.pre-commit-config.yaml', 'category': 'pre-commit'},
        {'filename': 'Jenkinsfile', 'category': 'pipeline'},
        {'filename': '*.yml', 'path': '.circleci' ,'category': 'pipeline'},
        {'filename': '*.yml', 'path': '.github' ,'category': 'pipeline'},
    ]

    def __init__(self, name, category_and_locations=None):
        self.name = name
        if category_and_locations != None:
            self.category_and_locations = category_and_locations
        return
