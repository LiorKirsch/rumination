'''
Created on Mar 5, 2014

@author: noampeled
'''

import pickle
import os,sys
from dateutil.parser import parse 
from path3 import path
import numpy as np
import utils
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets.base import Bunch
from sklearn.feature_selection import SelectKBest, f_classif
import plots
import json
from collections import defaultdict
import scipy.optimize 
from sklearn.svm import SVC
from sklearn import preprocessing
import MLUtils
from sklearn.cross_validation import StratifiedShuffleSplit

FOLDERS = ('/Users/noampeled/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/amt3', 
           '/home/noam/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/amt3/')
BASE_DIR = [f for f in FOLDERS if os.path.exists(f)][0]

FIELDS = ('demographic','clicks','rumination','feedback','ip')
# RUMI_VALUES = {'Almost never':1, 'Sometimes':2, 'Often':3, 'Almost always':4}
RUMI_VALUES= {"disagree":1,"somewhat disagree":2,"somewhat agree":3,"agree":4}
TOPICS_VALUES = {"1-3 topics":1,"4-6 topics":2,"7-9 topics":3,"10 and more topics":4}

CATEGORIES = {-1:'control2', 0:'control',1:'narrow',2:'wide',3:'random'}
CATEGORIES_KTV = utils.keyToValues(CATEGORIES)
POS_Q = [2,4,6,8]
NEG_Q = [0,1,3,5,7]

BEST_COMB = [0, 3, 4, 5, 6, 7]

# POS_Q = [1, 2, 3, 4, 5, 7, 8]
# NEG_Q = [0, 6]

MIN_GAME_TD = 5
MIN_WORDS_TD = 20

TEST_RUMI, TEST_PANAS = range(2)
TEST = TEST_PANAS

def formatLogKey(key,val):
    if (key=="click_times"):
        return calcTimeDiffs(val).__str__()
    else:
        return '{}: {}'.format(key,val)

def formatLogFileToStr(log,field):
    ret = '{}:\n'.format(field)
    ret += ', '.join([formatLogKey(key, val) for key,val in sorted(log.iteritems())])
    ret+='\n\n'
    return ret

def formatLogFile(log,field,options=()):
    if (field=='clicks'):
        return calcTimeDiffs(log['click_times'])
    elif (field=='rumination'):
        return calcRumiScore(log,options)
    elif (field=='demographic'):
        return Bunch(**log)
    elif(field=='categoryID'):
        return int(log[field])
#     
#     'age'=log['age'],'categoryID'=log['categoryID'],'condition'=log['condition'],'education'=log['education'],'fromAmazon'=log['fromAmazon'],
#                      'gender'=log['gender'],'motherTongue'=log['motherTongue'],'workerID')=log['workerID'])
    else:
        return [(key, val) for key,val in sorted(log.iteritems())]

def calcRumiScore(log,options=()):
    if (TEST == TEST_RUMI):
        negAnswers = [RUMI_VALUES[log[q]] for q in ['Q1RB','Q2RB','Q4RB','Q6RB']]
        posAnswers = [RUMI_VALUES[log[q]] for q in ['Q3RB','Q5RB']]
        posAnswers.append(TOPICS_VALUES[log['Q7RB']])
        negAnswers.append(int(log['q8'])*3.0/10+1)  # normalize to 1-4
        posAnswers.append(int(log['q9'])*3.0/10+1)  # normalize to 1-4
        posAnswers, negAnswers = np.array(posAnswers),np.array(negAnswers)
        if ('getAllScores' in options):
            scores =  [RUMI_VALUES[log[q]] for q in ['Q1RB','Q2RB','Q3RB','Q4RB','Q5RB','Q6RB']]
            scores.append(TOPICS_VALUES[log['Q7RB']])
            scores.append(int(log['q8'])*3.0/10+1)  # normalize to 1-4
            scores.append(int(log['q9'])*3.0/10+1)  # normalize to 1-4
            return np.array(scores) 
        elif ('onlyRB' in options):
            scores = [RUMI_VALUES[log[q]] for q in ['Q1RB','Q2RB','Q3RB','Q4RB','Q5RB','Q6RB']]
            scores.append(TOPICS_VALUES[log['Q7RB']])
            return np.array(scores)        
        else:
            return sum(negAnswers) + sum(5-posAnswers)
    elif (TEST == TEST_PANAS):
        answers = [int(log[q]) for q in log.keys() if q[0]=='q']
        if ('getAllScores' in options or 'onlyRB' in options):
            return answers
        else:
            return sum(answers)
    else:
        utils.throwException('invalid test')
