from totes.core.utils.logger import *
import json
import sys
import pandas as pd


# noinspection PyBroadException
def sum_required(data):
    log("Starting Sum Required")
    message = None
    status = bool(True)
    try:
        step_name = "Starting Try"
        log(step_name)
        df = pd.json_normalize(data)
        step_name = "Converted to DataFrame"
        log(step_name)
        result = pd.DataFrame()
        step_name = "Starting For Loop 1"
        log(step_name)
        for d in df.date.unique():
            step_name = "Running For Loop 1"
            log(step_name)
            for n in df.name.unique():
                step_name = "Running For Loop 2"
                log(step_name)
                score = df.loc[(df.name == n) & (df.date == d)]['score'].sum()
                team = df.loc[(df.name == n) & (df.date == d)]['team'].unique()
                temp = pd.DataFrame({"date": d, "name": n, "score": score, "team": team})
                result = pd.concat([result, temp])
        data = result.reset_index(drop=True)
        data = json.loads(data.to_json(orient='records'))
    except:
        key = "error"
        step_name = "In the except for function SumRequired"
        message = str(sys.exc_info())
        log(sys.exc_info(), key)
        status = bool(False)
        log("Error Message From " + whoami() + " -- with message: " + message + " step ", step_name)
    return data, status, message
