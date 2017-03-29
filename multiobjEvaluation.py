import matplotlib.pyplot as plt
import pandas as pd
from numpy import random
from numpy.random import randn
from pandas.tools.plotting import scatter_matrix
import answersParser
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

# print(randn(10, 4))
# df = pd.DataFrame(randn(1000, 4), columns=['a', 'b', 'c', 'd'])
# axes = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
# plt.show()

def getmulti(answer):
    paretofront = []
    multisol = []
    with open(answer, "r") as f:
        for line in f.readlines():
            line = line.split()
            if len(line) == 0 and len(multisol) == 4:
                paretofront.append(multisol)
                multisol = []
            elif len(line) > 0 and (line[0] == "Cost:" or line[0] == "ConnectingF:" or line[0] == "TripD:" or line[0] == "FlightsNo:"):
                multisol.append(float(line[1]))
    return paretofront

def optsol(objective,answer):
    with open(answer, "r") as f:
        for line in f.readlines():
            line = line.split()
            if len(line) > 0 and line[0] == objective:
                return float(line[1])

def optsols(sols):
    mincost = None
    minflights = None
    minconn = None
    mintrip = None
    ipmulti = None
    cpmulti = None
    for sol in sols:
        ismulti = sol.split("_")[-3] == "multi"
        optfunc = sol.split("_")[-2]
        solver = sol.split("_")[-1]
        if solver == "ip":
            if optfunc == "cost":
                mincost = optsol("Cost:",sol)
            elif optfunc == "connections":
                minconn = optsol("ConnectingF:",sol)
            elif optfunc == "trip":
                mintrip = optsol("TripD:",sol)
            elif optfunc == "flights":
                minflights = optsol("FlightsNo:",sol)
            elif ismulti:
                ipmulti = getmulti(sol)
        elif solver == "cp" and ismulti:
            cpmulti = getmulti(sol)
    return mincost,minconn,mintrip,minflights,ipmulti,cpmulti

def makeInstancesDict(filenames):
    allinstances = {}
    currentName = ""
    solutions = []
    for answer in filenames:
        name = answersParser.getInstanceName(answer)
        if currentName == "":
            currentName = name
        elif not currentName == name:
            cost,conn,trip,flights,ipmulti,cpmulti = optsols(solutions)
            if not cost == None and not flights == None and not conn == None and not trip == None and not cpmulti == None and not ipmulti == None:
                allinstances[currentName] = [cost,conn,trip,flights,ipmulti,cpmulti]
            solutions = []
            currentName = name
        solutions.append(answer)
    cost,conn,trip,flights,ipmulti,cpmulti = optsols(solutions)
    if not cost == None and not flights == None and not conn == None and not trip == None and not cpmulti == None and not ipmulti == None:
        allinstances[currentName] = [cost,conn,trip,flights,ipmulti,cpmulti]
    return allinstances

filenames = []
with open("filenames", "r") as f:
    filenames = f.readline().strip().split(" ")
    dfiles = f.readline().strip().split(" ")
    for dfile in dfiles:
        filenames.append(dfile)

instances = makeInstancesDict(filenames)
pp.pprint(instances)