def calcTimeDiffs(clicks):
#     for clickTime in clicks.split(','): 
#         print('{} - {}'.format(clickTime,parse(clickTime)))
    times = clicks.split(',')
    deltas = [(parse(t)-parse(times[i-1])).total_seconds() for i,t in enumerate(times) if i>0]
    return deltas
    
def readLog(uuid,fields=FIELDS,options=(),printLogs=False):
    data = {}
    for field in fields:
        fileName = os.path.join(BASE_DIR, '{}_{}.pkl'.format(uuid,field))
        try:
            with open(fileName, 'r') as pklFile:
                log = pickle.load(pklFile)
                if (printLogs):
                    print(formatLogFileToStr(log,field))
                data[field] = formatLogFile(log,field,options)
        except IOError as err:
            if (field not in ['displayWords','game']):
                print(err)
#             print ('No file for {} ({})'.format(field,err.strerror))
        except Exception, err:
            print (err)
    return data

def readLogs(fields=FIELDS,options=()): 
    uuids = set(f.name[:5] for f in path(BASE_DIR).files('*feedback.pkl')) 
#     print('{} logs'.format(len(uuids)))
    data=[]
    for uuid in uuids:
        log = readLog(uuid,fields,options)
        log['uuid']=uuid
        data.append(log)
    return data

def calcRuminationEffect(logs):
    data = defaultdict(list)
    errors = defaultdict(int)
    validLogs=0
    for log in logs:
        if (isValidLog(log,errors)):
            cat = CATEGORIES[log['categoryID']]
            data[cat].append(log['rumination'])
            validLogs=validLogs+1
    
    print('{} valid logs out of {}'.format(validLogs,len(logs)))
    print(errors)
    for k in data.keys():
        print('{} of {}'.format(len(data[k]),k))
    utils.printTtestResultDict(data)
#     boxplot([narrow,wide,random],['narrow','wide','random'])
#     plots.boxPlot([narrow,wide,random],['narrow','wide','random'])
 
def isValidLog(log,errors):
    validMT = isValidMT(log)
    validRumi = isValidRumi(log,0)
    validClicks = isValidClicks(log,MIN_WORDS_TD) 
    validGame = isValidGame(log,MIN_GAME_TD)  
    if (not validMT): errors['mt']=errors['mt']+1 
    if (not validRumi): errors['rumi']=errors['rumi']+1
    if (not validClicks): errors['clicks']=errors['clicks']+1
    if (not validGame): errors['game']=errors['game']+1
    return validMT and validClicks  and validGame and validRumi

def isValidMT(log):
    return log['demographic']['motherTongue'][0]=='en'

def isValidRumi(log, minEnt=0, doPrint=False):
    workerID, cat = log['demographic']['workerID'][0],CATEGORIES[log['categoryID']]
#     if (workerID=='A3SPYHC5V0ZPX1'):
#         scores = readLog(log['uuid'],['rumination'],'getAllScores')['rumination']
#         print(scores)
    rumi = readLog(log['uuid'],['rumination'],'onlyRB')['rumination']
    ent = utils.entropy(rumi)
    if (ent<=minEnt and doPrint):
        print('{}, category {}, has low entropy!'.format(workerID, cat))
#         print(rumi)
    return ent>minEnt

def isValidClicks(log,maxTimeDiff=20,doPrint=False):
    workerID, cat = log['demographic']['workerID'][0],CATEGORIES[log['categoryID']]
