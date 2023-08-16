from Roja.Totes.core.utils.logger import *
import json
import sys
import pandas as pd
import traceback

# noinspection PyBroadException
def sum_required(data):
    log("Starting Sum Required lib: dataprocessor/summer" + whoami())
    errorMessage = None
    park = bool(False)
    try:
        if data is not None:
            step_name = "Starting Try in the function " + whoami()
            log(step_name)
            df = pd.json_normalize(json.loads(data))
            log(df.columns)
            step_name = "Converted to DataFrame"
            log(step_name)
            if len(df.columns)<=5:
                park = bool(True)
            if not park:
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
        errorMessage = str(sys.exc_info())
        log(sys.exc_info(), key)
        park = bool(True)
        log("Error Message From " + whoami())
        log(" -- with message: " + errorMessage + " step ", step_name)
        print("Traceback")
        print(traceback.format_exc())
    return data, park, errorMessage