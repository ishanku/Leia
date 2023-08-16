import sys
import logging
from Roja.Totes.core.utils.identifier import *
logger = logging.getLogger("Leia.General")

def build_time_query(key='Created', value='Last10Days'):
    logger.info("Starting Function " + whoami())
    query = "startOfWeek()"
    result = None

    if value == 'this_week':
        query = "startOfWeek()"
    if value == 'this_month':
        query = "startOfMonth()"
    if value == 'today':
        query = 'startOfDay()'
    if value == 'from_yesterday':
        query = 'startOfDay(-1)'
    if value == 'yesterday':
        query = ['startOfDay(-1)', 'endOfDay(-1)']
    if value == "Last30Days":
        query = "startOfDay(-30)"
    if value == "Last10Days":
        query = "startOfDay(-10)"  # Default
    if value == "Last7Days":
        query = "startOfDay(-7)"  # Default
    if value == "Last5Days":
        query = "startOfDay(-5)"  # Default

    if key is not None:
        result = "'" + str(key) + "'" + ">=" + query

    return result


# noinspection PyBroadException
def query_builder(startAt=0, duration=None, key="Completed Date", dashboard='Performance Score'):
    logger.info("Starting Function lib: dataprocessor/query")
    park = bool(True)
    message = None
    jql = "jql="
    try:
        # key = "Completed Date"
        if duration is not None:
            time_query = build_time_query(key, duration)  # Level Access
        else:
            time_query = build_time_query(key, "Last10Days")

        if dashboard == 'Performance Score':
            jql = jql + "('Performance Score'>0 or 'Performance Score'<0)"
            jql = jql + " and " + time_query
        else:
            jql = jql + time_query
        jql = jql + "&maxResults=100&startAt=" + str(startAt)

        logger.info("-----------------------------------------------------------")
        logger.info("Printing the JQL " + jql)
        logger.info("-----------------------------------------------------------")

    except:
        message = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
        park = bool(True)
        logger.info(message)

    return jql, park, message
