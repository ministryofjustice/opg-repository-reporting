from github.Repository import Repository
import pandas as pd
from github.MainClass import Github
from github.Organization import Organization
from github.Team import Team
from shared.github_extensions.init import init
from shared.github_extensions.rate_limiter import RateLimiter
from shared.github_extensions.teams import teams_to_string
from shared.logger.out import Out
from shared.folder import timestamp_directory
from owners.args import get_args
from owners.stub import erb

def main():
    """Main function"""
    path = timestamp_directory("owners")
    args = get_args()

    Out.log("Repository ownership and meta data")
    g:Github
    org:Organization
    team:Team
    g, org, team = init(args)

    RateLimiter.CONNECTION = g
    RateLimiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all = []
    r:Repository
    for r in repos:
        i = i + 1
        Out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        RateLimiter.check()
        row = {
                'Repository': f"<a href='{r.html_url}'>{r.full_name}</a>",
                'Archived?': "Yes" if r.archived else "No",
                'Clone Traffic': r.get_clones_traffic()['count'],
                'Fork Count': r.forks_count,
                'Default Branch': r.default_branch,
                'Open Pull Requests': r.get_pulls(state='open', sort='created', base=r.default_branch).totalCount,
                'Last Commit Date to Default': r.get_branch(r.default_branch).commit.commit.committer.date,
                'Ownership': teams_to_string(r, args.team_slug, args.exclude)
            }
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
