import os
import sys
import json
import pandas as pd
import calendar
import time
import datetime
from github import Github
from github import RateLimitExceededException
import argparse
import pprint


pp = pprint.PrettyPrinter(indent=4)
spacer = '      '

# rate_limiter wrapper to handle the github api call limits
class rate_limiter:
    g = None
    remaining = 0
    rate_limit = None

    def __init__(self, g):
        self.g = g
        self.reset()
        return

    def reset(self):
        self.rate_limit = self.g.get_rate_limit()
        self.remaining = self.rate_limit.search.remaining
        print('>>>>> Api calls remaining: {}\n'.format(self.remaining))
        return
    # pause execution
    def pause(self):
        search_rate_limit = self.rate_limit.search
        reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
        # add 5 seconds to be sure the rate limit has been reset
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 2
        print('>>>>> Sleeping for {} seconds'.format(sleep_time) )
        time.sleep(sleep_time)

    # run
    def run(self, function, on_rate_limited=None, on_error=None, on_complete=None):
        while True:
            try:
                # if we have calls remaining, run the function
                if self.remaining > 0:
                    # returns a tripple of a boolean for complete,
                    # bool for status and a counter for number of calls made
                    complete, function_result = function()
                    # update the rate limit
                    r, limit = self.g.rate_limiting
                    self.remaining = r
                    # if complete, break the loop
                    if complete == True and on_complete != None:
                        on_complete(function_result)
                        break
                    elif complete == True:
                        break
                    # if theres an error, run that function
                    if function_result != True and errror_function != None:
                        on_error()

                # we've caught the rate limit error before making the call
                else:
                    print('\n>>>>> Rate limit hit 0')
                    if on_rate_limited != None:
                        on_rate_limited()
                    self.pause()
                    self.reset()
            # rate limit hit
            except RateLimitExceededException:
                print('\n>>>>> Rate limit exceeded')
                if on_rate_limited != None:
                    on_rate_limited()
                self.pause()
                self.reset()
            # breaks the loop
            except StopIteration:
                break
        # end the func
        return


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

# queries generates the code_search dict for use in
# calling the github api
class queries:
    tools = [
        # unit testing
        # expand for ide file
        tool("phpunit",
            tool.category_and_locations.append({
                'filename': 'phpunit.xml', 'category': 'ide'
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
        for t in self.tools:
            for q in t.category_and_locations:
                add = q.copy()
                add.update({'query': t.name})
                query_data.append(add)
        return query_data
    #

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

# github base helper class
class github_connection:
    g = None
    organization_slug = None
    team_slug = None
    team_repos = None
    org = None
    def __init__(self, organization_slug, team_slug):
        self.organization_slug = organization_slug
        self.team_slug = team_slug
        self.g = Github( self.get_github_token() )
        self.org = self.g.get_organization(self.organization_slug)
        return


    # get_github_token fetches env var or fails
    def get_github_token(self):
        if 'GITHUB_TOKEN' not in os.environ:
            print('GITHUB_TOKEN must be set')
            exit(1)
        token = os.getenv('GITHUB_TOKEN', '')
        if token == '':
            print('GITHUB_TOKEN must have a value')
            exit(1)
        return token

    # get_and_set_team_repos fetches the teams repos
    def get_and_set_team_repos(self):
        team = self.org.get_team_by_slug(self.team_slug)
        self.team_repos = team.get_repos()
        return True, True


# output class
class outputer:
    data_store = {}
    conversion_function = None
    save_function = None

    def __init__(self, conversion_function, save_function):
        self.conversion_function = conversion_function
        self.save_function = save_function
        return

    def append(self, key, values):
        self.data_store[key] = values
        return

    def output(self):
        if len(self.data_store) > 0:
            print('>>>>> Saving dataframe')
            convert = self.conversion_function
            processed = convert(self.data_store)
            save = self.save_function
            save(processed)
        else:
            print('>>>>> Nothing to save')
        return

# convert and save dataframe to csv
class dataframe_to_csv:
    filename = './report.csv'

    def convert(self, temporary_store):
        processed_results = []
        for key in temporary_store:
            item = temporary_store[key]
            # ony save if it has a location
            if len(item['Locations']) > 0:
                processed_results.append({
                    'Repository': item['Repository'].replace("ministryofjustice/", ""),
                    'Tool': item['Tool'] if 'Tool' in item else "",
                    'Category': item['Category'] if 'Category' in item else "",
                    'Locations': "\n".join(item['Locations'])
                })
        return processed_results

    def save(self, processed_results):
        if len(processed_results) > 0:
            df = pd.DataFrame(processed_results)
            if df is not None:
                df.sort_values(by=['Repository'], inplace=True)
                df.to_csv(self.filename, index=False)
        return

# main class
class tooling_report(github_connection):

    def __init__(self, organization_slug, team_slug):
        super().__init__( organization_slug=organization_slug, team_slug=team_slug )
        return

    # main function body
    def generate(self):
        # using dataframe -> to csv for this
        df = dataframe_to_csv()
        out = outputer(df.convert, df.save)
        # get the team repos
        print('---------------------------')
        print('Getting team repos')
        get_and_set_repos = self.get_and_set_team_repos
        api_runner = rate_limiter(self.g)
        api_runner.run(get_and_set_repos)
        # top level elements on the queries that never change
        query_set = queries()
        for_api = query_set.for_api()
        length = len(for_api)

        # now loop over all the repos
        x = 1
        for repo in self.team_repos:
            found = False
            # loop over each query
            print('============================\n{} [{}/{}]'.format(repo.name, x, self.team_repos.totalCount))
            print(spacer+ '{0} Queries to run:'.format(length) )
            i = 1
            for q in for_api:
                # insert the repo to search
                q.update({'repo': repo.full_name})
                # call the api and process the result data using the
                # api rate limter wrapper so we dont miss any details
                # - on rate limit, output the results so far
                searcher = api_code_search(self.g, q, i)
                api_runner.run(searcher.run, out.output)
                # iterating over the search result returned triggers the api call
                # so we need to wrap the location store
                # - on rate limit, output the results so far
                api_runner.run(searcher.results, out.output)
                # append the data to the dataoutput store
                out.append(searcher.key, searcher.store)
                # if theres a result, track we have something for this repo
                if searcher.found == True:
                    found = True
                # inc counter
                i += 1
            # if nothing has been found for this repo, we still need to add it to the output
            if found == False:
                print('\n❌ Not found: ' + repo.name)
                out.append(repo.name, {'Repository': repo.name, 'Locations':[""] } )
            else:
                print('\n✔ Found: '+ repo.name)

            print('-----------------------\n\n')
            x += 1
        #
        return


def main():
    report = tooling_report('ministryofjustice', 'opg')
    report.generate()
    return

if __name__ == "__main__":
    main()
