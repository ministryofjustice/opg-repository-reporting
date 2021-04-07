import sys
import os
import json
import calendar
import time

import datetime
from github import Github
from github import RateLimitExceededException
import pandas as pd
import argparse
import pprint


from github_connection.github import github_connection
from rate_limiter.rate_limiter import rate_limiter
from search.tool import tool
from search.queries import queries
from search.api_code_search import api_code_search
from output.ouput import outputer
from dataframe.csv import dataframe_to_csv

pp = pprint.PrettyPrinter(indent=4)
spacer = '      '



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
