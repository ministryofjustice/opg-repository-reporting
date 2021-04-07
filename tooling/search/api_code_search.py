
spacer = '      '

# handles calls to the api for the repo & query passed
# using the rate_limiter
class api_code_search:
    g = None
    key = None
    query = None
    category = None
    search_results = None
    store = {}
    res = None
    found = False
    i = 0
    def __init__(self, g, query, i):
        self.i = i
        self.g = g
        self.key = self.generate_key(query)
        self.category = query['category']
        self.query = query.copy()
        if 'category' in self.query: self.query.pop('category')
        # create the data store for the results
        self.store = {
            'Tool': self.query['query'],
            'Category': self.category,
            'Key': self.key,
            'Repository': self.query['repo'],
            'Locations': []
        }
        return
    # runs the initial api call - compatible with rate limiter
    def run(self):
        print (spacer+'[{}] Search - query: {} file: {} path: {}'.format(
            str(self.i).zfill(2),
            self.query['query'].ljust(14),
            self.query['filename'].ljust(24) if 'filename' in self.query else "",
            self.query['path'].ljust(12) if 'path' in self.query else ""
        ))

        self.search_results = self.g.search_code( **self.query )
        self.itr = iter(self.search_results)
        return True, True
    # create a key string
    def generate_key(self, q):
        return '::'.join(q.values())

    # process results
    def results(self):
        while True:
            try:
                self.res = next(self.itr)
                path = self.res.path
                print(spacer+spacer+'Result location: ' + path)
                self.store['Locations'].append(path)
            except StopIteration:
                break
        # final found check
        self.found = ( len(self.store['Locations']) > 0 )
        return True, True
