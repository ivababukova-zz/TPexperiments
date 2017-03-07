import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas
import matplotlib.pyplot as plt
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pprint

pp = pprint.PrettyPrinter(indent=4)


def getMinMaxY(cpdata, ipdata):
    minYcp = min(cpdata)
    minYip = min(ipdata)
    minY = min(minYcp, minYip)
    maxYcp = max(cpdata)
    maxYip = max(ipdata)
    maxY = max(maxYcp, maxYip)
    return [0, maxY + 10] # change 0 with minY if needed

def parallelCoordinates(cpdata, ipdata):
    fig, ax = plt.subplots()
    ylimits = getMinMaxY(cpdata, ipdata)
    data = pandas.read_csv('parallel.csv', sep=',')
    parallel_coordinates(data, 'Name', color=['red','blue'])
    plt.show()

def twoBars(cpdata, ipdata, width, dvals, xlabel, ylabel, plotname):

    N = len(cpdata)
    ind = np.arange(N)  # the x locations for the groups

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, cpdata, width, color='r')
    rects2 = ax.bar(ind + width, ipdata, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(plotname)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(dvals)
    ylimits = getMinMaxY(cpdata, ipdata)
    ax.set_ylim(ylimits) # sets the start and end points on the y axis
    ax.legend((rects1[0], rects2[0]), ('CP', 'IP'), loc='upper left')

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,
                    '%.1f' % height,
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    plt.show()

def separateData(data):
    cpdata = []
    ipdata = []
    turn = "cp"
    for elem in data:
        elem = elem.strip("\"")
        if turn == "ip":
            ipdata.append(int(elem.strip("\"").strip("[,]")))
        if turn == "cp":
            cpdata.append(int(elem.strip("\"").strip("[,]")))
        if elem[-1] == "]":
            turn = "ip"
    return cpdata, ipdata

def makePlots(cpdata, ipdata, dvals, xlabel):
    width = 0.5 # the width of the bars
    ylabel = "Running Time (sec)"
    plotname = "Running time of CP and IP models"
    twoBars(cpdata, ipdata, width, dvals, xlabel, ylabel, plotname)

def makeCustomParallelPlot():
    cpdata = []
    ipdata = []
    with open("parallel.csv", "r") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            if line[-1] == "cp":
                cpdata.append([float(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4])])
            elif line[-1] == "ip":
                ipdata.append([float(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4])])

    x=[1,2,3,4,5] # spines

    fig,(ax,ax2,ax3,ax4) = plt.subplots(1, 4, sharey=False)

    for y1, y2 in zip(cpdata,ipdata):
        # plot the same on all the subplots
        ax.plot(x,y1,'r-',x,y2,'b-')
        ax2.plot(x,y1,'r-',x,y2,'b-')
        ax3.plot(x,y1,'r-',x,y2,'b-')
        ax4.plot(x,y1,'r-',x,y2,'b-')

    # now zoom in each of the subplots
    ax.set_xlim([x[0],x[1]])
    ax2.set_xlim([x[1],x[2]])
    ax3.set_xlim([x[2],x[3]])
    ax4.set_xlim([x[3],x[4]])

    # set the x axis ticks
    for axx,xx in zip([ax,ax2,ax3,ax4],x[:-1]):
      axx.xaxis.set_major_locator(ticker.FixedLocator([xx]))
    ax4.xaxis.set_major_locator(ticker.FixedLocator([x[-2],x[-1]]))  # the last one

    # EDIT: add the labels to the rightmost spine
    for tick in ax4.yaxis.get_major_ticks():
      tick.label2On=True

    # stack the subplots together
    plt.subplots_adjust(wspace=0)
    plt.show()

# makeCustomParallelPlot()