#     if (workerID=='A3G4SJREB8K0BG'):
#         clicks = calcTimeDiffs(log['displayWords'][0][1])
#         print(clicks)    
    validClicks = True
    if ('displayWords' in log):
        clicks = calcTimeDiffs(log['displayWords'][0][1])
        validClicks = checkClicks(clicks,maxTimeDiff)
        if (not validClicks and doPrint):
            print('{}, category {}, has long clicks!'.format(workerID, cat))
#             print(clicks)  
    return validClicks   
              
def checkClicks(clicks, maxTimeDiff=20,doPrint=False):
    return np.all([c<maxTimeDiff for c in clicks])
#     return np.array([np.all(np.array(c)<threshold) for c in clicks])

def isValidGame(log,maxTimeDiff=20,doPrint=False):
    workerID, catID = log['demographic']['workerID'][0],log['categoryID']
    cat = CATEGORIES[catID]
    if (catID==-1): 
        return True   
#     if (workerID=='A275X9MSOS8O46'):
#         data = json.loads(log['game'][0][1])[0]
#         print(data['max_time_diff'])
    if ("game" not in log):
        print('{}, category {}, has no game log!'.format(workerID, cat))
        return False
    try:
        data = json.loads(log['game'][0][1])[0]
        validGame = data['max_time_diff']<maxTimeDiff
        if (not validGame and doPrint):
            print('{}, category {}, has long clicks in the game!'.format(workerID, cat))
    #         print(data['max_time_diff'])  
        return validGame
    except:
        print('{}, category {}, error in reading the game log!'.format(workerID, cat))


def findSignificantRuminationTestCombination(logs, doPrint=True):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs,[1,2])
    if (doPrint): print(utils.count(categoryIDs))
    foldsNum=2
    psTests,psTrains = [],[]
#     ruminationScores,idx = MLUtils.shuffle(ruminationScores)
#     categoryIDs = categoryIDs[idx]
    cv = StratifiedShuffleSplit(categoryIDs,foldsNum,1.0/foldsNum,random_state=0)
    for fold, (train_index, test_index) in enumerate(cv):
        if (doPrint): print('fold {}'.format(fold))
        xtrain, ytrain = ruminationScores[train_index,:], categoryIDs[train_index]
        xtest, ytest = ruminationScores[test_index,:], categoryIDs[test_index]
        if (doPrint): print(utils.count(ytrain))
        if (doPrint): print(utils.count(ytest))
        psTrain,minCombs=calcRuminationTTestForCombinations(xtrain, ytrain,doPlot=False,doPrint=False,combsType='all')
        psTest = testRuminationScoresComb(xtest, ytest, minCombs, doPrint)
        psTests.append(psTest)
        psTrains.append(psTrain)
#     pneg=calcRuminationTTestForCombinations(ruminationScores, categoryIDs, combsType='neg')
#     ppos=calcRuminationTTestForCombinations(ruminationScores, categoryIDs, combsType='pos')
#     print(pall,pneg,ppos)
    psTrains=np.array(psTrains)
    psTests=np.array(psTests)
    qRange = range(ruminationScores.shape[1])  
#     plotPValsForQNum(qRange,np.mean(psTrains,0),'train',np.std(psTrains,0))
    plotPValsForQNum(qRange,np.mean(psTests,0),'test',np.std(psTests,0))
    if (doPrint): print(np.mean(psTests,0))
    psAllTrain,minCombsAllTrain = calcRuminationTTestForCombinations(ruminationScores, categoryIDs,doPlot=True,doPrint=True,combsType='all')
    calcControlComb(ruminationScores, categoryIDs, minCombsAllTrain)
#     plotPValsForQNum(qRange,psAllTrain,'all train',np.std(psAllTrain,0))
    return np.min(np.mean(psTests,0))

