from datetime import datetime, timedelta


def get_date(weeks: int) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())
