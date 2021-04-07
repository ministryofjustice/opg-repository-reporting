import os
import json
import datetime
import pandas as pd
from github import Github

class github_report:

    organization = ''

    def __init__(self, organization):
        self.df = None
        self.organization = organization

        if 'GITHUB_TOKEN' not in os.environ:
            print('GITHUB_TOKEN must be set')
            exit(1)
        token = os.getenv('GITHUB_TOKEN', '')

        if token == '':
            print('GITHUB_TOKEN must have a value')
            exit(1)
        self.g = Github(token)
        self.org = self.g.get_organization(self.organization)
        return

    def get_team_repos(self, team):
        team = self.org.get_team_by_slug(team)
        return team.get_repos()

    def report_by_team(self, team):
        report_rows = []
        repos = self.get_team_repos(team)
        for repo in repos:
            clones = repo.get_clones_traffic(per="week")
            branch = repo.get_branch(repo.default_branch)
            commitDate = branch.commit.commit.committer.date
            open_pull_requests = repo.get_pulls(state='open', sort='created', base=repo.default_branch)

            teams = ""
            for t in repo.get_teams():
                # exclude these as they are default teams
                if t.name != "OPG" and t.name != "opg-webops":
                    teams =  "[{name}]({url}), {existing}".format(
                        name = t.name,
                        url = "https://github.com/orgs/ministryofjustice/teams/" + t.slug,
                        existing= teams)

            row = {
                'Name': "[{name}]({url})".format(
                    name = repo.name,
                    url = repo.html_url),
                'Archived?': "Yes" if repo.archived else "No",
                'Clone Traffic': clones['count'],
                'Fork Count': repo.forks_count,
                'Default Branch': repo.default_branch,
                'Open Pull Requests': open_pull_requests.totalCount,
                'Last Commit Date to Default': commitDate,
                'Ownership': teams.strip(", ")
            }
            report_rows.append(row)

        df = pd.DataFrame(report_rows, columns=['Name', 'Archived?', 'Clone Traffic', 'Fork Count', 'Default Branch', 'Open Pull Requests', 'Last Commit Date to Default', 'Ownership'])
        self.df = df
        return

    def output_as_markdown_page(self):
        if self.df is not None:
            df = self.df
            df.sort_values(by=['Name'], inplace=True)
            # front matter for the output
            date = datetime.datetime.now()
            front_matter = "---\ntitle: Repository Ownership\nlast_reviewed_on: {date}\nreview_in: 3 months\n---\n\n".format(date = date.strftime("%Y-%m-%d") )
            intro = "# <%= current_page.data.title %>\nListing of all our repositorys, team that owns them and their current status\n"
            notes = "\n\n### Notes\n\nThe list of repositories was generated via [this script](https://github.com/ministryofjustice/opg-org-infra/tree/main/github_report).\n\n"
            print(front_matter)
            print(intro)
            print(df.to_markdown(index=False))
            print(notes)
        else:
            print('Dataframe must be set')
            exit(1)
        return


def main():
    work = github_report('ministryofjustice')
    work.report_by_team('opg')
    work.output_as_markdown_page()

if __name__ == "__main__":
    main()
