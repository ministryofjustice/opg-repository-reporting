import json
from github import Repository, UnknownObjectException
from ..logger import Out
from .rate_limiter import RateLimiter



def check_standard_files(repo:Repository.Repository) -> dict:
    """Check if the repo has standard expected files"""

    return {
        "CODE_OF_CONDUCT": has_file(repo, "./CODE_OF_CONDUCT.md"),
        "CODEOWNERS": has_file(repo, "./CODEOWNERS"),
        "CONTRIBUTING": has_file(repo, "./CONTRIBUTING.md"),
        "LICENCE": has_file(repo, "./LICENCE"),
        "METADATA": has_metafiles(repo),
        "README": has_file(repo, "./README.md"),
    }


def has_metafiles(repo:Repository.Repository) -> bool:
    """Return true if meta_file is found to exist """
    metadata_file_path:str = "./metadata.json"
    return has_file(repo, metadata_file_path)


def has_file(repo:Repository.Repository, file_path:str) -> bool:
    """Return true if file_path is found to exist """

    RateLimiter.check()
    try:
        repo.get_contents(file_path)
        Out.log(f"[{repo.full_name}] Found [{file_path}] file")
        return True
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] No [{file_path}] file")

    return False


def metadata(repo:Repository.Repository) -> dict:
    """Returns either the contents of the metadata file, or empty dict"""
    metadata_file_path:str = "./metadata.json"
    data:dict = {}

    try:
        data = json.loads( repo.get_contents(metadata_file_path).decoded_content)
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] Failed to fetch metadata file")
    return data