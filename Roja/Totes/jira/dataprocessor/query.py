import sys

from Roja.Totes.core.utils.logger import *


def build_time_query(key='Created', value='this_week'):
    query = "startOfWeek()"
    result = None

    if value == 'this_week':
        query = "startOfWeek()"
    if value == 'today':
        query = 'startOfDay()'
    if value == 'from_yesterday':
        query = 'startOfDay(-1)'
    if value == 'yesterday':
        query = ['startOfDay(-1)', 'endOfDay(-1)']
    if value == "Last7Days":
        query = "startOfDay(-7)"  # Default
    if value == "Last5Days":
        query = "startOfDay(-5)"  # Default

    if key is not None:
        result = "'" + str(key) + "'" + ">=" + query

    return result


# noinspection PyBroadException
def query_builder(dashboard='Performance Score', key="Completed Date", startAt=0, duration=None):
    # logNow("Starting Function " + whoami())
    status = bool(True)
    message = None
    jql = "jql="
    try:

        # key = "Completed Date"
        if duration is not None:
            time_query = build_time_query(key, duration)  # Level Access
        else:
            time_query = build_time_query(key, "Last7Days")

        if dashboard == 'Performance Score':
            jql = jql + "('Performance Score'>0 or 'Performance Score'<0)"
            jql = jql + " and " + time_query
        else:
            jql = jql + time_query
        jql = jql + "&maxResults=100&startAt=" + str(startAt)
    except:
        message = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
        status = bool(False)
        log(message)

    return jql, status, message
