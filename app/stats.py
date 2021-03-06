from itertools import count
import pandas as pd

from github import Github, Organization, Team, Repository
from packages import init, RateLimiter, protected_default_branch, Out, timestamp_directory, check_standard_files
from packages.stats import get_args, erb


def main():
    """ Main function """
    path = timestamp_directory("stats")
    args = get_args()

    Out.log("Repository stats data")
    g:Github
    org:Organization.Organization
    team:Team.Team
    g, org, team = init(args)

    RateLimiter.CONNECTION = g
    RateLimiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all = []
    r:Repository.Repository
    for r in repos:
        i = i + 1
        Out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        RateLimiter.check()
        
        row = {
            'Repository': f"<a href='{r.html_url}'>{r.full_name}</a>",
            'Archived?': "Yes" if r.archived else "No",
            'Default Branch': r.default_branch,
            'Default Branch Protection?': "Yes" if protected_default_branch(r) else "No",
            }
        # get standard file checks (readme etc) add those in to the stats
        standard_files = check_standard_files(r)
        for name,exists in standard_files.items():
            row.update({f"Has {name}?": "Yes" if exists is True else "No"})

        row.update({
            'Vulnerability Alerts Enabled?': "Yes" if r.get_vulnerability_alert() else "No",
            'Open Pull Requests': r.get_pulls(state='open', sort='created', base=r.default_branch).totalCount,
            'Clone Traffic': r.get_clones_traffic()['count'],
            'Fork Count': r.forks_count,
            'Last Commit Date to Default': r.get_branch(r.default_branch).commit.commit.committer.date,
            'Has Webhooks?': "Yes" if r.get_hooks().totalCount > 0 else "No"

        })

        Out.log(f"Repository [{r.full_name}] archived [{r.archived}] last commit [{row.get('Last Commit Date to Default', None)}]")
        Out.debug(row)
        all.append(row)
        Out.group_end()

    Out.group_start("Output")

    all = sorted(all, key=lambda p: p['Repository'])
    df = pd.DataFrame(all)
    df.to_markdown(f"{path}/report.md", index=False)
    df.to_html(f"{path}/report.html", index=False, border=0)

    Out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    Out.log(f"Generated reports here [{path}]")
    Out.set_var("directory", path)
    Out.group_end()

if __name__ == "__main__":
    main()
