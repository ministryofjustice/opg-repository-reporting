from pprint import pp
import pandas as pd

from github import Github, Organization, Team, Repository
from shared import init, RateLimiter, protected_default_branch, out, timestamp_directory
from meta import get_args, erb


def main():
    path = timestamp_directory("meta")
    args = get_args()

    out.log(f"Repository meta data")
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
        out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        RateLimiter.check()
        row = {
                'Repository': f"<a href='{r.html_url}'>{r.full_name}</a>",
                'Archived?': "Yes" if r.archived else "No",
                'Default Branch': r.default_branch,
                'Default Branch Protection?': "Yes" if protected_default_branch(r) else "No",
                'Vulnerability Alerts Enabled?': "Yes" if r.get_vulnerability_alert() else "No",
                'Open Pull Requests': r.get_pulls(state='open', sort='created', base=r.default_branch).totalCount,
                'Clone Traffic': r.get_clones_traffic()['count'],
                'Fork Count': r.forks_count,
                'Last Commit Date to Default': r.get_branch(r.default_branch).commit.commit.committer.date
            }
        out.log(f"Repository [{r.full_name}] archived [{r.archived}] last commit [{row.get('Last Commit Date to Default', None)}]")
        out.debug(row)
        all.append(row)
        out.group_end()

    out.group_start("Output")

    all = sorted(all, key=lambda p: p['Repository'])
    df = pd.DataFrame(all)
    df.to_markdown(f"{path}/report.md", index=False)
    df.to_html(f"{path}/report.html", index=False, border=0)

    out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    out.log(f"Generated reports here [{path}]")
    out.set_var("directory", path)
    out.group_end()

if __name__ == "__main__":
    main()