def testRuminationScoresComb(ruminationScores,categoryIDs,combs,doPrint=True):
    ps = []
    for comb in combs:
        ruminationNew = sumRuminationScores(ruminationScores, comb=comb)        
        narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
        if (doPrint): print(len(comb),comb)
        _,p = utils.printTtestResult(narrow,wide, 'narrow', 'wide', doPrint)
        ps.append(p)
    return ps

def calcControlComb(ruminationScores, categoryIDs, combs,doPrint=True):
    pns,pws = [],[]
    controlRuminationScores,_ = calcRuminationScoresAndCategories(logs,[0])
    for comb in combs:
        control = sumRuminationScores(controlRuminationScores, comb=comb) 
        ruminationNew = sumRuminationScores(ruminationScores, comb=comb)
        narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
        if (doPrint): print(len(comb),comb)
        _,pn = utils.printTtestResult(narrow,control, 'narrow', 'control', doPrint)
        _,pw = utils.printTtestResult(wide,control, 'narrow', 'control', doPrint)
        pns.append(pn)
        pws.append(pw)
    qRange = range(ruminationScores.shape[1])
    plots.graphN(qRange,[pns,pws], ['control-narrow','control-wide'], ylim=[0,1],doShow=False)
    plots.plt.plot(qRange, [0.05] * len(qRange), 'r--')
    plots.plt.show()
        
def fitRuminationScores(logs):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs)
    selector = SelectKBest(f_classif, k=9) 
    selector.fit(ruminationScores,categoryIDs)
    print('fit:')
    print(selector.scores_)
    scoresOrder = np.argsort(selector.scores_)[::-1]
    print(scoresOrder)
    calcRuminationForDifferentQuestionsSubsets(ruminationScores,categoryIDs,scoresOrder)
    

def calcRuminationForDifferentQuestionsSubsets(ruminationScores,categoryIDs,scoresOrder,doPlot=True):
    qRange = range(1,len(scoresOrder)+1)
    ps = []
    for k in qRange:
        print(scoresOrder[:k])
        ruminationNew = sumRuminationScores(ruminationScores, comb=scoresOrder[:k])        
        narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
        _,p = utils.printTtestResult(narrow,wide, 'narrow', 'wide')
        ps.append(p)
    if (doPlot):
        plots.graph(qRange, ps, title='min pval for different subsets', xlabel='#questions', ylabel='minimum p-value',doShow=False)
        plots.plt.plot(qRange, [0.05] * len(qRange), 'r--')
        plots.plt.show()


def calcRuminationScoresAndCategories(logs, categoriesToDiffretiate = [1,2]):
    ruminationScores,categoryIDs = [],[]  
    errors = defaultdict(int)
    validLogs,totalLogs=0,0
    for log in logs:
        workerID, cat = log['demographic']['workerID'][0],log['categoryID']
        if (cat==CATEGORIES_KTV['control']):
            if ('displayWords' in log):
                print('*** displayWords in control!')
        if (cat in categoriesToDiffretiate):
            totalLogs = totalLogs+1
            if (isValidLog(log,errors)):
                validLogs=validLogs+1
                rumiScores = readLog(log['uuid'],['rumination'],'getAllScores')['rumination']
                ruminationScores.append(rumiScores)
                categoryIDs.append(cat)
    print('{} valid logs out of {}'.format(validLogs,totalLogs))
    print(errors)
    ruminationScores = np.array(ruminationScores)
    categoryIDs = np.array(categoryIDs)
    return (ruminationScores,categoryIDs)

#     calcNewRuminationTTest(ruminationScores, categoryIDs)
        
def sumRuminationScores(scores,posQ=POS_Q,negQ=NEG_Q,comb=None):
    scores = np.array(scores)
    if (comb is None): comb = range(scores.shape[1])
    posIndices = list(set(posQ).intersection(set(comb)))
    negIndices = list(set(negQ).intersection(set(comb)))
    combScores = np.hstack((scores[:,negIndices],5-scores[:,posIndices]))
    score = np.sum(combScores,1)
    return score

def weightsSumRuminationScores(scores,w,posQ,negQ,comb=()):
    return sumRuminationScores(w*scores,posQ,negQ,comb)

