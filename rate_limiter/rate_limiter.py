from github import Github
from github import RateLimitExceededException
import calendar
import time
import datetime


# rate_limiter wrapper to handle the github api call limits
class rate_limiter:
    g = None
    remaining = 0
    rate_limit = None

    def __init__(self, g):
        self.g = g
        self.reset()
        return

    def reset(self):
        self.rate_limit = self.g.get_rate_limit()
        self.remaining, limit = self.g.rate_limiting
        return
    # pause execution
    def pause(self):
        reset_timestamp = self.g.rate_limiting_resettime
        date = datetime.datetime.fromtimestamp(reset_timestamp)
        # add 5 seconds to be sure the rate limit has been reset
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 1
        print('>>>>> Sleeping for {} seconds until {}'.format(sleep_time, date.strftime("%Y-%m-%d %H:%M") ) )
        time.sleep(sleep_time)

    # run
    def run(self, function, on_rate_limited=None, on_error=None, on_complete=None):
        while True:
            try:
                # if we have calls remaining, run the function
                if self.remaining > 0:
                    # returns a tripple of a boolean for complete,
                    # bool for status and a counter for number of calls made
                    complete, function_result = function()
                    # update the rate limit
                    r, limit = self.g.rate_limiting
                    self.remaining = r
                    # if complete, break the loop
                    if complete == True and on_complete != None:
                        on_complete(function_result)
                        break
                    elif complete == True:
                        break
                    # if theres an error, run that function
                    if function_result != True and errror_function != None:
                        on_error()

                # we've caught the rate limit error before making the call
                else:
                    print('\n>>>>> Rate limit hit 0')
                    if on_rate_limited != None:
                        on_rate_limited()
                    self.pause()
                    self.reset()
            # rate limit hit
            except RateLimitExceededException:
                print('\n>>>>> Rate limit exceeded')
                if on_rate_limited != None:
                    on_rate_limited()
                self.pause()
                self.reset()
            # breaks the loop
            except StopIteration:
                break
        # end the func
        return
