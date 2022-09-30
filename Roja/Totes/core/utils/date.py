import time
from datetime import date, timedelta


def getCurrentDateISO():
    return date.today().isoformat()


def getDate7Days():
    return date.today() - timedelta(days=7)


def getDateLastMonth():
    return date.today() - timedelta(days=30)


def millis():
    return int(round(time.time() * 1000))
