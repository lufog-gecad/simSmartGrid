import numpy as np

def defineSeed(seed):
    np.random.seed(seed)


def generateFlexibility(consumption, peakAssumptionTarget, flexEmpty_low, flexEmpty_high, flexPeak_low, flexPeak_high):
    res = []
    targetPeak = sum(consumption)/len(consumption)*peakAssumptionTarget/100

    for period in range(len(consumption)):
        if consumption[period] < targetPeak:
            res.append(int(np.random.randint(low=flexEmpty_low, high=(flexEmpty_high))/100 * consumption[period]))
        else:
            res.append(int(np.random.randint(low=flexPeak_low, high=(flexPeak_high))/100 * consumption[period]))
    return res

def simulateProsumers(ds, data2generate, peakAssumptionTarget):
    ds_res = ds.copy()
    numClients = int(data2generate[-1]["consumption"][-1:])

    for rep in data2generate:
        ds_res.columns.get_loc(rep["generation"])
        flex = generateFlexibility(ds_res[rep["consumption"]], peakAssumptionTarget, rep["flexibility_empty_low"], rep["flexibility_empty_high"], rep["flexibility_peak_low"], rep["flexibility_peak_high"])
        ds_res.insert(ds_res.columns.get_loc(rep["generation"]), "Flexibility " + rep["consumption"][-1:], flex)

        for i in range(rep["rep"]):
            numClients += 1
            x = np.random.randint(size=24, low=(100-rep["varCon"]), high=(100+rep["varCon"]))/100
            cons = (ds_res[rep["consumption"]] * x).astype(int)
            ds_res[rep["consumption"][:-1] + str(numClients)] = cons

            ds_res["Flexibility " + str(numClients)] = generateFlexibility(cons, peakAssumptionTarget, rep["flexibility_empty_low"], rep["flexibility_empty_high"], rep["flexibility_peak_low"], rep["flexibility_peak_high"])

            xx = np.random.randint(size=24, low=(100-rep["varGen"]), high=(100+rep["varGen"]))/100
            ds_res[rep["generation"][:-1] + str(numClients)] = (ds_res[rep["generation"]] * xx).astype(int)
    return ds_res

def getTotalNumClients(data2generate):
    numClients = int(data2generate[-1]["consumption"][-1:])
    for rep in data2generate:
        numClients += rep["rep"]
    return numClients