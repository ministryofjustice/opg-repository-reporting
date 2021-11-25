from datetime import date
import dateutil.relativedelta
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository
from shared.logger.out import out
from shared.github_extensions.rate_limiter import rate_limiter


def date_valid(merged_at:date, start:date, end:date):
    return (merged_at != None) and (merged_at >= start and merged_at <= end)

def pull_requests(repository:Repository) -> PaginatedList:
    rate_limiter.check()
    return repository.get_pulls(
                        state='closed',
                        sort='merged_at',
                        direction='desc',
                        base=repository.default_branch)

def date_struct(start:date, end:date) -> dict:
    struct = {'Repository': ""}
    m = start
    out.debug(f"Creating struct for [{start}] [{end}]")
    while start <= end:
        key = start.strftime('%Y-%m')
        struct[key] = 0
        # increment the date by a month, but keep it to the 1st of the month
        start = start + dateutil.relativedelta.relativedelta(months=1)
        start = start.replace(day=1, hour=0, minute=0, second=0)
    return struct

def pull_requests_in_date_counters(repository:Repository, start:date, end:date) -> dict:
    """
    """
    counters = date_struct(start, end)
    link = f"<a href='{repository.html_url}'>{repository.full_name}</a>"
    counters.update({'Repository': link})
    prs = pull_requests(repository)
    i = 0
    t = prs.totalCount

    pr:PullRequest

    for pr in prs:
        i = i + 1
        rate_limiter.check()
        valid = date_valid(pr.merged_at, start, end )
        out.log(f"[{i}/{t}] PR for [{repository.full_name}]@[{pr.merged_at}] is [{valid}]")
        if valid:
            monthYear = pr.merged_at.strftime('%Y-%m')
            counters[monthYear] += 1
        elif pr.merged_at != None and pr.merged_at < start:
            return counters

    return counters