def calcRumiClicksHist():
    clicks, maxTimeDiffs = [],[]
    logs = readLogs(['displayWords'])
    for log in logs:
        if ('displayWords' in log):
            hitClicks = calcTimeDiffs(log['displayWords'][0][1])
            clicks.extend(hitClicks)
            maxTimeDiffs.append(max(hitClicks))
#     clicks = np.array(clicks)
#     clicksMax = np.min(clicks)+2*np.std(clicks)
#     print('{} above {}'.format(sum(clicks<clicksMax)/float(len(clicks)),clicksMax))
# #     plots.histCalcAndPlot(clicks,min=14,max=clicksMax, binsNum=50, title='mason words clicks diffs')
    clicks = np.array(clicks) - 15.6 # 15.6 is the time it take to present a words chain
    maxTimeDiffs = np.array(maxTimeDiffs) - 15.6
#     plots.plotCDF(clicks,(0,20),threshold=MIN_WORDS_TD-15.6)
#     plots.histCalcAndPlot(clicks, min=0, max=10, binsNum=50)
#     plots.plotCDF(maxTimeDiffs,threshold=MIN_WORDS_TD-15.6)
    plots.histCalcAndPlot(maxTimeDiffs, min=0, max=20, binsNum=50)


def calcRumiScoresHist(logs):
    ruminationScores=[]
    validRuminationScores,categoryIDs= calcRuminationScoresAndCategories(logs)
    for log in logs:
        ruminationScores.append(log['rumination'])
    ruminationScores = np.array(ruminationScores)
    validRuminationScoresSum = sumRuminationScores(validRuminationScores)
    validRuminationScoresComb = sumRuminationScores(validRuminationScores,comb=BEST_COMB)
#     plots.histCalcAndPlot(validRuminationScoresSum, binsNum=30)
#     plots.histCalcAndPlot(validRuminationScoresComb, binsNum=30)
    plots.histCalcAndPlotN([validRuminationScoresSum[categoryIDs==1],validRuminationScoresSum[categoryIDs==2]], binsNum=30, labels=['narrow','wide'])
    plots.histCalcAndPlotN([validRuminationScoresComb[categoryIDs==1],validRuminationScoresComb[categoryIDs==2]], binsNum=30, labels=['narrow','wide'])
    plots.plotCDF(validRuminationScoresSum, title='valid rumination scores CDF')
    plots.plotCDF(ruminationScores,title='rumination scores CDF')

def barPlotCategoriesSocres(logs):
    catRange = [1,2,0,-1]
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs,catRange)
    ruminationScoresSum = sumRuminationScores(ruminationScores,comb=BEST_COMB)
    x,err=[],[]
    data={}
    for cat in catRange:  
        data[CATEGORIES[cat]] = ruminationScoresSum[categoryIDs==cat]
        x.append(np.mean(ruminationScoresSum[categoryIDs==cat]))
        err.append(np.std(ruminationScoresSum[categoryIDs==cat]))
    utils.printTtestResultDict(data)
    plots.barPlot(x, 'rumination score', xTickLabels=[CATEGORIES[cat] for cat in catRange],errors=err)

def calcGameClicksHist(logs):
    timeDiffs,dists,maxTimeDiffs,times,clicks=[],[],[],[],[]
    notValid=0
    for log in logs:
#         if (isValidClicks(log) and isValidMT(log) and isValidRumi(log)):
        data = json.loads(log['game'][0][1])[0]
        timeDiffs.extend(data['times_diff'])
        dists.append(data['distance'])
        maxTimeDiffs.append(data['max_time_diff'])
        times.extend(np.cumsum(data['times_diff']))
        clicks.append(data['clicks'])
        if (data['max_time_diff']<MIN_GAME_TD): notValid+=1
