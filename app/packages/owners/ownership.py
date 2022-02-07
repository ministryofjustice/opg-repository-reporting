from github import Repository, Team
from ..shared import has_metafiles, repositories

class Ownership:
    """Class to handle ..."""
    repositories:list = []
    # list of all owners (service teams)
    owners:list = []
    # list of repositories each team owns
    owner_repositories:dict = {}
    # list of repositories each team depends on
    owner_dependencies:dict = {}


    def update_owners(self, metadata:dict) -> None:
        """Add owners"""
        # add to the list of all owners (service teams)
        self.owners.extend(metadata.get("owners", []))
        self.owners = list( set( self.owners ) )

    def update_owned_repositories(self, repository:Repository.Repository, metadata:dict) -> None:
        """Update owned repos"""
        # now work out repos owned
        for owner in metadata.get("owners", []):
            owned = self.owner_repositories.get(owner, [])
            owned.append(repository.html_url)
            self.owner_repositories[owner] = owned
    
    def update_owned_dependencies(self, metadata:dict) -> None:
        """Update dependencies"""
        for owner in metadata.get("owners", []):
            owned = self.owner_dependencies.get(owner, [])
            owned.extend( metadata.get("dependencies", []) )
            self.owner_dependencies[owner] = owned


    def add(self, repository:Repository.Repository, metadata:dict) -> None:
        """Add data"""
        self.update_owners(metadata)
        self.update_owned_repositories(repository, metadata)
        self.update_owned_dependencies(metadata)
