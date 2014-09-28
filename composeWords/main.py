'''
Created on Jan 19, 2014

@author: noampeled
'''

import csv
import os 
from collections import Counter
import numpy as np
import utils

BASE_DIR = os.path.join(os.path.dirname(__file__), 'files')
MASON_WORDS_FILE_NAME =  os.path.join(BASE_DIR, 'AllWords-Horizontal.csv')
ANEW_WORDS_FILE_NAME = os.path.join(BASE_DIR, 'Anew.csv')
WARRINER_WORDS_FILE_NAME = os.path.join(BASE_DIR, 'Ratings_Warriner_et_al.csv')
NEUTRAL_MASON_WORDS_NARROW_FILE_NAME = os.path.join(BASE_DIR, 'neutralMasonWordsNarrow.csv')

NEGATIVE_MAX_VAL = 3
POSITIVE_MIN_VAL = 7

MIN_NEUTRAL_SCORE = 10
MIN_UNDEFINED_CATEGORIES = 2

WORDS_LISTS_NUM = 8
WORDS_IN_LIST = 12

CATEGORY_NEGATIVE = 'negative'
CATEGORY_POSITIVE = 'positive'
CATEGORY_NEUTRAL = 'neutral'
CATEGORY_UNDEFINED = 'undefined'

CATEGORIES = set([CATEGORY_NEGATIVE, CATEGORY_POSITIVE, CATEGORY_NEUTRAL])
MIN_SCORES = {CATEGORY_NEGATIVE:0, CATEGORY_POSITIVE:0, CATEGORY_NEUTRAL:10}

def loadMasonWords():
    masonTable = []
    for line in utils.csvGenerator(MASON_WORDS_FILE_NAME, ','):
        currentLine = []
        for word in line:
            if (word!=''):
                currentLine.append(word.strip().lower())
        if (len(currentLine)>0 and currentLine[0]!=''):
            masonTable.append(currentLine)    
        else:
            break
    return masonTable

def loadWordsTable(csvFileName, delimiter=','):
    anewDict = {}
    for line in utils.csvGenerator(csvFileName, delimiter, 1):
        word = line[0].strip().lower()
        val = float(line[1])
        anewDict[word]=val

    return anewDict

def loadAnewTable():
    return loadWordsTable(ANEW_WORDS_FILE_NAME,',')

def loadWarrinerTable():
    return loadWordsTable(WARRINER_WORDS_FILE_NAME,'\t')

def getAllLineInTheSameCategory(masonTable, anewDict, category):
    newTable, scoring, valancesList  = [], [], []
    for line in masonTable:
        if (len(line)<WORDS_IN_LIST): continue
        valances = [anewDict.get(word,np.nan) for word in line]
        categories = [valanceValToName(val) for val in valances]   
        
        if (categories[0]!=category): continue # Continue if the first word isn't form the current category
        newWordsIndices = []
        for index, word in enumerate(line[:WORDS_IN_LIST], 1):
            if (categories[index]!=category):
                newWord, newWordIndex = findAlternativeWord(line,categories,category,newWordsIndices)
                if (newWord):
                    line[index] = newWord
                    newWordsIndices.append(newWordIndex)
                else:
                    break

        line = line[:WORDS_IN_LIST]
        valances = [getValance(anewDict,word) for word in line]
        categories = [valanceValToName(val) for val in valances]   
        
        count = Counter(categories)
        falseCategories = sum([count[cat] for cat in CATEGORIES-set([category])])
        undefinedCategories =  count[CATEGORY_UNDEFINED]
        score = count[category]
        if (falseCategories==0 and undefinedCategories<=MIN_UNDEFINED_CATEGORIES and score>=MIN_SCORES[category]):
            newTable.append(line)
            scoring.append(score)
            valancesList.append(valances)
            
    return np.array(newTable), np.array(scoring), np.array(valancesList)

def findAlternativeWord(line,categories,category,newWordsIndices):
    for index, word in enumerate(line[WORDS_IN_LIST:]):
        realIndex = index + WORDS_IN_LIST
        if (categories[realIndex]==category and realIndex not in newWordsIndices):
            return word, realIndex
    return None, 0   

def windowsGenerator(line,windowLength=12):
    windowsNum=len(line)-windowLength+1
    if (windowsNum>0):
        valances = [getValance(anewDict,word) for word in line]
        categories = [valanceValToName(val) for val in valances]   
        for startIndex in xrange(windowsNum):
            yield (line[startIndex:startIndex+windowLength],valances[startIndex:startIndex+windowLength],
                   categories[startIndex:startIndex+windowLength])
    else:
        yield (None, None, None)

def getValance(anewDict, word):
    if (word in anewDict):
        return anewDict[word]
    else:
        print('{}'.format(word))
        return np.nan

def getBroadAssociativeChains(masonTable, anewDict, category):
    usedLines = set([0])
    L = masonTable.shape[0]
    

def valanceValToName(val):
    if (np.isnan(val)):
        return CATEGORY_UNDEFINED
    else:
        val = float(val)
        if (val<=NEGATIVE_MAX_VAL):
            return CATEGORY_NEGATIVE
        elif (val>=POSITIVE_MIN_VAL):
            return CATEGORY_POSITIVE
        else:
            return CATEGORY_NEUTRAL
    
def saveNewTable(words, fileName):
    fileName = os.path.join(BASE_DIR,fileName)
    with open(fileName, 'w') as csvWords:
        file_writer = csv.writer(csvWords)
        for line in words:
            file_writer.writerow(line)
    
def getBestWordsIndices(valancesList):
    if (len(valancesList)>0):
        valScoresMean = utils.mean(valancesList,1)
        valScoresStd = utils.std(valancesList,1)
        return np.argsort(abs((valScoresMean+valScoresStd)-5))
    else:
        return []

if __name__ == '__main__':
    masonTable = loadMasonWords()
    anewDict = loadWarrinerTable() #loadAnewTable()
    print('length of dictionary: {}'.format(len(anewDict)))
    for category in [CATEGORY_NEUTRAL]:# CATEGORIES:
        print(category)
        table, scoring, valancesList = getAllLineInTheSameCategory(masonTable, anewDict, category)
        if (table!=[]):
#             bestTable = table[np.argsort(scoring)][-8:]    
            indices = getBestWordsIndices(valancesList)#[:WORDS_LISTS_NUM]
            bestTable = table[indices]
            print(scoring[indices])
#             print(np.sort(scoring)[-8:])
            print(bestTable)
            saveNewTable(bestTable,'{}_narrow.csv'.format(category))
        else:
            print('{}: empty table!'.format(category))
    print('finish!')
    
    
    