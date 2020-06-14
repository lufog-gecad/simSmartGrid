import pandas as pd
import numpy as np
import helper
import basicSim as basic

def getTop_cheapest(cons, gen, prices, nTop):
    fromGrid = cons - gen
    energyCosts = fromGrid/1000 * prices
    iTop = []
    for _ in range(nTop):
        lower = (-1, -1) # (index, cost)
        for j in range(len(energyCosts)):
            if j not in iTop:
                if lower[0] != -1:
                    lower = (j, energyCosts[j])
                elif lower[1] > energyCosts[j]:
                    lower = (j, energyCosts[j])
        iTop.append(lower[0])
    print(iTop)
    return iTop

def getUnusedIndex(index, numIndexs, usedIndexs):
    c = 0
    for i in range(numIndexs):
            if i not in usedIndexs:
                c += 1
                if c > index:
                    return i

def getFlexibilityToShift(cons, flex, y, energyCosts):
    # fazer um for aleatório para os 96 periodos e ir anexando flexibility de acordo com o target até atingir o flex2get
    
    flex2get = sum(flex) * y
    costs = set(zip(np.arange(0, len(energyCosts)), energyCosts))
    costs = sorted(costs, key=lambda tup: tup[1])
    for i in range(len(costs)):
        flex_bank += flex[p]
        cons_shift[p] -= flex[p]
        if flex_bank > flex2get:
            break
        
def changeConsumption(cons, flex, gen, prices, y=1,):
    avgValue = 1 # target to move (eg. 90 % of avg)
    fromGrid = cons - gen
    energyCosts = fromGrid/1000 * prices
    avgCost = sum(energyCosts) / len(energyCosts)
    cons_shift = cons.copy()

    # get energy to move (periods with cost above avg)
    flex_bank = 0
    if y == 1:
        for p in range(len(cons)):
            if energyCosts[p] >= avgCost * avgValue:
                flex_bank += flex[p]
                cons_shift[p] -= flex[p]
    else:
        flex2get = sum(flex) * y
        costs = set(zip(np.arange(0, len(energyCosts)), energyCosts))
        costs = sorted(costs, key=lambda tup: tup[1])
        for cost in costs:
            flex_bank += flex[cost[0]]
            cons_shift[cost[0]] -= flex[cost[0]]
            if flex_bank > flex2get:
                break

    # distribute energy (periods till equal avg)
    for p in range(len(cons)):
        if energyCosts[p] < avgCost * avgValue:
            margin = avgCost * avgValue - energyCosts[p]
            goTo = int(margin / prices[p] * 1000)
            if goTo > flex_bank: goTo = flex_bank
            flex_bank -= goTo
            cons_shift[p] += goTo

    # equal distribution (rest/(periods/3) distributed to top_1/3 periods low cost)
    if flex_bank > 0:
        nTop = int(len(cons) / 3)
        flex_bank = int(flex_bank / nTop)
        iTop = getTop_cheapest(cons, gen, prices, nTop)
        for t in iTop:
            cons_shift[t] += flex_bank

    # final adjust of diference (resulted from int convertions)
    dif = sum(cons) - sum(cons_shift)
    if dif > 0:
        cons_shift[np.random.randint(low=0, high=(len(cons)-1))] += dif
    elif dif < 0:
        cons_shift[np.random.randint(low=0, high=(len(cons)-1))] -= dif

    return cons_shift

def runSelfConsumptionFlexibility(ds, numClients, fromGridPrice, toGridPrice):
    ds_res = ds.copy()

    for nClient in range(numClients):
        ds_res['Consumption ' + str(nClient+1)] = changeConsumption(ds['Consumption ' + str(nClient+1)], ds['Flexibility ' + str(nClient+1)], ds['Generation ' + str(nClient+1)], fromGridPrice)

    return basic.runSelfConsumption(ds_res, numClients, fromGridPrice, toGridPrice)

def runSelfConsumption_only_Flexibility(ds, numClients, fromGridPrice):
    ds_res = ds.copy()

    for nClient in range(numClients):
        ds_res['Consumption ' + str(nClient+1)] = changeConsumption(ds['Consumption ' + str(nClient+1)], ds['Flexibility ' + str(nClient+1)], ds['Generation ' + str(nClient+1)], fromGridPrice)

    return basic.runSelfConsumption_only(ds_res, numClients, fromGridPrice)

def runSelfConsumptionFlexibility_x(ds, numClients, x, fromGridPrice, toGridPrice):
    ds_res = ds.copy()
    iClientsChanged = []
    
    for i in range(int(numClients * x)):
        n = getUnusedIndex(np.random.randint(low = 0, high = numClients - i), numClients, iClientsChanged)
        ds_res['Consumption ' + str(n+1)] = changeConsumption(ds['Consumption ' + str(n+1)], ds['Flexibility ' + str(n+1)], ds['Generation ' + str(n+1)], fromGridPrice)
        iClientsChanged.append(n)

    return basic.runSelfConsumption(ds_res, numClients, fromGridPrice, toGridPrice)

def runSelfConsumptionFlexibility_x_y(ds, numClients, x, y, fromGridPrice, toGridPrice):
    ds_res = ds.copy()
    iClientsChanged = []
    
    for i in range(int(numClients * x)):
        n = np.random.randint(low = 0, high = numClients - i)
        n = getUnusedIndex(np.random.randint(low = 0, high = numClients - i), numClients, iClientsChanged)
        ds_res['Consumption ' + str(n+1)] = changeConsumption(ds['Consumption ' + str(n+1)], ds['Flexibility ' + str(n+1)], ds['Generation ' + str(n+1)], fromGridPrice, y)
        iClientsChanged.append(n)

    return basic.runSelfConsumption(ds_res, numClients, fromGridPrice, toGridPrice)