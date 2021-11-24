import pandas as pd
from github.MainClass import Github
from github.Organization import Organization
from github.Team import Team
from shared.github_extensions.init import init
from shared.github_extensions.dependencies import dependencies
from shared.github_extensions.rate_limiter import rate_limiter
from shared.logger.out import out
from shared.folder import timestamp_directory
from dependencies import get_args

def main():
    path = timestamp_directory()
    args = get_args()

    out.log(f"Dependency data")
    g:Github
    org:Organization
    team:Team
    g, org, team = init(args)

    rate_limiter.CONNECTION = g
    rate_limiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all = []
    for r in repos:
        i = i + 1
        out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        rate_limiter.check()

        d = dependencies()
        dep, s = d.get(args.organisation_slug, team, r, args.organisation_token)

        out.log(f"[{r.full_name}] Found [{len(dep)}] packages within [{len(s)}] sources")
        all.extend(dep)

        out.group_end()

    df = pd.DataFrame(all)
    df.to_html(f"{path}/report.v1.0.0.html", index=False, border=0)
    out.group_start("Output")
    out.log(f"Generated reports here [{path}]")
    out.set_var("generated_report_directory", path)
    out.group_end()

if __name__ == "__main__":
    main()
