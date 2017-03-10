import sys
import json
import pprint
import plotMaker
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)

def separateFiles(filenames):
    cpfiles = []
    ipfiles = []
    for name in filenames:
        solver = name.split("_")[-1]
        if solver == "cp":
            cpfiles.append(name)
        elif solver == "ip":
            ipfiles.append(name)
    return(cpfiles, ipfiles)

def separateOptFuncs(filenames):
    cost = []
    duration = []
    conn = []
    flights = []
    for name in filenames:
        optfunc = name.split("_")[-2]
        if optfunc == "cost":
            cost.append(name)
        elif optfunc == "connections":
            conn.append(name)
        elif optfunc == "trip":
            duration.append(name)
        elif optfunc == "flights":
            flights.append(name)
    return cost,duration,conn,flights

# given a filename, returns its running time
def runningTime(filename):
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.split()
            if len(line) > 0 and line[0] == "Solving:":
                return float(line[1])
    return [filename, None]

def getInstanceProps(filename):
    instance = filename.split("/")[-1].split("_")[0:4]
    instance = '_'.join(instance)
    return(instance)

def getInstanceName(filename):
    instance = filename.split("/")[-1].split("_")[0:5]
    instance = '_'.join(instance)
    return(instance)

def median(lista):
    lista.sort()
    if len(lista) % 2 == 0:
        item1 = lista[int(len(lista)/2) - 1]
        item2 = lista[int(len(lista)/2)]
        returned = (item1 + item2)/2
    else:
        returned = lista[int((len(lista) - 1)/2)]
    return returned

# running time per instance, collapsing on opt func
def runningtimes(allfiles):
    runtimes = []
    instanceTimes = []
    instanceName = ""
    for filename in allfiles:
        currentInstance = getInstanceProps(filename)
        time = runningTime(filename)
        if instanceName == "":
            instanceName = currentInstance
        elif instanceName != currentInstance:
            m = int(instanceName.split("_")[0])
            n = int(instanceName.split("_")[1])
            d = int(instanceName.split("_")[2])
            T = int(instanceName.split("_")[3])
            runtimes.append([m, n, d, T, instanceName, median(instanceTimes)])
            instanceTimes = []
            instanceName = currentInstance
        instanceTimes.append(time)
    return runtimes

def parseForParallelPlot(cpdata, ipdata, instanceNames):
    with open("parallel.csv", "w") as f:
        line = "Running Time,m,n,d,T,Name\n"
        f.write(line)
        for cp, ip, name in zip(cpdata, ipdata, instanceNames):
            m = name.split("_")[0]
            n = name.split("_")[1]
            d = name.split("_")[2]
            T = name.split("_")[3]
            cpline = ",".join([str(cp), m, n, d, T, "cp"])
            ipline = ",".join([str(ip), m, n, d, T, "ip"])
            f.write(cpline + "\n" + ipline + "\n")

# returns running times, instances, grouped by m, n, d or T
def group(data, pos):
    sorteddata = sorted(data, key=itemgetter(pos))
    vals = [val[pos] for val in sorteddata]
    instanceNames = [val[4] for val in sorteddata]
    newdata = [val[5] for val in sorteddata]
    if pos == 0:
        xlabel = "Number of Flights"
    elif pos == 1:
        xlabel = "Number of Airports"
    elif pos == 2:
        xlabel = "Number of Destinations"
    elif pos == 3:
        xlabel = "Holiday Time"
    else:
        print("The pos index specified is wrong!!!!")
    return newdata, instanceNames, vals, xlabel

def satVsUnsat(ipfiles):
    unsatFiles = []
    satFiles = []
    for ip in ipfiles:
        sat = False
        with open(ip, "r") as f:
            for line in f.readlines():
                line = line.strip().split()
                props = getInstanceName(ip)

                if len(line) > 0 and line[0] == "Schedule:":
                    sat = True
                    if len(satFiles) == 0 or satFiles[-1] != props:
                        satFiles.append(props)
            if not sat and (len(unsatFiles) == 0 or unsatFiles[-1] != props):
                unsatFiles.append(props)
    return satFiles, unsatFiles

def countLines(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        return len(lines)

def compareCPandIP(filenames):
    cpfiles, ipfiles = separateFiles(filenames)
    cpruntimes = runningtimes(cpfiles)
    ipruntimes = runningtimes(ipfiles)
    pos = 0
    cpdata, instanceNames, vals, xlabel = group(cpruntimes, pos)
    ipdata, instanceNames, vals, xlabel = group(ipruntimes, pos)
    # plotMaker.makePlots(cpdata, ipdata, vals, xlabel)
    ylabel = "Running Times (sec)"
    plotMaker.twoHistograms(cpdata, ipdata, vals, xlabel, ylabel)
    # plotname = "Running time of CP and IP models"
    # parseForParallelPlot(cpdata, ipdata, instanceNames)
    # plotMaker.parallelCoordinates(cpdata, ipdata)

def compareOptFuncs(filenames):
    cost,duration,conn,flights = separateOptFuncs(filenames)

    costruntimes = runningtimes(cost)
    durationruntimes = runningtimes(duration)
    connruntimes = runningtimes(conn)
    flightsruntimes = runningtimes(flights)

    pos = 0

    costdata, instanceNames, vals, xlabel = group(costruntimes, pos)
    durationdata, instanceNames, vals, xlabel = group(durationruntimes, pos)
    conndata, instanceNames, vals, xlabel = group(connruntimes, pos)
    flightsdata, instanceNames, vals, xlabel = group(flightsruntimes, pos)
    print(costdata)
    print(durationdata)
    print(conndata)
    print(flightsdata)
    ylabel = "Running Times (sec)"
    plotMaker.histograms(costdata,durationdata,conndata,flightsdata,vals, xlabel, ylabel)

# returns a plot with one bar with number of unsat and one bar with number of sat instances
def compareSatvsUnsat(filenames):
    cpfiles, ipfiles = separateFiles(filenames)
    satFiles, unsatFiles = satVsUnsat(ipfiles)
    xlabel = ""
    plotname = "SAT vs UNSAT TP instances"
    plotMaker.twoBarsOnce(len(satFiles), len(unsatFiles), ["SAT", "UNSAT"], xlabel, "", plotname)

# aims to generate a cumulative bar with total configs, successful configs, sat and unsat instances
def dataGeneratorStats(filenames, total):
    cpfiles, ipfiles = separateFiles(filenames)
    satFiles, unsatFiles = satVsUnsat(ipfiles)
    totalSAT = len(satFiles)
    totalUNSAT = len(unsatFiles)
    garbageCount = total*5 - (totalSAT+totalUNSAT)

    data = {
        'config_name': ['MonteCarlo'],
        'garbage': [garbageCount],
        'unsat': [totalUNSAT],
        'sat': [totalSAT]
    }
    print(data)
    plotMaker.stackedBar(data)

totalCount = 200 # how many configs were given to the data generator
filenames = sys.argv[1:]
dataGeneratorStats(filenames, totalCount)
