from github.Organization import Organization
from github.Team import Team
from github.Repository import Repository
from pprint import pp
from string import Template
import requests
from shared.logger.out import out


class secrets:

    endpoint:str = 'https://api.github.com/'
    header:str = 'application/vnd.github.v3+json'


    def has_secrets(self,
        repository:Repository,
        token:str) -> str:
        """
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.header
        }
        out.debug(f"[{repository.full_name}] Calling api for secrets")
        uri:str = f"repos/{repository.full_name}/actions/secrets"
        out.debug(f"API call to [{uri}]")

        response = requests.get(f"{self.endpoint}{uri}")
        if response.status_code == 200:
            count = dict( response.json() ).get('total_count', 0)
            return "Yes" if count > 0 else "No"
        elif response.status_code == 403:
            return "Permission error"
        return "No"
