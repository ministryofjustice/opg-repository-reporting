import time
from datetime import datetime, timedelta
from github import RateLimitExceededException
import github
from github.Rate import Rate
from shared.logger.out import Out

class RateLimiter:
    """Static class to handle github api reat limit tracking"""
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
        if RateLimiter.CONNECTION is None:
            raise ValueError("CONNECTION not set")
        ratelimit = RateLimiter.CONNECTION.get_rate_limit()
        Out.debug(f"Rate limit data: [{ratelimit.core.remaining}/{ratelimit.core.limit}] reset: [{ratelimit.core.reset}]")
        RateLimiter.LIMITER = ratelimit.core
        return RateLimiter.LIMITER

    @staticmethod
    def pause(extend_pause_by:int = 5) -> datetime:
        """
        Pauses the execution with time.sleep()

        Uses the details of LIMITER.reset to work this out
        """
        date = RateLimiter.LIMITER.reset + timedelta(seconds=extend_pause_by)
        now = datetime.utcnow()
        pause_for = (date - now).total_seconds()
        Out.debug(f"Pausing execution for [{pause_for}] seconds until [{date}]")
        time.sleep(pause_for)
        return date

    @staticmethod
    def check(refresh:bool = True, extend_pause_by:int = 5):
        """ Check the api rate and if we need to pause"""
        try:
            if refresh:
                RateLimiter.update()
            if RateLimiter.LIMITER.remaining <= 1:
                return RateLimiter.pause(extend_pause_by)

        except RateLimitExceededException:
            return RateLimiter.pause(extend_pause_by)

        return
