import pandas as pd
import helper

def runCommonDay(ds, numClients, fromGridPrice, toGridPrice):
    ds_res = helper.generate_dataframe(ds)
    money2grid = 0
    money2community = 0
    total_cons = 0
    total_gen = 0

    for nClient in range(numClients):
        toGrid = []
        fromGrid = []
        earnGrid = []
        payGrid = []

        for period in range(len(ds['Consumption ' + str(nClient+1)])):
            cons = ds['Consumption ' + str(nClient+1)][period]
            gen = ds['Generation ' + str(nClient+1)][period]
            toGrid.append(gen)
            fromGrid.append(cons)
            earnGrid.append(gen/1000*toGridPrice[period])
            payGrid.append(cons/1000*fromGridPrice[period])

        ds_res['Consumption ' + str(nClient+1)] = ds['Consumption ' + str(nClient+1)]
        ds_res['Generation ' + str(nClient+1)] = ds['Generation ' + str(nClient+1)]
        ds_res['To grid ' + str(nClient+1)] = toGrid
        ds_res['From grid ' + str(nClient+1)] = fromGrid
        ds_res['Earned from grid ' + str(nClient+1)] = earnGrid
        ds_res['Payed to grid ' + str(nClient+1)] = payGrid
        money2grid += sum(payGrid)
        money2community += sum(earnGrid)
        total_cons += sum(ds['Consumption ' + str(nClient+1)])
        total_gen += sum(ds['Generation ' + str(nClient+1)])

    ds_res['Grid earned'] = money2grid
    ds_res['Grid payed'] = money2community
    ds_res['Grid balance'] = money2grid - money2community
    ds_res['Community earn'] = money2community
    ds_res['Community payed'] = money2grid
    ds_res['Community balance'] = money2community - money2grid
    ds_res['Community consumption'] = total_cons
    ds_res['Community generation'] = total_gen
    return ds_res

def runSelfConsumption(ds, numClients, fromGridPrice, toGridPrice):
    ds_res = helper.generate_dataframe(ds)
    money2grid = 0
    money2community = 0
    total_cons = 0
    total_gen = 0

    for nClient in range(numClients):
        toGrid = []
        fromGrid = []
        earnGrid = []
        payGrid = []

        for period in range(len(ds['Consumption ' + str(nClient+1)])):
            cons = ds['Consumption ' + str(nClient+1)][period]
            gen = ds['Generation ' + str(nClient+1)][period]
            if gen > cons:
                toGrid.append(gen-cons)
                fromGrid.append(0)
                earnGrid.append((gen-cons)/1000*toGridPrice[period])
                payGrid.append(0)
            else:
                toGrid.append(0)
                fromGrid.append(cons-gen)
                earnGrid.append(0)
                payGrid.append((cons-gen)/1000*fromGridPrice[period])
                
        ds_res['Consumption ' + str(nClient+1)] = ds['Consumption ' + str(nClient+1)]
        ds_res['Generation ' + str(nClient+1)] = ds['Generation ' + str(nClient+1)]
        ds_res['To grid ' + str(nClient+1)] = toGrid
        ds_res['From grid ' + str(nClient+1)] = fromGrid
        ds_res['Earned from grid ' + str(nClient+1)] = earnGrid
        ds_res['Payed to grid ' + str(nClient+1)] = payGrid
        money2grid += sum(payGrid)
        money2community += sum(earnGrid)
        total_cons += sum(ds['Consumption ' + str(nClient+1)])
        total_gen += sum(ds['Generation ' + str(nClient+1)])

    ds_res['Grid earned'] = money2grid
    ds_res['Grid payed'] = money2community
    ds_res['Grid balance'] = money2grid - money2community
    ds_res['Community earn'] = money2community
    ds_res['Community payed'] = money2grid
    ds_res['Community balance'] = money2community - money2grid
    ds_res['Community consumption'] = total_cons
    ds_res['Community generation'] = total_gen
    return ds_res

def runSelfConsumption_only(ds, numClients, fromGridPrice):
    ds_res = helper.generate_dataframe(ds)
    money2grid = 0
    money2community = 0
    total_cons = 0
    total_gen = 0

    for nClient in range(numClients):
        toGrid = []
        fromGrid = []
        earnGrid = []
        payGrid = []

        for period in range(len(ds['Consumption ' + str(nClient+1)])):
            cons = ds['Consumption ' + str(nClient+1)][period]
            gen = ds['Generation ' + str(nClient+1)][period]
            if gen > cons:
                toGrid.append(gen-cons)
                fromGrid.append(0)
                earnGrid.append(0)
                payGrid.append(0)
            else:
                toGrid.append(0)
                fromGrid.append(cons-gen)
                earnGrid.append(0)
                payGrid.append((cons-gen)/1000*fromGridPrice[period])
                
        ds_res['Consumption ' + str(nClient+1)] = ds['Consumption ' + str(nClient+1)]
        ds_res['Generation ' + str(nClient+1)] = ds['Generation ' + str(nClient+1)]
        ds_res['To grid ' + str(nClient+1)] = toGrid
        ds_res['From grid ' + str(nClient+1)] = fromGrid
        ds_res['Earned from grid ' + str(nClient+1)] = earnGrid
        ds_res['Payed to grid ' + str(nClient+1)] = payGrid
        money2grid += sum(payGrid)
        money2community += sum(earnGrid)
        total_cons += sum(ds['Consumption ' + str(nClient+1)])
        total_gen += sum(ds['Generation ' + str(nClient+1)])

    ds_res['Grid earned'] = money2grid
    ds_res['Grid payed'] = money2community
    ds_res['Grid balance'] = money2grid - money2community
    ds_res['Community earn'] = money2community
    ds_res['Community payed'] = money2grid
    ds_res['Community balance'] = money2community - money2grid
    ds_res['Community consumption'] = total_cons
    ds_res['Community generation'] = total_gen
    return ds_res