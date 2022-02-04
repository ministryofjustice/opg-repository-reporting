from datetime import date
from dateutil.relativedelta import relativedelta
from shared.logger.out import Out


def counters_for_date_range(start:date, end:date, struct:dict) -> dict:
    """ Returns an empty dict with preset keys referencing YYYYMM between the start and end date """
    # make sure start is the first day of the month
    start = start.replace(day=1, hour=0, minute=0, second=0)
    Out.debug(f"Creating dict between [{start}] and [{end}]")
    while start <= end:
        key = start.strftime('%Y-%m')
        struct.setdefault(key, 0)
        start = start + relativedelta(months=1)
    return struct
