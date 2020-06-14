import pandas as pd
import time
import helper
import generateUsers as generate
import basicSim as basic
import flexibilitySim as flexibility

def flow():
    datasets = []
    numClients = 0
    start_millis = int(round(time.time() * 1000))

    # INFO
    ###############################
    data_dir = "./data/"
    data_file = "userData.xlsx"
    column_period = "Hour"
    data_sheet = "data"
    prices_sheet = "prices"
    saveOver = False
    peakAssumptionTarget = 150 # 150% above consumption average is peak
    ###############################

    # SEED
    ###############################
    helper.print_with_time(start_millis, "planting the seed")
    generate.defineSeed(123)
    ###############################

    # Open file
    ###############################
    helper.print_with_time(start_millis, "opening the file")
    datasets.append({"sheet" : "data", "ds" : helper.openFile(data_dir + data_file, data_sheet, column_period)})
    datasets.append({"sheet" : "prices", "ds" : helper.openFile(data_dir + data_file, prices_sheet, column_period)})
    periods = len(datasets[0]["ds"].index)
    prices_ds = datasets[-1]["ds"]
    ###############################

    # Generate new consumers
    ###############################
    helper.print_with_time(start_millis, "generating consumers")
    data2generate = [
        {"consumption" : "Consumption 1", "generation" : "Generation 1", "rep" : 20, "varCon" : 20, "varGen" : 20, "flexibility_empty_low" : 5, "flexibility_empty_high" : 20, "flexibility_peak_low" : 20, "flexibility_peak_high" : 40},
        {"consumption" : "Consumption 2", "generation" : "Generation 2", "rep" : 20, "varCon" : 20, "varGen" : 20, "flexibility_empty_low" : 5, "flexibility_empty_high" : 20, "flexibility_peak_low" : 20, "flexibility_peak_high" : 40},
        {"consumption" : "Consumption 3", "generation" : "Generation 3", "rep" : 20, "varCon" : 20, "varGen" : 20, "flexibility_empty_low" : 5, "flexibility_empty_high" : 20, "flexibility_peak_low" : 20, "flexibility_peak_high" : 40}
    ]
    datasets.append({"sheet" : "data generated", "ds" : generate.simulateProsumers(datasets[0]["ds"], data2generate, peakAssumptionTarget)})
    numClients = generate.getTotalNumClients(data2generate)
    endusers_ds = datasets[-1]["ds"]
    ###############################

    ###############################
    ###############################
    ###############################

    # Running a common day without self-consumption (price 1)
    ###############################
    helper.print_with_time(start_millis, "running common day, using prices 1")
    datasets.append({"sheet" : "common day", "ds" : basic.runCommonDay(endusers_ds, numClients, prices_ds["From grid 1"], prices_ds["To grid 1"])})
    ###############################

    # Running a common day with self-consumption (price 1)
    ###############################
    helper.print_with_time(start_millis, "running day with self consumption, using prices 1")
    datasets.append({"sheet" : "self cons", "ds" : basic.runSelfConsumption(endusers_ds, numClients, prices_ds["From grid 1"], prices_ds["To grid 1"])})
    ###############################

    # Running a common day with self-consumption only (price 1)
    ###############################
    helper.print_with_time(start_millis, "running day with self consumption only, using prices 1")
    datasets.append({"sheet" : "self only", "ds" : basic.runSelfConsumption_only(endusers_ds, numClients, prices_ds["From grid 1"])})
    ###############################

    # Running a common day without self-consumption (price 2)
    ###############################
    helper.print_with_time(start_millis, "running common day with hourly price, using prices 2")
    datasets.append({"sheet" : "common day hour", "ds" : basic.runCommonDay(endusers_ds, numClients, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Running a common day with self-consumption (price 2)
    ###############################
    helper.print_with_time(start_millis, "running day with self consumption with hourly price, using prices 2")
    datasets.append({"sheet" : "self cons hour", "ds" : basic.runSelfConsumption(endusers_ds, numClients, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Running a common day with self-consumption only (price 2)
    ###############################
    helper.print_with_time(start_millis, "running day with self consumption only with hourly price, using prices 2")
    datasets.append({"sheet" : "self only hour", "ds" : basic.runSelfConsumption_only(endusers_ds, numClients, prices_ds["From grid 2"])})
    ##############################

    # Running a common day with self-consumption and all flexibility (price 2)
    ##############################
    helper.print_with_time(start_millis, "running day with self consumption, flexibility and hourly price, using prices 2")
    datasets.append({"sheet" : "self flex", "ds" : flexibility.runSelfConsumptionFlexibility(endusers_ds, numClients, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ##############################
 
    # Running a common day with self-consumption only and all flexibility (price 2)
    ##############################
    helper.print_with_time(start_millis, "running day with self consumption only, flexibility and hourly price, using prices 2")
    datasets.append({"sheet" : "self only flex", "ds" : flexibility.runSelfConsumption_only_Flexibility(endusers_ds, numClients, prices_ds["From grid 2"])})
    ##############################

    # Flexibility where only x% will change consumption (price 2)
    ###############################
    x = 0.5 # percentual value of participations (clients in the community)
    helper.print_with_time(start_millis, "running day with self consumption, flexibility (" + str(x) + ") and hourly price, using prices 2")
    datasets.append({"sheet" : "self flex " + str(x), "ds" : flexibility.runSelfConsumptionFlexibility_x(endusers_ds, numClients, x, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Flexibility where x% will change y% of its consumption (price 2)
    ###############################
    x = 1 # percentual value of participations (clients in the community)
    y = 0.5 # percentual value of the participation (flexibility per client)
    helper.print_with_time(start_millis, "running day with self consumption, flexibility (" + str(x) + ", " + str(y) + ") and hourly price, using prices 2")
    datasets.append({"sheet" : "self flex " + str(x) + " " + str(y), "ds" : flexibility.runSelfConsumptionFlexibility_x_y(endusers_ds, numClients, x, y, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Flexibility where x% will change y% of its consumption (price 2)
    ###############################
    x = 0.2 # percentual value of participations (clients in the community)
    y = 0.3 # percentual value of the participation (flexibility per client)
    helper.print_with_time(start_millis, "running day with self consumption, flexibility (" + str(x) + ", " + str(y) + ") and hourly price, using prices 2")
    datasets.append({"sheet" : "self flex " + str(x) + " " + str(y), "ds" : flexibility.runSelfConsumptionFlexibility_x_y(endusers_ds, numClients, x, y, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Flexibility where x% will change y% of its consumption (price 2)
    ###############################
    x = 0.7 # percentual value of participations (clients in the community)
    y = 0.6 # percentual value of the participation (flexibility per client)
    helper.print_with_time(start_millis, "running day with self consumption, flexibility (" + str(x) + ", " + str(y) + ") and hourly price, using prices 2")
    datasets.append({"sheet" : "self flex " + str(x) + " " + str(y), "ds" : flexibility.runSelfConsumptionFlexibility_x_y(endusers_ds, numClients, x, y, prices_ds["From grid 2"], prices_ds["To grid 2"])})
    ###############################

    # Saving the file
    ###############################
    helper.print_with_time(start_millis, "saving the file")
    helper.save2file(datasets, saveOver, data_dir, data_file)
    ###############################

    helper.print_with_time(start_millis, "DONE")

flow()