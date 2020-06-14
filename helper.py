import pandas as pd
import time

def openFile(file, sheet, orderBy):
    ds = pd.read_excel(file, sheet_name = sheet)
    if orderBy != None:
        ds = ds.set_index([orderBy])
        ds = ds.sort_index()
    return ds

def save2file(datasets, saveOver, directory, file):
    if saveOver == False:
        file = "res_" + file
    writer = pd.ExcelWriter(directory + file)
    for ds in datasets:
        ds["ds"].to_excel(writer, sheet_name=ds["sheet"], startrow=0, startcol=0)
    writer.save()

def print_with_time(start_millis, text):
    millis = int(round(time.time() * 1000)-start_millis)
    milliseconds = int(millis%1000)
    seconds = (millis/1000)%60
    seconds = int(seconds)
    minutes = (millis/(1000*60))%60
    minutes = int(minutes)
    hours = int((millis/(1000*60*60))%24)

    if milliseconds < 10: milliseconds = "00" + str(milliseconds)
    elif milliseconds < 100: milliseconds = "0" + str(milliseconds)
    else: milliseconds = str(milliseconds)

    if seconds < 10: seconds = "0" + str(seconds)
    else: seconds = str(seconds)

    if minutes < 10: minutes = "0" + str(minutes)
    else: minutes = str(minutes)

    if hours < 10: hours = "0" + str(hours)
    else: hours = str(hours)

    print("%s:%s:%s.%s :: %s" % (hours, minutes, seconds, milliseconds, text))

def generate_dataframe(ds):
    ds_res = pd.DataFrame(index=ds.index.copy())

    ds_res['Grid earned'] = 0
    ds_res['Grid earned'] = 0
    ds_res['Grid payed'] = 0
    ds_res['Grid balance'] = 0
    ds_res['Community earn'] = 0
    ds_res['Community payed'] = 0
    ds_res['Community balance'] = 0
    ds_res['Community consumption'] = 0
    ds_res['Community generation'] = 0
    return ds_res