
from . import tool as t
# queries generates the code_search dict for use in
# calling the github api
class queries:
    tools = [
        # unit testing
        # expand for ide file
        t.tool("phpunit",
            t.tool.category_and_locations.append({
                'filename': 'phpunit.xml', 'category': 'ide'
            })
        ),

        # code scanning
        t.tool("php-cs-fixer"),
        t.tool("phpstan"),
        # expand for ide file
        t.tool("psalm",
            t.tool.category_and_locations.append({
                'filename': 'psalm.xml', 'category': 'ide'
            })
        ),
        t.tool("flake8"),

        # test runners
        t.tool("behat"),
        t.tool("cypress"),
    ]
    # convert structure to a dict
    def for_api(self):
        query_data= []
        for item in self.tools:
            for q in item.category_and_locations:
                add = q.copy()
                add.update({'query': item.name})
                query_data.append(add)
        return query_data
    #