#             if (max(np.cumsum(data['times_diff']))>300):
#                 print(max(np.cumsum(data['times_diff'])),data['max_time_diff'],data['times_diff'][0],data['times_diff'][-1],data['clicks'])

    print('{} out of {} are invalid'.format(notValid,len(logs)))
    timeDiffs = np.array(timeDiffs)
    maxTD = 5# np.mean(timeDiffs)+2*np.std(timeDiffs)
#     plots.histCalcAndPlot(timeDiffs,min=0,max=maxTD, title='timeDiffs',binsNum=50)
#     plots.plotCDF(timeDiffs,xlim=[0,maxTD+2], threshold=MIN_GAME_TD)
    plots.plotCDF(maxTimeDiffs, xlim=[0,10], threshold=MIN_GAME_TD)
#     plots.histCalcAndPlot(timeDiffs, 0, np.min(timeDiffs)+2*np.std(timeDiffs), title='timeDiffs',binsNum=100)
#     plots.histCalcAndPlot(times,0,300, title='times',binsNum=100)
#     plots.histCalcAndPlot(maxTimeDiffs, title='maxTimeDiffs',binsNum=50)
#     plots.histCalcAndPlot(dists, title='dists',binsNum=50)

def allCategoriesDiffrentation(logs):
    ruminationScores,categoryIDs= calcRuminationScoresAndCategories(logs,range(4))
    cnt = utils.count(categoryIDs)
    for k,v in cnt.iteritems():
        print('{}: {}'.format(CATEGORIES[k],v))


# def boxplot(groups,labels):
# #     ttestResults = utils.printTtestResult(baseline, effects, 'baseline', 'ruminatives', False)
#     sns.set(style="nogrid", context="poster")
#     colors = sns.color_palette(None, len(groups))
#     ax = sns.boxplot(groups,color=colors)
#     ax.set_xticklabels(labels)
# #     plt.title(ttestResults)
#     plt.show()  

# def calcRuminationScores():
#     data = readLogs(['categoryID','demographic','displayWords','game','rumination'],['onlyRB'])
#     demographic = [log['demographic'] for log in data]
#     engInds = np.array([demo.motherTongue[0] for demo in demographic])=='en'
#     ruminationScores = np.array([log['rumination'] for log in data])
#     entro = calcRuminationScoresEntropy(ruminationScores)
#     entroInds = entro>0
#     print('{} logs'.format(ruminationScores.shape[0]))
#     print('{} were ruled out because of low entropy!'.format(ruminationScores.shape[0]-sum(entroInds)))
#     print('{} were ruled out because of their mother tongue!'.format(ruminationScores.shape[0]-sum(engInds)))
#     print('{} were ruled out because of their slow clicks!'.format(ruminationScores.shape[0]-sum(validClicks)))
# 
#     validInds = entroInds & validClicks & engInds
#     ruminationScores = ruminationScores[validInds,:]
#     categoryIDs = np.array(categoryIDs)[validInds]
#     print('{} valid subjects'.format(sum(validInds)))
#     print('{} narrow, {} wide, {} random and {} did not see the words'.format(sum(categoryIDs==1), sum(categoryIDs==2),sum(categoryIDs==3),sum(categoryIDs==0)))
# 
# #     sawWords = np.array([0 if len(c)==0 else 1 for c in clicks])
# #     rumination = np.sum(ruminationScores,1) 
# #     utils.printTtestResult(rumination[sawWords==1], rumination[sawWords==0], 'sawWords', 'noWords')
# #     utils.printTtestResult(rumination[categoryIDs==1], rumination[categoryIDs==2], 'narrow', 'wide')
    
    
#     selector = SelectKBest(f_classif, k=5) 
#     selector.fit(ruminationScores,categoryIDs)
#     print(selector.scores_)
#     calcRuminationTTestForCombinations(ruminationScores, categoryIDs)
#     calcNewRuminationTTest(ruminationScores, categoryIDs)

def calcRuminationScoresEntropy(ruminationScores):
    entro = []
    for rumi in ruminationScores:
        entro.append(utils.entropy(rumi))
    return np.array(entro)


