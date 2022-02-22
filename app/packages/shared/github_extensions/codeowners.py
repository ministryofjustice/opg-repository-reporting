from github import Repository, UnknownObjectException
from ..logger import Out
from .rate_limiter import RateLimiter



def has_codeowners(repo:Repository.Repository, codeowners_file_path:str = "./CODEOWNERS") -> list:
    """Return true if CODEOWNERS is found to exist """

    RateLimiter.check()
    try:
        repo.get_contents(codeowners_file_path)
        Out.log(f"[{repo.full_name}] Found CODEOWNERS file")
        return True
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] No CODEOWNERS file")

    return False

