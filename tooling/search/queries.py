
from .tool import tool
# queries generates the code_search dict for use in
# calling the github api
class queries:
    tools = [
        # unit testing
        # expand for ide file
        tool("phpunit",
            tool.category_and_locations.append({
                'filename': 'phpunixml', 'category': 'ide'
            })
        ),

        # code scanning
        tool("php-cs-fixer"),
        tool("phpstan"),
        # expand for ide file
        tool("psalm",
            tool.category_and_locations.append({
                'filename': 'psalm.xml', 'category': 'ide'
            })
        ),
        tool("flake8"),

        # test runners
        tool("behat"),
        tool("cypress"),
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