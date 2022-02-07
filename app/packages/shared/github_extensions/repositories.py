from typing import Callable
from github import Repository, Team
from ..logger import Out
from .rate_limiter import RateLimiter


def repositories(team:Team.Team, filter_function:Callable = None) -> tuple:
    """Return all repos into a standard list """

    Out.group_start("Fetching all repositories")
    RateLimiter.check()
    remote_repos = team.get_repos()
    # return 3 elements, everything, those that match filter, those that fail filter
    all_list:list(Repository.Repository) = []
    filtered_list:list(Repository.Repository) = []
    failed_filter_list:list(Repository.Repository) = []
    archived_list:list(Repository.Repository) = []
    i:int = 0
    total:int = remote_repos.totalCount
    for repo in remote_repos:
        i = i + 1
        RateLimiter.check()
        Out.log(f"[{i}/{total}] Repo [{repo.full_name}]")
        all_list.append(repo)
        # filter our archived ones
        if repo.archived is True:
            archived_list.append(repo)
        elif filter_function is not None:
            match = filter_function(repo)
            if match:
                filtered_list.append(repo)
            else:
                failed_filter_list.append(repo)

    Out.group_end()
    return all_list, filtered_list, failed_filter_list, archived_list
