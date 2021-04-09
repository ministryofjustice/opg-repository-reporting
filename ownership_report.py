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
from output.ouput import outputer
from dataframe.csv import dataframe_to_csv
from dataframe.markdown import dataframe_to_markdown

from ownership.convertors import for_output
from ownership.ownership_data import ownership_data

# main class
class ownership_report(github_connection):
    dataframe_handler = None
    exclusions = None

    def __init__(self, organization_slug, team_slug, dataframe_handler, exclusions):
        super().__init__( organization_slug=organization_slug, team_slug=team_slug )
        self.dataframe_handler = dataframe_handler
        self.exclusions = exclusions
        return


    # main function body
    def generate(self):
        # using dataframe
        out = outputer(for_output, self.dataframe_handler.save)
        # get the team repos
        print('---------------------------')
        print('Getting team {} repos'.format(self.team_slug))
        print('---------------------------')

        get_and_set_repos = self.get_and_set_team_repos
        api_runner = rate_limiter(self.g)
        api_runner.run(get_and_set_repos)

        total = self.team_repos.totalCount
        # now loop over all the repos
        x = 1
        for repo in self.team_repos:
            print('[{}/{}] {}'.format(x, total, repo.name))
            data = ownership_data(repo)
            # use rate limiter to fetch the data
            api_runner.run(data.get_data, out.output)
            # create a row to add to dataframe
            row = {
                'Repository': "[{name}]({url})".format(
                    name = repo.name,
                    url = repo.html_url),
                'Archived?': "Yes" if repo.archived else "No",
                'Clone Traffic': data.clones['count'],
                'Fork Count': data.forks_count,
                'Default Branch': data.default_branch,
                'Open Pull Requests': data.open_pull_requests.totalCount,
                'Last Commit Date to Default': data.commit_date,
                'Ownership': data.teams_as_string(self.team_slug, self.exclusions)
            }
            # add to dataframe
            out.append(repo.full_name, row)
            x += 1
            print('---------------------------')
        out.output()
        return


def main():
    parser = argparse.ArgumentParser(description='Generate a report of what teams own which repositories based on root organization and team.')

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
                            default="ownership_report",
                            help="Name of the file to save results to (excluding extension)" )

    parser.add_argument("--exclude",
                            default="",
                            help="List of team names to exclude from the ownership listing.")

    args = parser.parse_args()
    filename = args.filename

    # create the dataframe handler
    if args.type == "csv":
        df = dataframe_to_csv(filename)
    else:
        df = dataframe_to_markdown(filename)

    report = ownership_report(args.organization, args.team, df, args.exclude)
    report.generate()
    return

if __name__ == "__main__":
    main()
