import sys
import json
import pprint
import plotMaker
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)

def runningtimesMin(allfiles):
    runtimes = []
    instanceTimes = []
    instanceName = ""
    for filename in allfiles:
        currentInstance = getInstanceProps(filename)
        time = runningTime(filename)
        if time > 900:
            time = 900
        if instanceName == "":
            instanceName = currentInstance
        elif instanceName != currentInstance:
            m = int(instanceName.split("_")[0])
            n = int(instanceName.split("_")[1])
            d = int(instanceName.split("_")[2])
            T = int(instanceName.split("_")[3])
            runtimes.append([m, n, d, T, instanceName, min(instanceTimes)])
            instanceTimes = []
            instanceName = currentInstance
        if time != None:
            instanceTimes.append(time)
    if not instanceName == "":
        m = int(instanceName.split("_")[0])
        n = int(instanceName.split("_")[1])
        d = int(instanceName.split("_")[2])
        T = int(instanceName.split("_")[3])
        runtimes.append([m, n, d, T, instanceName, min(instanceTimes)])
    return runtimes

def runningtimesMax(allfiles):
    runtimes = []
    instanceTimes = []
    instanceName = ""
    for filename in allfiles:
        currentInstance = getInstanceProps(filename)
        time = runningTime(filename)
        if time > 900:
            time = 900
        if instanceName == "":
            instanceName = currentInstance
        elif instanceName != currentInstance:
            m = int(instanceName.split("_")[0])
            n = int(instanceName.split("_")[1])
            d = int(instanceName.split("_")[2])
            T = int(instanceName.split("_")[3])
            if (d == 4):
                print("hoooray!")
                print(instanceTimes, max(instanceTimes))
            runtimes.append([m, n, d, T, instanceName, max(instanceTimes)])
            instanceTimes = []
            instanceName = currentInstance
        if time != None:
            instanceTimes.append(time)
    if not instanceName == "":
        if (d == 4):
            print("hoooray!")
            print(instanceTimes, max(instanceTimes))
        m = int(instanceName.split("_")[0])
        n = int(instanceName.split("_")[1])
        d = int(instanceName.split("_")[2])
        T = int(instanceName.split("_")[3])
        runtimes.append([m, n, d, T, instanceName, max(instanceTimes)])
    return runtimes

# running time per instance, collapsing on opt func
def runningtimesInstance(allfiles):
    runtimes = []
    instanceTimes = []
    instanceName = ""
    for filename in allfiles:
        currentInstance = getInstanceProps(filename)
        time = runningTime(filename)
        if time > 900:
            time = 900
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
        if time != None:
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
        time = runningTime(ip)
        with open(ip, "r") as f:
            counter += 1
            for line in f.readlines():
                line = line.strip().split()
                if len(line) > 0 and line[0] == "Schedule:":
                    sat = True
                    if time > 900:
                        print("not solved ", time, ip)
                        notsolved.append(ip)
                    else:
                        print("sat ", time, ip)
                        satFiles.append(ip)
                elif len(line) > 0 and (line[-1] == "IIS" or (line[0] == "No" and line[-1] == "found")):
                    unsat = True
                    if time > 900:
                        print("not solved ", time, ip)
                        notsolved.append(ip)
                    else:
                        print("unsat ", time, ip)
                        unsatFiles.append(ip)
            if not sat and not unsat:
                if time > 900:
                    print("not solved ", time, ip)
                    notsolved.append(ip)
                else:
                    print("unsat ", time, ip)
                    unsatFiles.append(ip)
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
    cpruntimesmin = runningtimesMin(cpfiles)
    ipruntimesmin = runningtimesMin(ipfiles)

    cpruntimes = runningtimesInstance(cpfiles)
    ipruntimes = runningtimesInstance(ipfiles)

    cpruntimesmax = runningtimesMax(cpfiles)
    ipruntimesmax = runningtimesMax(ipfiles)

    pos = 2
    cpdatamin, instanceNames, vals, xlabel = group(cpruntimesmin, pos)
    ipdatamin, instanceNames, vals, xlabel = group(ipruntimesmin, pos)

    cpdata, instanceNames, vals, xlabel = group(cpruntimes, pos)
    ipdata, instanceNames, vals, xlabel = group(ipruntimes, pos)

    cpdatamax, instanceNames, vals, xlabel = group(cpruntimesmax, pos)
    ipdatamax, instanceNames, vals, xlabel = group(ipruntimesmax, pos)

    ylabel = "Running Times (sec)"
    plotname = "Running time of CP and IP models"

    print("cpdatamin:")
    print(cpdatamin)
    print("cpdatamax:")
    print(cpdatamax)
    print("cpdata median:")
    print(cpdata)

    print("ipdatamin:")
    print(ipdatamin)
    print("ipdatamax:")
    print(ipdatamax)
    print("ipdata median:")
    print(ipdata)



    plotMaker.sixHistograms(cpdatamin, cpdata, cpdatamax, ipdatamin, ipdata, ipdatamax, vals, xlabel, ylabel)
    # plotMaker.oneBarMixed(cpdata,vals,xlabel,ylabel,"Running time of IP model","IP")
    # plotMaker.twoBars(cpdata, ipdata, vals, xlabel, ylabel, plotname)
    # plotMaker.twoHistograms(cpdata, ipdata, vals, xlabel, ylabel)
    # plotMaker.twoBoxPlots(cpdata, vals, xlabel, ylabel,"The CP model")
    #plotMaker.oneBar(ipdata,vals,xlabel,ylabel,"Running time of IP model","IP")

