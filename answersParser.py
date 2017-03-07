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

def groupByM(cpruntimes, ipruntimes):
    sortedcp = sorted(cpruntimes, key=itemgetter(0,1,2,3))
    sortedip = sorted(ipruntimes, key=itemgetter(0,1,2,3))

    mvals = [val[0] for val in sortedcp]
    instanceNames = [val[4] for val in sortedip]

    if len(mvals) != len(instanceNames):
        print("CP and IP number of results are not equal")
    cpdata = [val[5] for val in sortedcp]
    ipdata = [val[5] for val in sortedip]
    xlabel = "Number of Flights"
    return cpdata, ipdata, mvals, xlabel

def groupByN(cpruntimes, ipruntimes):
    sortedcp = sorted(cpruntimes, key=itemgetter(1,2,0,3))
    sortedip = sorted(ipruntimes, key=itemgetter(1,2,0,3))

    nvals = [val[1] for val in sortedcp]
    instanceNames = [val[4] for val in sortedip]

    if len(nvals) != len(instanceNames):
        print("CP and IP number of results are not equal")
    cpdata = [val[5] for val in sortedcp]
    ipdata = [val[5] for val in sortedip]
    xlabel = "Number of Airports"
    return cpdata, ipdata, nvals, xlabel

def groupByD(cpruntimes, ipruntimes):
    sortedcp = sorted(cpruntimes, key=itemgetter(2,0,1,3))
    sortedip = sorted(ipruntimes, key=itemgetter(2,0,1,3))

    dvals = [val[2] for val in sortedcp]
    instanceNames = [val[4] for val in sortedip]

    if len(dvals) != len(instanceNames):
        print("CP and IP number of results are not equal")
    cpdata = [val[5] for val in sortedcp]
    ipdata = [val[5] for val in sortedip]
    xlabel = "Number of Destinations"
    return cpdata, ipdata, dvals, xlabel

def groupByT(cpruntimes, ipruntimes):
    sortedcp = sorted(cpruntimes, key=itemgetter(3,0,1,2))
    sortedip = sorted(ipruntimes, key=itemgetter(3,0,1,2))

    tvals = [val[3] for val in sortedcp]
    instanceNames = [val[4] for val in sortedip]

    if len(tvals) != len(instanceNames):
        print("CP and IP number of results are not equal")
    cpdata = [val[5] for val in sortedcp]
    ipdata = [val[5] for val in sortedip]
    xlabel = "Holidat Time"
    return cpdata, ipdata, tvals, xlabel

filenames = sys.argv[1:]
cpfiles, ipfiles = separateFiles(filenames)
cpruntimes = runningtimes(cpfiles)
ipruntimes = runningtimes(ipfiles)

cpdata, ipdata, vals, xlabel = groupByN(cpruntimes, ipruntimes)
print(cpdata)
print(ipdata)
print(vals)
plotMaker.makePlots(cpdata, ipdata, vals, xlabel)

# parseForParallelPlot(cpdata, ipdata, instanceNames)
# plotMaker.parallelCoordinates(cpdata, ipdata)
