from pprint import pp
import pandas as pd
from github.MainClass import Github
from github.Organization import Organization
from github.Team import Team
from shared.github_extensions.init import init
from shared.github_extensions.pull_requests import pull_requests_in_date_counters
from shared.github_extensions.rate_limiter import rate_limiter
from shared.logger.out import out
from shared.folder import timestamp_directory
from releases import get_args
from releases.stub import erb

def main():
    path = timestamp_directory("releases")
    args = get_args()

    out.log(f"Releases between [{args.start}] and [{args.end}]")
    g:Github
    org:Organization
    team:Team
    g, org, team = init(args)

    rate_limiter.CONNECTION = g
    rate_limiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all_releases = []
    for r in repos:
        i = i + 1
        out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        rate_limiter.check()

        releases = pull_requests_in_date_counters(r, args.start, args.end)
        all_releases.append(releases)
        out.debug(releases)

        out.group_end()

    out.group_start("Output")
    df = pd.DataFrame(all_releases)
    df.to_markdown(f"{path}/report.md", index=False)
    df.to_html(f"{path}/report.html", index=False, border=0)

    out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    out.log(f"Generated reports here [{path}]")
    out.set_var("directory", path)
    out.group_end()

if __name__ == "__main__":
    main()