def compareOptFuncs(filenames):
    cpfiles, ipfiles = separateFiles(filenames)

    cost,duration,conn,flights = separateOptFuncs(ipfiles)
    costruntimes = runningtimesInstance(cost)
    durationruntimes = runningtimesInstance(duration)
    connruntimes = runningtimesInstance(conn)
    flightsruntimes = runningtimesInstance(flights)

    cpcost,cpduration,cpconn,cpflights = separateOptFuncs(cpfiles)
    cpcostruntimes = runningtimesInstance(cpcost)
    cpdurationruntimes = runningtimesInstance(cpduration)
    cpconnruntimes = runningtimesInstance(cpconn)
    cpflightsruntimes = runningtimesInstance(cpflights)

    pos = 2
    costdata, instanceNames, vals, xlabel = group(costruntimes, pos)
    durationdata, instanceNames, vals, xlabel = group(durationruntimes, pos)
    conndata, instanceNames, vals, xlabel = group(connruntimes, pos)
    flightsdata, instanceNames, vals, xlabel = group(flightsruntimes, pos)

    cpcostdata, instanceNames, vals, xlabel = group(cpcostruntimes, pos)
    cpdurationdata, instanceNames, vals, xlabel = group(cpdurationruntimes, pos)
    cpconndata, instanceNames, vals, xlabel = group(cpconnruntimes, pos)
    cpflightsdata, instanceNames, vals, xlabel = group(cpflightsruntimes, pos)
    print(costdata)
    print(durationdata)
    print(conndata)
    print(flightsdata)
    ylabel = "Running Times (sec)"

    plotMaker.eightHistograms(cpcostdata,cpflightsdata,cpdurationdata,cpconndata,costdata,flightsdata,durationdata,conndata, vals, xlabel, ylabel)
    # plotMaker.fourBars(costdata,flightsdata,durationdata,conndata, vals, xlabel,ylabel,"Running time per optimisation function")
    # plotMaker.histograms(costdata,durationdata,conndata,flightsdata,vals, xlabel, ylabel)

# returns a plot with one bar with number of unsat and one bar with number of sat instances
def numbofSatandUnsat(filenames):
    cpfiles, ipfiles = separateFiles(filenames)

    satFiles, unsatFiles, unsolved = satVsUnsat(ipfiles)

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

def compareSatUnsat(filenames):
    satFiles, unsatFiles, unsolved = satVsUnsat(filenames)

    satruntimesmin = runningtimesMin(satFiles)
    unsatruntimesmin = runningtimesMin(unsatFiles)

    satruntimes = runningtimesInstance(satFiles)
    unsatruntimes = runningtimesInstance(unsatFiles)

    satruntimesmax = runningtimesMax(satFiles)
    unsatruntimesmax = runningtimesMax(unsatFiles)

    pos = 3
    satmin, instanceNames, vals, xlabel = group(satruntimesmin, pos)
    unsatmin, instanceNames, bvals, xlabel = group(unsatruntimesmin, pos)

    sat, instanceNames, vals, xlabel = group(satruntimes, pos)
    unsat, instanceNames, bvals, xlabel = group(unsatruntimes, pos)

    satmax, instanceNames, vals, xlabel = group(satruntimesmax, pos)
    unsatmax, instanceNames, bvals, xlabel = group(unsatruntimesmax, pos)

    ylabel = "Running Times (sec)"
    plotname = "Running time of soluble and insoluble instances for the IP model"

    plotMaker.sixHistogramsSatUnsat(satmin, sat, satmax, unsatmin, unsat, unsatmax, vals, bvals, xlabel, ylabel)


def satUnsatCPIP(filenames):
    cpfiles, ipfiles = separateFiles(filenames)

    satcp, unsatcp, unsolvedcp = satVsUnsat(cpfiles)
    satip, unsatip, unsolvedip = satVsUnsat(ipfiles)

    pp.pprint(satip)
    pp.pprint(satcp)

    satcpruntime = runningtimesInstance(satcp)
    unsatcpruntime = runningtimesInstance(unsatcp)

    satipruntime = runningtimesInstance(satip)
    unsatipruntime = runningtimesInstance(unsatip)

    ylabel = "Running Times (sec)"
    pos = 2
    satcpdata, instanceNames, avals, xlabel = group(satcpruntime, pos)
    unsatcpdata, instanceNames, bvals, xlabel = group(unsatcpruntime, pos)
    satipdata, instanceNames, cvals, xlabel = group(satipruntime, pos)
    unsatipdata, instanceNames, dvals, xlabel = group(unsatipruntime, pos)

    print(satcpdata)
    print(satipdata)
    print(unsatcpdata)
    print(unsatipdata)

    plotMaker.fourHistograms(satcpdata, unsatcpdata, satipdata, unsatipdata, avals, bvals, cvals, dvals, xlabel, ylabel)
    # plotMaker.twoHistograms(satcpdata, satipdata, vals, xlabel, ylabel)

# for every x files with the same properties, returns number of sat, unsat and not solved instances
def satUnsatUnsolvedPerProps(filenames):
    cpfiles, ipfiles = separateFiles(filenames)

    alles = satUnsatNotsolvedProps(ipfiles)
    pos = 1
    ylabel = "Percent of instances"
    plotname = ""
    sat, unsat, notsolved, instanceNames, vals, xlabel = groupSatUnsatNotsolved(alles,pos)
    instancesPerConfig = sat[0] + unsat[0] + notsolved[0]
    satPercent = topercent(sat,instancesPerConfig)
    unsatPercent = topercent(unsat,instancesPerConfig)
    notsolvedPercent = topercent(notsolved,instancesPerConfig)
    plotMaker.customStackedBar(satPercent,unsatPercent,notsolvedPercent, vals, xlabel,ylabel,plotname)


filenames = sys.argv[1:]
# compareSatUnsat(filenames)
