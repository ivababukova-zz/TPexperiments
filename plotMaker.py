import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas
import matplotlib.pyplot as plt
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pprint
import pandas as pd

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

def twoHistograms(a, b, x, xlabel, ylabel):
    fig, ax = plt.subplots()
    lw = 1
    ha = plt.plot(x, a, 'r-', linewidth=lw)
    hb = plt.plot(x, b, 'b-', linewidth=lw)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    # ax.set_yscale('log')
    ax.grid(True)
    ax.legend((ha[0], hb[0]), ('CP', 'IP'), loc='upper left')
    plt.show()

def histograms(a, b, c, d, x, xlabel, ylabel):
    fig, ax = plt.subplots()
    lw = 1
    ha = plt.plot(x, a, 'r-', linewidth=lw)
    hb = plt.plot(x, b, 'b-', linewidth=lw)
    hc = plt.plot(x, c, 'g-', linewidth=lw)
    hd = plt.plot(x, d, 'y-', linewidth=lw)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    # ax.set_yscale('log')
    ax.grid(True)
    ax.legend((ha[0], hb[0], hc[0], hd[0]), ('cost', 'duration', 'connections', 'flights'), loc='upper left')
    plt.show()

def twoBars(cpdata, ipdata, dvals, xlabel, ylabel, plotname):
    width = 0.5
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

# accepts data in this format:
#data = {
#     'config_name': ['MonteCarlo'],
#     'garbage': [garbageCount],
#     'unsat': [answersScale*totalUNSAT],
#     'sat': [answersScale*totalSAT]
# }
def stackedBar(raw_data):
    df = pd.DataFrame(raw_data, columns = ['config_name', 'garbage', 'unsat', 'sat'])
    # Create the general blog and the "subplots" i.e. the bars
    f, ax1 = plt.subplots(1, figsize=(10,5))

    # Set the bar width
    bar_width = 0.4

    # positions of the left bar-boundaries
    bar_l = [i+1 for i in range(len(df['garbage']))]

    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = [i+(bar_width/2) for i in bar_l]

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l,
        # using the pre_score data
        df['garbage'],
        # set the width
        width=bar_width,
        # with the label pre score
        label='Failed',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F4561D')

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l,
        # using the mid_score data
        df['unsat'],
        # set the width
        width=bar_width,
        # with pre_score on the bottom
        bottom=df['garbage'],
        # with the label mid score
        label='UNSAT',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F1911E')

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l,
        # using the post_score data
        df['sat'],
        # set the width
        width=bar_width,
        # with pre_score and mid_score on the bottom
        bottom=[i+j for i,j in zip(df['garbage'],df['unsat'])],
        # with the label post score
        label='SAT',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F1BD1A')

    # set the x ticks with names
    plt.xticks(tick_pos, df['config_name'])

    # Set the label and legends
    ax1.set_ylabel("Number of TP instances")
    ax1.grid(True)
    plt.legend(loc='upper left')

    # Set a buffer around the edge
    plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
    plt.show()

def twoBarsOnce(val1, val2, dvals, xlabel, ylabel, plotname):
    width = 0.5
    fig, ax = plt.subplots()
    rects1 = ax.bar(0, val1, width, color='r')
    rects2 = ax.bar(0 + width, val2, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(plotname)
    ylimits = (0,max(val1, val2) + 10)
    ax.set_xticks([])
    ax.set_ylim(ylimits) # sets the start and end points on the y axis
    ax.legend((rects1[0], rects2[0]), ('SAT', 'UNSAT'), loc='lower right')

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,
                    '%.f' % height,
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