def calcRuminationTTestForCombinations(ruminationScores, categoryIDs, posQ=POS_Q, negQ=NEG_Q, combsType='all', doPlot=True, doPrint=True, w=None):
    ps,minCombs = [],[]
    if (w is None): w = np.ones((1,ruminationScores.shape[1]))
    if (combsType=='all'):
        qgroup = range(ruminationScores.shape[1])  
    elif (combsType=='neg'):
        qgroup = NEG_Q
    elif (combsType=='pos'):
        qgroup = POS_Q

    qRange = range(1,len(qgroup)+1)
    for l in qRange:
        combs = itertools.combinations(qgroup,l)
        minp=1
        mincomb=None
        for comb in combs:
            ruminationNew = weightsSumRuminationScores(ruminationScores, w, posQ, negQ, comb)         
            narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
            _, p = utils.ttestCond(narrow,wide)
            if (p<minp): 
                minp=p
                mincomb=comb
        ps.append(minp)
        minCombs.append(mincomb)
        if (mincomb is not None):
            ruminationNew = weightsSumRuminationScores(ruminationScores, w, posQ, negQ, mincomb)        
            narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
            if (doPrint): 
                print(l,np.array(mincomb))
                utils.printTtestResult(narrow,wide, 'narrow', 'wide')
        else:
            print('no combination with p<1')
    if (doPlot):
        plotPValsForQNum(qRange,ps,'min pval for different combinations ({})'.format(combsType))
    return ps,minCombs

def plotPValsForQNum(qRange,ps,title='',yerr=None):
    plots.graph(qRange, ps, title=title,ylim=[0,1],yticks=np.linspace(0, 1, 11), xlabel='#questions', ylabel='minimum p-value',yerr=yerr,doShow=False)
    plots.plt.plot(qRange, [0.05] * len(qRange), 'r--')
    plots.plt.show()
    
def calcRuminationTTestForCombinationsWeights(w,ruminationScores, categoryIDs, posQ=POS_Q, negQ=NEG_Q, combsType='all', doPlot=False, doPrint=False):
    return calcRuminationTTestForCombinations(ruminationScores, categoryIDs, posQ, negQ, combsType, doPlot, doPrint, w)

def calcWeightsForRuminationTest(logs):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs)
    w0 = np.ones((1,ruminationScores.shape[1]))
    res = scipy.optimize.minimize(calcRuminationTTestForCombinationsWeights, w0, (ruminationScores,categoryIDs),options={'disp': True})
    utils.save(res, 'optimizationResults')

def calcWeightsCombsForRuminationTest(logs):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs)
    wordsLenRange = range(1,ruminationScores.shape[1]+1)
    pmin = 1
    for l in wordsLenRange:
        print(l)
        combs = itertools.combinations(range(ruminationScores.shape[1]),l)
        for comb in combs:
            posQ = comb
            negQ = list(set(range(ruminationScores.shape[1]))-set(posQ))

            ruminationNew = sumRuminationScores(ruminationScores, posQ, negQ)        
            narrow,wide = ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2]
            print(posQ,negQ)
            _, p = utils.ttestCond(narrow,wide)
                        
#             p = calcRuminationTTestForCombinations(ruminationScores, categoryIDs, posQ, negQ, combsType='all', doPlot=False, doPrint=False, w=None)
            if (p<pmin):
                pmin=p
                best_pos = POS_Q
                best_neg = NEG_Q
    print(pmin,best_pos,best_neg)
   
def calcSVMWeightsForRuminationTest(logs):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs)
    categoryIDs = categoryIDs-1
    svc = SVC(C=1,kernel='linear')
    scaler = preprocessing.StandardScaler().fit(ruminationScores)
    ruminationScores = scaler.transform(ruminationScores)
    model = svc.fit(ruminationScores,categoryIDs)
    ypred = svc.predict(ruminationScores)
    MLUtils.calcConfusionMatrix(categoryIDs, ypred, ('narrow','wide'),True)
    print(model)
    

