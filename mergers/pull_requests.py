import datetime
import dateutil.relativedelta

class pull_requests:
    repository = None
    start_date = None
    end_date = None
    structure = {}
    pull_requests = []

    def __init__(self, repository, start_date, end_date):
        self.repository = repository
        self.start_date = start_date
        self.end_date = end_date
        # generate the date structure
        start = self.start_date
        self.structure = {'Repository': self.repository.name}
        while start <= self.end_date:
            key = start.strftime('%Y-%m')
            self.structure[key] = 0
            # increment the date by a month, but keep it to the 1st of the month
            start = start + dateutil.relativedelta.relativedelta(months=1)
            start = start.replace(day=1, hour=0, minute=0, second=0)
        #
        return
    # fetch all the pr's for this repo
    # - configured for rate limiter usage to return results
    def get(self):
        self.pull_requests = self.repository.get_pulls(
                                        state='closed',
                                        sort='merged_at',
                                        direction='desc',
                                        base=self.repository.default_branch)
        return True, self.pull_requests

    # check if the merged_at date is within the allowed times
    def date_valid(self, merged_at):
        if merged_at >= self.start_date and merged_at <= self.end_date:
            return True
        return False

    # convert to month with counters
    # - as the api call to get PRs doesnt have a way to filteron date
    #   this group stage does that to try and reduce workloads (as some have over 4k PRs)
    def group(self):
        length = self.pull_requests.totalCount
        x = 1
        for pr in self.pull_requests:
            print('{}[{}/{}] ({}) {}'.format('      ', x, length, self.repository.name, pr.merged_at) )
            if pr.merged:
                valid = self.date_valid(pr.merged_at)
                if valid:
                    monthYear = pr.merged_at.strftime('%Y-%m')
                    self.structure[monthYear] += 1
                # presuming the prs are sorted by date correctly (merged_at desc), to speed
                # up the process if the date is outside of the range, return straight away
                elif not valid:
                    print('{}>>> Exiting PRs ({}) as date [{}] is out of range ({}-{})'.format(
                                    '      ',
                                    self.repository.name,
                                    pr.merged_at,
                                    self.start_date,
                                    self.end_date
                            ) )
                    return True, self.structure
            x += 1
        #
        return True, self.structure
