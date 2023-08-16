from Roja.Totes.core.cache.setCache import *
from Roja.Totes.jira.dataprocessor.summer import *


def how(data, fine_data, data_format="fine", data_from_cache=False, cache_name="ProcessedCache"):
    log("Starting How Processor lib: dataprocessor.filter.how")
    status = bool(True)
    key = "info"
    console = bool(False)
    message = None
    move = bool(True)
    if data_format == "fine":
        if fine_data is None:
            log("No Fine Data Found")
            fine_data, move, message = sum_required(data)
            if move:
                if fine_data is not None:
                    data = json.dumps(fine_data, indent=3, sort_keys=True)
                    move, message = setRedisCache(cache_name, data, console, True)
                    if not move:
                        status = bool(False)
                        message = "Setting cache failed for " + cache_name + " with message: " + message
                        log(message, key, console)
                    else:
                        message = "How Processor Successful for " + data_format + " data"
                else:
                    status = bool(False)
                    message = "Null Value reported in Fine Data from SumRequired "
                    log(message, key, console)
            else:
                status = bool(False)
                log(message, key, False)
        else:
            data = json.dumps(fine_data, indent=3, sort_keys=True)
            move, message = set_cache(cache_name, data)
            if not move:
                status = bool(False)
                message = "False status received while setting cache " + cache_name + " with message: " + message
                log(message, key, console)
            else:
                message = "How Processor Successful for " + data_format + " data"
    if data_format == "extract":
        if not data_from_cache:
            # move, message = set_cache(ExtractedCache, data)
            move, message = set_cache(cache_name, data)

        data = json.dumps(data, indent=3, sort_keys=True)

        if not move:
            status = bool(False)
            message = "False status received while setting cache " + cache_name + " with message: " + message
            log(message, key, console)
        else:
            message = "How Processor Successful for " + data_format + " data"

    return data, status, message
