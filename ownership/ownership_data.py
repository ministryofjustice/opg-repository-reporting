

class ownership_data:
    repo = None
    clones = None
    commit_data = None
    open_pull_requests = None
    teams = None
    default_branch = None
    forks_count = None

    def __init__(self, repo):
        self.repo = repo
        return

    # fetch all the required data from the repository
    # called by wrapper function incase this triggers
    # limits
    def get_data(self):
        self.forks_count = self.repo.forks_count
        self.clones = self.repo.get_clones_traffic(per="week")
        self.default_branch = self.repo.default_branch
        branch = self.repo.get_branch(self.default_branch)
        self.commit_date = branch.commit.commit.committer.date
        self.open_pull_requests = self.repo.get_pulls(state='open', sort='created', base=self.default_branch)
        self.teams = self.repo.get_teams()
        return True, True
    # return all the teams with access to the repo as a string
    # removing excluded
    def teams_as_string(self, exclude, others=''):
        teams = ''
        for t in self.teams:
            matched = ( t.name.lower() == exclude.lower() )
            within = ( t.name.lower() in others.lower() )
            if  matched == False and within == False:
                teams =  "{name}, {existing}".format(
                        name = t.name,
                        existing= teams)
        return teams.strip(", ")