def calcNewRuminationTTest(ruminationScores,categoryIDs):
    inds = np.where((categoryIDs==1) | (categoryIDs==2))[0]
    ruminationScores = ruminationScores[inds,:]
    categoryIDs = categoryIDs[inds]
    print(len(categoryIDs))
    print(utils.count(categoryIDs))
    for k in range(ruminationScores.shape[1],0,-1):
        print(k)
        selector = SelectKBest(f_classif, k) 
        selector.fit(ruminationScores,categoryIDs)
        print(selector.get_support(True))
        ruminationScoresNew = selector.transform(ruminationScores)
        ruminationNew = np.sum(ruminationScoresNew,1) 
        utils.printTtestResult(ruminationNew[categoryIDs==1], ruminationNew[categoryIDs==2], 'narrow', 'wide')
        utils.printTtestResult(ruminationNew[categoryIDs==1], ruminationNew[categoryIDs!=1], 'narrow', 'others')
        utils.printTtestResult(ruminationNew[categoryIDs!=0], ruminationNew[categoryIDs==0], 'sawWords', 'noWords')

def readFat():
    fats = set(f for f in path(BASE_DIR).files('*fat.pkl')) 
    for fileName in fats:
        with open(fileName, 'r') as pklFile:
            log = pickle.load(pklFile)
            data = json.loads(log["data"])
            print (fileName)
            print (data)
#             print (json.dumps(data, sort_keys=True, indent=4))
#             print(data)

def someLie(logs):
    global MIN_WORDS_TD,MIN_GAME_TD
    minp = 1
    bestRumiDiff, bestGameDiff = 0,0
    for MIN_WORDS_TD in np.linspace(20, 30, 11):
        for MIN_GAME_TD in np.linspace(2, 10, 18):
            print(MIN_WORDS_TD,MIN_GAME_TD)
            p = findSignificantRuminationTestCombination(logs,False)
            if (p<minp):
                minp=p
                bestRumiDiff = MIN_WORDS_TD
                bestGameDiff = MIN_GAME_TD
    print (bestRumiDiff,bestGameDiff,minp)

def findWorkerUUID():
    workerID =  'A1L3O9OZKV3FF4'
    uuids = set(f.name[:5] for f in path(BASE_DIR).files('*demographic.pkl'))
    for uuid in uuids:
        log = readLog(uuid,['demographic'])
        if (log['demographic']['workerID'][0]==workerID):
            print(uuid)
            print([f.name for f in path(BASE_DIR).files('{}*.pkl'.format(uuid))])
            print('haha!')

def calcRumiQuestionsHists(logs):
    ruminationScores,categoryIDs = calcRuminationScoresAndCategories(logs,[1,2])
    ents=[]
    qRange = range(ruminationScores.shape[1])
    for q in qRange:
        ans  = np.array(ruminationScores[:,q])*10
        ent = utils.entropy(ans.astype(int))
        ents.append(ent)
#         plots.histCalcAndPlot(ruminationScores[:,q], binsNum=50, title="question {}".format(q))
#         plots.plotPie(ruminationScores[:,q],title='question {}'.format(q),fileName=os.path.join('figures','question{}_pie'.format(q)))
    plots.graph(qRange, ents, 'Questions Entropy', '#Questions', 'Entropy')

if __name__ == '__main__':
#     findWorkerUUID()
#     calcRumiClicksHist()
#     fat = readFat()
    logs = readLogs(['categoryID','demographic','displayWords','game','rumination'])
#     fitRuminationScores(logs)
    barPlotCategoriesSocres(logs)
#     allCategoriesDiffrentation(logs)
#     calcRumiQuestionsHists(logs)
#     someLie(logs)
#     calcGameClicksHist(logs)
#     calcRumiScoresHist(logs)

#     calcWeightsForRuminationTest(logs)
#     calcSVMWeightsForRuminationTest(logs)
#     calcWeightsCombsForRuminationTest(logs)
#     calcRuminationEffect(logs)

#     findSignificantRuminationTestCombination(logs)
    print('finish')
#         