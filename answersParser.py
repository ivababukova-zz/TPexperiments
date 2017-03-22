import sys
import json
import pprint
import plotMaker
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)


# running time per instance, collapsing on opt func
def runningtimesInstance(allfiles):
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
    if not instanceName == "":
        m = int(instanceName.split("_")[0])
        n = int(instanceName.split("_")[1])
        d = int(instanceName.split("_")[2])
        T = int(instanceName.split("_")[3])
        runtimes.append([m, n, d, T, instanceName, median(instanceTimes)])
    return runtimes

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
    return None

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

# running time per instance config, collapsing on opt func
def runningtimes(allfiles):
    runtimes = []
    instanceTimes = []
    instanceName = ""
    for filename in allfiles:
        currentInstance = getInstanceProps(filename)
        time = runningTime(filename)
        if time is not None:
            if time > 900:
                time = 900
            if instanceName == "":
                instanceName = currentInstance
            elif instanceName != currentInstance:
                m = int(instanceName.split("_")[0])
                n = int(instanceName.split("_")[1])
                d = int(instanceName.split("_")[2])
                T = int(instanceName.split("_")[3])
                runtimes.append([m, n, d, T, instanceName, instanceTimes])
                instanceTimes = []
                instanceName = currentInstance
            instanceTimes.append(time)
    if not instanceName == "":
        m = int(instanceName.split("_")[0])
        n = int(instanceName.split("_")[1])
        d = int(instanceName.split("_")[2])
        T = int(instanceName.split("_")[3])
        runtimes.append([m, n, d, T, instanceName, instanceTimes])
    return runtimes

def satUnsatNotsolvedProps(allfiles):
    stats = []
    instances = []
    currentProps = ""
    for name in allfiles:
        props = getInstanceProps(name)
        if currentProps == "":
            currentProps = props
        if currentProps != props:
            sat, unsat, unsolved = satVsUnsat(instances)
            instances = []
            m = int(currentProps.split("_")[0])
            n = int(currentProps.split("_")[1])
            d = int(currentProps.split("_")[2])
            T = int(currentProps.split("_")[3])
            stats.append([m, n, d, T, currentProps, len(sat), len(unsat), len(unsolved)])
            currentProps = props
        instances.append(name)
    sat, unsat, unsolved = satVsUnsat(instances)
    instances = []
    m = int(currentProps.split("_")[0])
    n = int(currentProps.split("_")[1])
    d = int(currentProps.split("_")[2])
    T = int(currentProps.split("_")[3])
    stats.append([m, n, d, T, currentProps, len(sat), len(unsat), len(unsolved)])
    return(stats)

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

def groupSatUnsatNotsolved(data,pos):
    sorteddata = sorted(data, key=itemgetter(pos))
    vals = [val[pos] for val in sorteddata]
    instanceNames = [val[4] for val in sorteddata]

    sat = [val[5] for val in sorteddata]
    unsat = [val[6] for val in sorteddata]
    notsolved = [val[7] for val in sorteddata]

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

    return sat, unsat, notsolved, instanceNames, vals, xlabel

def satVsUnsat(ipfiles):
    unsatFiles = []
    satFiles = []
    notsolved = []
    counter = 0
    for ip in ipfiles:
        sat = False
        unsat = False
        with open(ip, "r") as f:
            counter += 1
            for line in f.readlines():
                line = line.strip().split()
                if len(line) > 0 and line[0] == "Schedule:":
                    sat = True
                    # if len(satFiles) == 0 or satFiles[-1] != props:
                    satFiles.append(ip)
                elif len(line) > 0 and line[-1] == "IIS":
                    unsat = True
                    # if (len(unsatFiles) == 0 or unsatFiles[-1] != props):
                    unsatFiles.append(ip)

            if not sat and not unsat: #and (len(notsolved) == 0 or notsolved[-1] != props):
                notsolved.append(ip)
    return satFiles, unsatFiles, notsolved

def topercent(data,suma):
    percents = []
    for v in data:
        x = (v*100.0)/(suma*1.0)
        percents.append(x)
    print(percents)
    return percents

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
    ylabel = "Running Times (sec)"
    plotname = "Running time of CP and IP models"

    # plotMaker.oneBarMixed(cpdata,vals,xlabel,ylabel,"Running time of IP model","IP")
    # plotMaker.twoHistograms(cpdata, ipdata, vals, xlabel, ylabel)
    plotMaker.twoBoxPlots(ipdata, vals, xlabel, ylabel,"The IP model")
    #plotMaker.oneBar(ipdata,vals,xlabel,ylabel,"Running time of IP model","IP")

def compareOptFuncs(filenames):
    cpfiles, ipfiles = separateFiles(filenames)

    cost,duration,conn,flights = separateOptFuncs(ipfiles)
    costruntimes = runningtimesInstance(cost)
    durationruntimes = runningtimesInstance(duration)
    connruntimes = runningtimesInstance(conn)
    flightsruntimes = runningtimesInstance(flights)
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
    plotMaker.fourBars(costdata,flightsdata,durationdata,conndata, vals, xlabel,ylabel,"Running time per optimisation function")
    # plotMaker.histograms(costdata,durationdata,conndata,flightsdata,vals, xlabel, ylabel)

# returns a plot with one bar with number of unsat and one bar with number of sat instances
def compareSatvsUnsat(filenames):
    satFiles, unsatFiles, unsolved = satVsUnsat(filenames)

    print(satFiles)
    print(unsatFiles)
    xlabel = ""
    plotname = "SAT, UNSAT and unsolved TP instances"
    plotMaker.threeBarsOnce(len(satFiles), len(unsatFiles), len(unsolved), ["SAT", "UNSAT"], xlabel, "", plotname)

def satUnsatRuntimes(filenames):
    satFiles, unsatFiles, unsolved = satVsUnsat(filenames)
    satruntimes = runningtimes(satFiles)
    unsatruntimes = runningtimes(unsatFiles)
    pos = 3
    satdata, instanceNames, vals, xlabel = group(satruntimes, pos)
    unsatdata, instanceNames, vals, xlabel = group(unsatruntimes, pos)
    ylabel = "Running Times (sec)"
    plotname = "Running time of soluble TP instances"
    # plotMaker.oneBarMixed(cpdata,vals,xlabel,ylabel,"Running time of IP model","IP")
    # plotMaker.twoHistograms(satdata, unsatdata, vals, xlabel, ylabel)
    plotMaker.twoBoxPlots(satdata, vals, xlabel, ylabel,plotname)
    # plotMaker.oneBar(unsatdata,vals,xlabel,ylabel,plotname,"SAT")

# for every x files with the same properties, returns number of sat, unsat and not solved instances
def satUnsatUnsolvedPerProps(filenames):
    alles = satUnsatNotsolvedProps(filenames)
    pos = 0
    ylabel = "Percent of instances"
    plotname = "Properties of instances for each config"
    sat, unsat, notsolved, instanceNames, vals, xlabel = groupSatUnsatNotsolved(alles,pos)
    instancesPerConfig = sat[0] + unsat[0] + notsolved[0]
    satPercent = topercent(sat,instancesPerConfig)
    unsatPercent = topercent(unsat,instancesPerConfig)
    notsolvedPercent = topercent(notsolved,instancesPerConfig)
    plotMaker.customStackedBar(satPercent,unsatPercent,notsolvedPercent, vals, xlabel,ylabel,plotname)


# generates a cumulative bar with total configs, successful configs, sat and unsat instances
# todo: add numbers to the plot
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
satUnsatRuntimes(filenames)
# dataGeneratorStats(filenames, totalCount)
