from datetime import date
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository
from shared.github_extensions.rate_limiter import rate_limiter
from shared.logger.out import out


def date_valid(merged_at:date, start:date, end:date):
    """See if the merged_date is between start & end and not None """
    return (merged_at is not None) and (merged_at >= start and merged_at <= end)

def pull_requests(repository:Repository, branch:str) -> PaginatedList:
    """
    Wrapper around repository.get_pulls() to add rate limiting check
    """
    rate_limiter.check()
    return repository.get_pulls(
                        state='closed',
                        sort='merged_at',
                        direction='desc',
                        base=branch)



def pull_requests_in_date_counters(
    repository:Repository,
    start:date,
    end:date,
    counters:dict,
    branch:str="main") -> dict:
    """Create a dict of YYYY-MM keys counting the nubmer of merges in each month for this repo"""

    prs = pull_requests(repository, branch)
    i = 0
    total = prs.totalCount
    out.log(f"[{total}] pull requests for [{repository.full_name}] onto [{branch}]")

    pr:PullRequest

    for pr in prs:
        i = i + 1
        rate_limiter.check()
        valid = date_valid(pr.merged_at, start, end )
        out.debug(f"[{i}/{total}] PR for [{repository.full_name}][{branch}]@[{pr.merged_at}] is [{valid}]")
        if valid:
            month_year = pr.merged_at.strftime('%Y-%m')
            counters[month_year] += 1
        elif pr.merged_at is not None and pr.merged_at < start:
            return counters

    return counters
