import sys
import os
import json
import calendar
import time

import datetime
import dateutil.relativedelta

from github import Github
from github import RateLimitExceededException
import pandas as pd
import argparse
import pprint

from github_connection.github import github_connection
from rate_limiter.rate_limiter import rate_limiter
from output.ouput import outputer
from dataframe.csv import dataframe_to_csv
from dataframe.markdown import dataframe_to_markdown

from mergers.convertors import for_output
from mergers.pull_requests import pull_requests

pp = pprint.PrettyPrinter(indent=4)
spacer = '      '



# main class
class merge_report(github_connection):
    dataframe_handler = None
    start_date = None
    end_date = None
    default_date_structure = {}

    def __init__(self, organization_slug, team_slug, dataframe_handler, start_date, end_date):
        super().__init__( organization_slug=organization_slug, team_slug=team_slug )
        self.dataframe_handler = dataframe_handler
        self.start_date = start_date
        self.end_date = end_date

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
        # totals & counters
        total = self.team_repos.totalCount
        x = 1
        # loop over each repo and find details
        for repo in self.team_repos:
            print('[{}/{}] {}'.format(x, total, repo.name))
            # create the pr class
            pr = pull_requests(repo, self.start_date, self.end_date)
            # run via the limiter, with grouping running after
            api_runner.run(pr.get, out.output)
            api_runner.run(pr.group, out.output)
            # add the results
            out.append(repo.name, pr.structure)
            print('---------------------------')
            x += 1
        #
        out.output()
        return


def main():
    # date handling
    now = datetime.datetime.utcnow()
    start = now - dateutil.relativedelta.relativedelta(months=6)
    start = start.replace(day=1, hour=0, minute=0, second=0)

    parser = argparse.ArgumentParser(description='Generate a report of merges to the default branch - grouped by month - by repo.')
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
                            default="merge_counts",
                            help="Name of the file to save results to (excluding extension)" )

    # start & end date of the report
    parser.add_argument("--start",
                            type=datetime.date.fromisoformat,
                            default=start,
                            help="Set the start date for this report (default: {})".format(start.strftime("%Y-%m-%d"))  )
    parser.add_argument("--end",
                            type=datetime.date.fromisoformat,
                            default=now,
                            help="Set the end date for this report (default: {})".format(now.strftime("%Y-%m-%d")) )



    args = parser.parse_args()
    filename = args.filename
    # convert to a datetime for consistency
    start_date = datetime.datetime(args.start.year, args.start.month, args.start.day)
    end_date = args.end
    # create the dataframe handler
    if args.type == "csv":
        df = dataframe_to_csv(filename)
    else:
        df = dataframe_to_markdown(filename)

    report = merge_report(args.organization, args.team, df, start_date, end_date)
    report.generate()
    return

if __name__ == "__main__":
    main()
