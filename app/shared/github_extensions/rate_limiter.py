from pprint import pp
import time
from datetime import datetime, timedelta
from github import RateLimitExceededException
import github
from github.Rate import Rate
from shared.logger.out import out

class rate_limiter:
    # create an Rate class as we'll use this struct
    LIMITER:Rate = Rate(None, {}, {'limit':5000, 'remaining':5000}, True)
    CONNECTION:github.Github = None
    PAUSED = False

    @staticmethod
    def update() -> Rate:
        """
        Uses CONNECTION to update LIMITER with a call to get_rate_limit()
        Returns the updated version for ease
        """
        if rate_limiter.CONNECTION == None:
            raise ValueError("CONNECTION not set")
        ratelimit = rate_limiter.CONNECTION.get_rate_limit()
        out.debug(f"Rate limit data: [{ratelimit.core.remaining}/{ratelimit.core.limit}] reset: [{ratelimit.core.reset}]")
        rate_limiter.LIMITER = ratelimit.core
        return rate_limiter.LIMITER

    @staticmethod
    def pause(extend_pause_by:int = 5) -> datetime:
        """
        Pauses the execution with time.sleep()

        Uses the details of LIMITER.reset to work this out
        """
        date = rate_limiter.LIMITER.reset + timedelta(seconds=extend_pause_by)
        now = datetime.utcnow()
        pause_for = (date - now).total_seconds()
        out.debug(f"Pausing execution for [{pause_for}] seconds until [{date}]")
        time.sleep(pause_for)
        return date

    @staticmethod
    def check(refresh:bool = True, extend_pause_by:int = 5):
        """
        """
        try:
            if refresh:
                rate_limiter.update()
            if rate_limiter.LIMITER.remaining <= 1:
                return rate_limiter.pause(extend_pause_by)

        except RateLimitExceededException:
            return rate_limiter.pause(extend_pause_by)

        return
