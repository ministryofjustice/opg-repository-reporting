from datetime import date
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository
from shared.github_extensions.rate_limiter import rate_limiter
from shared.logger.out import out


def date_valid(merged_at:date, start:date, end:date):
    """See if the merged_date is between start & end and not None """
    return (merged_at != None) and (merged_at >= start and merged_at <= end)

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
    branch:str="main",
    counters:dict={}) -> dict:
    """
    """

    prs = pull_requests(repository, branch)
    i = 0
    t = prs.totalCount
    out.log(f"[{t}] pull requests for [{repository.full_name}] onto [{branch}]")

    pr:PullRequest

    for pr in prs:
        i = i + 1
        rate_limiter.check()
        valid = date_valid(pr.merged_at, start, end )
        out.debug(f"[{i}/{t}] PR for [{repository.full_name}][{branch}]@[{pr.merged_at}] is [{valid}]")
        if valid:
            monthYear = pr.merged_at.strftime('%Y-%m')
            counters[monthYear] += 1
        elif pr.merged_at != None and pr.merged_at < start:
            return counters

    return counters
