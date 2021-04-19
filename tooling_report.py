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

from tooling.search.tool import tool
from tooling.search.queries import queries
from tooling.search.api_code_search import api_code_search
from tooling.convertors import for_output

from github_connection.github import github_connection
from rate_limiter.rate_limiter import rate_limiter
from output.ouput import outputer
from dataframe.csv import dataframe_to_csv
from dataframe.markdown import dataframe_to_markdown

pp = pprint.PrettyPrinter(indent=4)
spacer = '      '



# main class
class tooling_report(github_connection):
    dataframe_handler = None

    def __init__(self, organization_slug, team_slug, dataframe_handler):
        super().__init__( organization_slug=organization_slug, team_slug=team_slug )
        self.dataframe_handler = dataframe_handler
        return

    # main function body
    def generate(self):
        # conversion and save
        out = outputer(for_output, self.dataframe_handler.save)
        # get the team repos
        print('---------------------------')
        print('Getting team {} repos'.format(self.team_slug))
        print('---------------------------')
        get_and_set_repos = self.get_and_set_team_repos
        api_runner = rate_limiter(self.g)
        api_runner.run(get_and_set_repos)
        # top level elements on the queries that never change
        query_set = queries()
        for_api = query_set.for_api()
        length = len(for_api)
        total = self.team_repos.totalCount
        # now loop over all the repos
        x = 1
        for repo in self.team_repos:
            found = False
            # loop over each query
            print('[{}/{}] {}'.format(x, total, repo.name))
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

            print('---------------------------\n\n')
            x += 1
        #
        out.output()
        return


def main():
    parser = argparse.ArgumentParser(description='Generate a report of tools found within each repository owned by the team & organization.')

    # github org & team
    parser.add_argument("--organization",
                            default="ministryofjustice",
                            help="Set the orginisation to query against" )

    parser.add_argument("--team",
                            default="opg",
                            help="Set the team to fetch repositories from" )
    # determine if we output as csv or markdown from the dataframe
    parser.add_argument("--type",
                            default="csv",
                            choices=["csv", "md"],
                            help="Output as either a csv or a markdown file (default to csv)"
                        )
    # pick the location to save the report
    parser.add_argument("--filename",
                            default="tooling_report",
                            help="Name of the file to save results to (excluding extension)" )


    args = parser.parse_args()
    filename = args.filename

    # create the dataframe handler
    if args.type == "csv":
        df = dataframe_to_csv(filename)
    else:
        df = dataframe_to_markdown(filename)

    report = tooling_report(args.organization, args.team, df)
    report.generate()
    return

if __name__ == "__main__":
    main()
