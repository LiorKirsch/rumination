'''
Created on Apr 11, 2011

@author: noam
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.colors import cnames
from matplotlib import rcParams
from matplotlib import animation
from itertools import cycle 
from matplotlib.patches import Polygon
from matplotlib.pyplot import xticks
import statsmodels.api as sm # recommended import according to the docs
from collections import Counter
        
def init():
    # set plot attributes
    fig_width = 12  # width in inches
    fig_height = 9  # height in inches
    fig_size = [fig_width, fig_height]
    params = {'backend': 'Agg',
    'axes.labelsize': 22,
    'axes.titlesize': 20,
    'text.fontsize': 20,
    'legend.fontsize': 22,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'figure.figsize': fig_size,
    'savefig.dpi' : 600,
    'font.family': 'sans-serif'}
    rcParams.update(params)

def autolabel(rects, fontSize=24):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, '%.2f' % height,
                ha='center', va='bottom', fontsize=fontSize)
        
def bensErrBars(humansBen, humansStd, agentsBen, agentsStd, figName, labels=None):
    if not labels: labels = ['Human', 'Agent']
    init()
    locs = np.arange(1, 4)
    width = 0.33
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(locs + width / 2, humansBen, width=width, yerr=humansStd, ecolor='black', facecolor=cnames['darkcyan'], label=labels[0]);
    plt.bar(locs + width * 1.5, agentsBen, width=width, yerr=agentsStd, ecolor='black', facecolor=cnames['darkkhaki'], label=labels[1]);
    plt.xticks(locs + width * 1.5, locs);
    ax.set_xticklabels(['First Proposer', 'Second Proposer', 'Global'])
    plt.legend(loc="upper right")
    plt.ylabel('Benefit')
    plt.ylim([0, 160])
    plt.grid(True)
    # fig.autofmt_xdate()
    plt.show()    
    # plt.savefig('%s.svg'%figName)

def barPlot(x, yLabel='', xTickLabels='', ylim=None, xlim=None, labels=None, xLabelsFontSize=34, title='',
            doPlotValues=False, errors=None, xrotate=0, startsWithZeroZero=False):
    if not ylim: ylim = []
    if not xlim: xlim = []
    if not labels: labels = ['', '', '']
    if (errors is None): errors = []
    init()
    ind = range(len(x))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if (len(errors) == 0): errors = np.zeros((len(x)))
    rects = ax.bar(ind, x, facecolor='#777777', align='center', ecolor='black', yerr=errors)
    if (doPlotValues): autolabel(rects, 34)
    if (startsWithZeroZero):
        if (ylim): ylim[0]=0
        else: ylim = [0,max(x+1)]
        if (xlim): xlim[0]=-0.5
        else: xlim = [-0.5,len(x)]
    if (ylim): plt.ylim(ylim)
    if (xlim): plt.xlim(xlim)
    if (xTickLabels != ''):
        plt.xticks(ind);        
        ax.set_xticklabels(xTickLabels, fontsize=xLabelsFontSize)
#        plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=xLabelsFontSize)
    plt.ylabel(yLabel, fontsize=34)
    if (xrotate): plt.xticks(rotation=xrotate)    
    if (title != ''): 
        ax.set_title(title, fontsize=34)
#    fig.autofmt_xdate()
    # fig.autofmt_xdate()
    plt.show()    

def bens3GErrBars(x1Avg, x1Std, x2Avg, x2Std, x3Avg, x3Std, yLabel='Benefit', yLim=130, labels=None, xTickLabels=None,
                  errBars=True):
    if not labels: labels = ['SIGAL', 'EQ', 'People']
    if not xTickLabels: xTickLabels = ['Proposer in round 1', 'Proposer in round 2', 'Global']
    init()
    locs = np.arange(1, 4)
    eps = 0.01
    width = 0.25
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if (errBars):
        plt.bar(locs + width, x1Avg, width=width, yerr=x1Std, ecolor='black', facecolor=cnames['darkblue'], label=labels[0]);
        plt.bar(locs + width * 2 + eps, x2Avg, width=width, yerr=x2Std, ecolor='black', facecolor=cnames['green'], label=labels[1]);
        plt.bar(locs + width * 3 + eps * 2, x3Avg, width=width, yerr=x3Std, ecolor='black', facecolor=cnames['brown'], label=labels[2]);
    else:
        plt.bar(locs + width, x1Avg, width=width, facecolor=cnames['darkblue'], label=labels[0]);
        plt.bar(locs + width * 2 + eps, x2Avg, width=width, facecolor=cnames['green'], label=labels[1]);
        plt.bar(locs + width * 3 + eps * 2, x3Avg, width=width, facecolor=cnames['brown'], label=labels[2]);        
    plt.xticks(locs + width * 2.5, locs);
    ax.set_xticklabels(xTickLabels)
    plt.legend(loc="upper right")
    plt.ylabel(yLabel)
    plt.ylim([0, yLim])
    plt.grid(True)
    # fig.autofmt_xdate()
    plt.show()    
    # plt.savefig('%s.svg'%figName)

def twoBarsPlot(x1, x2, xlabel, ylabel, xtick1, xtick2):
    init()
    ind = np.arange(2)
    width = 0.33
    plt.bar(ind, [np.mean(x1), np.mean(x2)], width=width, yerr=[np.std(x1), np.std(x2)], ecolor='black', facecolor=cnames['darkcyan']);
    plt.xticks(ind + width / 2, [xtick1, xtick2]);
    plt.ylim([0, 1.5])
    plt.grid(True)
    # fig.autofmt_xdate()
    plt.show()    
    # plt.savefig('%s.svg'%figName)
    
def graph(x, y, title='', xlabel='', ylabel='', xlim=None, ylim=None, fileName='', yerr=None, yticks=None, xticks=None, doShow=True):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if (x is None): x = range(len(y))
    plt.plot(x, y, '-')
    if (yerr is not None):
        plt.errorbar(x, y, yerr)#, color='%s' % colors[i])  # , linestyle='-', label=labels[i])    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if (xlim is not None): plt.xlim(xlim)
    if (ylim is not None): plt.ylim(ylim)    
    if (yticks is not None):  ax.set_yticks(yticks)
    if (xticks is not None):  ax.set_xticks(xticks)
    if (fileName != ''):
        plt.savefig('%s.png' % fileName)
        plt.close()
    else:
        if (doShow): plt.show()        

def graph2(x, y1, y2, labels, xlim=None, title='', xlabel='', ylabel='', fileName='', legendLocation='upper right'):
    if not xlim: xlim = []
    plt.plot(x, y1, '-', label=labels[0])
    plt.plot(x, y2, '-', label=labels[1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if (xlim): plt.xlim(xlim)
    plt.legend(loc=legendLocation)
    if (fileName != ''):
        plt.savefig('%s.png' % fileName)
    plt.show()        
    
def graphN(x, ys, labels=None, yerrs=None, xlabel='', ylabel='', title='', legendLoc='upper right', xlim=None, ylim=None,
           fileName='', poster=True, doShow=True):
    if (yerrs is None): yerrs = []
    if (xlim is None): xlim = []
    if (ylim is None): ylim = []
    if (labels is None): labels = []
    yerrs=[[]]*len(ys)
    pp = []
    lines = cycle(['-']*len(ys)) if poster else linesCycler()
#    colors = ['r', 'b', 'g']
    for i, (y, yerr) in enumerate(zip(ys, yerrs)):
        p = plt.plot(x, y, next(lines), lw=4 if poster else 3)#, color='%s' % colors[i])
        pp.append(p[0])
        if (len(yerr)>0):
            plt.errorbar(x, y, yerr)#, color='%s' % colors[i])  # , linestyle='-', label=labels[i])
    if (len(labels)>0):
        plt.legend(pp, labels, loc=legendLoc, numpoints=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if (xlim): plt.xlim(xlim)
    if (ylim): plt.ylim(ylim)
    if (fileName != ''):
        plt.savefig('%s.png' % fileName)  
    else:  
        if (doShow): plt.show()        
    
def confInt(x, y, stds, label=''):
    y, stds = np.array(y), np.array(stds)
    plt.plot(x, y, '-', label=label)
    plt.fill(np.concatenate([x, x[::-1]]), \
        np.concatenate([y - stds, (y + stds)[::-1]]), \
        alpha=.5, fc='b', ec='None', label='95% confidence interval')    
    plt.legend()
    plt.show()
    
def scatterPlot(x, y, size=10, title='', xlabel='', ylabel=''):
    fig = plt.figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='-', color='0.75')
    ax.scatter(x, y, size, color='tomato');
    plt.show()
    # canvas.print_figure('revelationVSscore.png',dpi=500)

def histCalcAndPlot(x, min= -1, max= -1, binsNum=10, xlabel='', title=''):
    if (min == -1): min = np.min(x)
    if (max == -1): max = np.max(x) 
    bins = np.linspace(min, max, binsNum)
#    histPlot(x, bins)
    plt.hist(x, bins, alpha=0.5)
    plt.xlabel(xlabel)
    plt.title(title)    
    plt.xlim([min,max])
    plt.show()

def histCalcAndPlotN(X, binsNum=10, labels=None, xlabel='', title='', alpha=0.5):
    if not labels: labels = []
    mins, maxs = [], []
    for x in X:
        mins.append(np.min(x))
        maxs.append(np.max(x))
    bins = np.linspace(min(mins), max(maxs), binsNum)
    for i, x in enumerate(X):
        label = str(i) if labels==[] else labels[i]
        plt.hist(x, bins, alpha=alpha, label=label)
    plt.legend()
    plt.xlabel(xlabel)
    plt.title(title)    
    plt.show()


def histBarPlot(hist, bins):
    plt.bar(bins[:-1], hist)
    plt.show()
    
def setHistBarPlot(counter):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    plt.bar(range(len(counter)), counter.values())
    labels = []
    for key in counter.keys(): labels.append(str(key)) 
    ax.set_xticks(range(len(counter)))
    ax.set_xticklabels(counter.keys())
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=12)
    plt.show()

def histPlot(x, min, max, binsNum):
    bins = np.linspace(min, max, binsNum)
    plt.hist(x, bins, alpha=0.5)
    plt.show()
    
def twoHistsPlot(x1, x2, binsNum=10, label1='', label2='', xmin=None, xmax=None):
    if not xmin: xmin = []
    if not xmax: xmax = []
    if (not xmin): xmin = min([min(x1), min(x2)])
    if (not xmax): xmax = max([min(x1), max(x2)])
    bins = np.linspace(xmin, xmax, binsNum)
#    fig = plt.figure()
#    ax = fig.add_subplot(1, 1, 1)
    plt.hist(x1, bins, alpha=0.5, edgecolor='black', label=label1)
    plt.hist(x2, bins, alpha=0.5, edgecolor='black', label=label2)
    plt.legend()
#    ax.set_xticks(np.linspace(xmin,xmax,30))
#    plt.xticks(rotation=70)    
    plt.show()

def threeHistsPlots(x1, x2, x3, min, max, binsNum):
    bins = np.linspace(min, max, binsNum)
    plt.hist(x1, bins, alpha=0.9, facecolor='yellow', edgecolor='black')
    plt.hist(x2, bins, alpha=0.9, facecolor='blue', edgecolor='black')
    plt.hist(x3, bins, alpha=0.9, facecolor='red', edgecolor='black')
    plt.show()
    
    
def twoHistsPlot2(x1, x2, binsNum=10, xmin=None, xmax=None, label1='', label2='', title=''):
    if not xmin: xmin = []
    if not xmax: xmax = []
    if (not xmin): xmin = min([min(x1), min(x2)])
    if (not xmax): xmax = max([min(x1), max(x2)])
    bins = np.linspace(xmin, xmax, binsNum)  
    plt.subplot(111)
    hist1, bins1 = np.histogram(x1, bins)
    hist1 = float(hist1) / float(np.sum(hist1))
    center1 = (bins1[:-1] + bins1[1:]) / 2
    hist2, bins2 = np.histogram(x2, bins)
    hist2 = float(hist2) / float(np.sum(hist2))
    center2 = (bins2[:-1] + bins2[1:]) / 2
    width = 1.5
    plt.bar(center1, hist1, width, color='k', label=label1)
    plt.bar(center2 + width, hist2, width, color='w', label=label2)
    plt.legend()
    plt.title(title)
    plt.show()
    
def histMeans(x, y, binsNum=20):
    bins = np.linspace(np.min(x), np.max(x), binsNum)
    hist, bins = np.histogram(x, bins)
    centers = (bins[:-1] + bins[1:]) / 2
    ind = 0
    ymeans = []
    for itemsNum in hist:
        ymeans.append(np.mean(y[ind:ind + itemsNum]))
        ind += itemsNum + 1
    scatterPlot(centers, ymeans)
    
def regressionLine(x, y, yh):
    plt.scatter(x, y, 10, color='k');
    plt.scatter(x, yh, 10, color='tomato');
    # plt.plot(x, y, 'k', x, yh, 'r-')
    # plt.plot([x1, x2], [y1, y2], 'k')
    plt.show()

def scoresScatter(xProposer, yResponder, xLabel, yLabel, labels, markers=None):
    if not markers: markers = ['o', (5, 0), '>']
    init()
    fig = plt.figure()        
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xLabel, fontsize=14)
    ax.set_ylabel(yLabel, fontsize=14)
    ax.grid(True, linestyle='-', color='0.75')

    for ind, lab in enumerate(labels):
        plt.scatter(xProposer[ind], yResponder[ind], marker=markers[ind], s=100, label=lab)

#    for label, _x, _y in zip(['round 1', 'round 2', 'round 1', 'round 2'], xProposer, yResponder):
#        plt.annotate(label,
#                xy=(_x, _y), xytext=(-20, 20),
#                textcoords='offset points', ha='right', va='bottom',
#                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
#                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))    
    plt.legend(loc="upper left")
    plt.show()
    
def matShow(z,title=''):
#     fig = plt.figure()
#     surf = plt.matshow(z, cmap=plt.cm.hot)
#     fig.colorbar(surf, shrink=0.5, aspect=5)
#     if (title!=''): plt.title(title)
#     plt.show()

    fig = plt.figure()

    # Plot distance matrix.
    axmatrix = fig.add_axes([0.3,0.1,0.6,0.8])
    im = axmatrix.matshow(z, aspect='auto', origin='lower')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    
    # Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.8])
    plt.colorbar(im, cax=axcolor)

    if (title!=''): plt.title(title)
    
    # Display and save figure.
    fig.show()
    plt.show()

def linesCycler():
    return cycle(["--","-.",":","-","--"])

class Animate(object):

    def __init__(self, dataFunc):
        self.fig = plt.figure()
        self.ax = plt.axes()  # xlim=(0, 2), ylim=(-2, 2))
        self.line, = self.ax.plot([], [], lw=2)
        self.dataFunc = dataFunc
        
    def init(self):
        self.line.set_data([], [])
        return self.line,
    
    def animate(self, t):
        x, y = self.dataFunc(t)
        self.line.set_data(x, y)
        return self.line,
    
    def run(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=200, interval=20, blit=True)
    #    anim.save('basic_animation.mp4', fps=30)#, extra_args=['-vcodec', 'libx264'])
        plt.show()    
        
    
class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, data, lines, sizes, interval=10, lims=None, figureName='', movieName=''):
        if not lims: lims = [-10, 10, -10, 10]
        self.numpoints = data.shape[1]
        self.stream = self.data_stream()
        self.fig, self.ax = plt.subplots()
        self.linesNum = lines.shape[1]
        self.line = [None] * self.linesNum
        for i in range(self.linesNum):
            self.line[i], = self.ax.plot([], [], lw=2)
        self.data = data
        self.lines = lines
        self.sizes = sizes
        self.interval = interval
        self.lims = lims
        self.figureName = figureName
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=interval,
                                           init_func=self.setup_plot, blit=True)
        if (not movieName == ''):
            self.ani.save('%s.mp4' % movieName)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        points, _ = next(self.stream)
        plt.hold(True)
        self.scat = self.ax.scatter(points[:, 0], points[:, 1], c=self.sizes, s=self.sizes * 30, animated=True)
        self.ax.axis(self.lims)
        for i in range(self.linesNum):
            self.line[i].set_data([], [])
            self.line[i].set_color('b')
        ret = list([self.scat])
        for i in range(self.linesNum): ret.append(self.line[i])
        self.ax.get_xaxis().set_ticks([])
        self.ax.get_yaxis().set_ticks([])
        self.fig.canvas.set_window_title(self.figureName) 
        return ret

    def data_stream(self):
        for points, lines in zip(self.data, self.lines):
            yield points, lines
            
    def update(self, i):
        """Update the scatter plot."""
        points, lines = next(self.stream)
        self.scat.set_offsets(points)
        for i, line in enumerate(lines):
            self.line[i].set_data([line[0]], [line[1]])
        ret = list([self.scat])
        for i in range(self.linesNum): ret.append(self.line[i])
        return ret

    def run(self):
        plt.show()
        
def boxPlot(data,labels):
    fig, ax1 = plt.subplots(figsize=(10,6))
    fig.canvas.set_window_title('A Boxplot Example')
    plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
    
    bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    
    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.5)
    
    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
    ax1.set_xlabel('Distribution')
    ax1.set_ylabel('Value')
    
    # Now fill the boxes with desired colors
    boxColors = ['darkkhaki','royalblue']
    numBoxes = len(data)
    medians = range(numBoxes)
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(len(data)):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX,boxY)
        # Alternate between Dark Khaki and Royal Blue
        k = i % 2
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')
    
    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes+0.5)
    top = 40
    bottom = -5
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=np.repeat(labels, 2))
    plt.setp(xtickNames, rotation=45, fontsize=8)
    
    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes)+1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick,label in zip(range(numBoxes),ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top-(top*0.05), upperLabels[tick],
             horizontalalignment='center', size='x-small', weight=weights[k],
             color=boxColors[k])
    
    # Finally, add a basic legend
#     plt.figtext(0.80, 0.08,  str(N) + ' Random Numbers' ,
#                backgroundcolor=boxColors[0], color='black', weight='roman',
#                size='x-small')
#     plt.figtext(0.80, 0.045, 'IID Bootstrap Resample',
#     backgroundcolor=boxColors[1],
#                color='white', weight='roman', size='x-small')
#     plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
#                weight='roman', size='medium')
#     plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
#                size='x-small')
#     
    plt.show()    

def plotCDF(sample,xlim=None,title='', threshold=None):
    ecdf = sm.distributions.ECDF(sample)
    minSample = min(sample) if xlim is None else xlim[0]
    maxSample = max(sample) if xlim is None else xlim[1]
    x = np.linspace(minSample, maxSample)
    y = ecdf(x)
    if (threshold is not None):
        print('{} above threshold'.format(y[np.where(x>=threshold)[0][0]]))
    plt.step(x, y)
    if (xlim is not None): plt.xlim(xlim)
    plt.title(title)
    plt.show()   
    
def plotPie(x, labels=None, title='', explode=None, shadow=False, fileName=''):
    cnt = Counter(x)
    fracs = cnt.values()
    if (labels is None): labels = cnt.keys()
    plt.pie(fracs, explode, labels, autopct='%1.1f%%', shadow=shadow, startangle=90)
    plt.title(title)
    if (fileName != ''):
        plt.savefig('%s.png' % fileName)
        plt.close()
    else:
        plt.show()