from github import Repository, UnknownObjectException
from ..logger import Out
from .rate_limiter import RateLimiter


def has_metafiles(repo:Repository.Repository, meta_file:str = "./metadata.json") -> list:
    """Return true if meta_file is found to exist """

    RateLimiter.check()
    try:
        repo.get_contents(meta_file)
        Out.log(f"[{repo.full_name}] Found metafile")
        return True
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] No metafile")

    return False