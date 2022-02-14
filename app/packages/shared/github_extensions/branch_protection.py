from github import Repository

def protected_default_branch(repository:Repository) -> bool:
    """ Check if the default_branch has branch protection enabled """
    default_branch = repository.default_branch
    b = repository.get_branch(default_branch)
    return b.protected
