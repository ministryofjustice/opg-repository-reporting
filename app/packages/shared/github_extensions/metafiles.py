import json
from github import Repository, UnknownObjectException
from ..logger import Out
from .rate_limiter import RateLimiter


metadata_file_path:str = "./metadata.json"

def has_metafiles(repo:Repository.Repository) -> list:
    """Return true if meta_file is found to exist """

    RateLimiter.check()
    try:
        repo.get_contents(metadata_file_path)
        Out.log(f"[{repo.full_name}] Found metadata file")
        return True
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] No metadata file")

    return False



def metadata(repo:Repository.Repository) -> dict:
    """Returns either the contents of the metadata file, or empty dict"""
    data:dict = {}

    try:
        data = json.loads( repo.get_contents(metadata_file_path).decoded_content)
    except UnknownObjectException:
        Out.log(f"[{repo.full_name}] Failed to fetch metadata file")
    return data