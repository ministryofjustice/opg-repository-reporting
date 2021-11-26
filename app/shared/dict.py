from datetime import date
import dateutil.relativedelta
from shared.logger.out import out


def counters_for_date_range(start:date, end:date, struct:dict = {}) -> dict:
    # make sure start is the first day of the month
    start = start.replace(day=1, hour=0, minute=0, second=0)
    out.debug(f"Creating dict between [{start}] and [{end}]")
    while start <= end:
        key = start.strftime('%Y-%m')
        struct.setdefault(key, 0)
        start = start + dateutil.relativedelta.relativedelta(months=1)
    return struct
