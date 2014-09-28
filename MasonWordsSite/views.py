from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
# from django.utils import simplejson 
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
import json

from random import randrange
from django.conf import settings
from django.views.decorators.cache import never_cache
import random, string
import os
import csv
import numpy as np

import pickle
import zipfile
import StringIO
import inspect
from path3 import path

FOLDERS = ('/Users/noampeled/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/', 
           '/home/noam/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/',
           '/home/liorkirsch/webapps/masonwords/MasonWordsSite/logs',
           '/home/liorlocal/workspace/MasonWordsSite/logs',
           )

BASE_DIR = [f for f in FOLDERS if os.path.exists(f)][0]
HISTORY_LOGS_DIRS =  [os.path.join(BASE_DIR,historyFolder) for historyFolder in ['amt1','amt2','amt3']]

PAGE_DEFAULT, PAGE_CONTROL, PAGE_CONTROL_NO_GAME = range(3)
POST_DEMOGRAPHIC = {PAGE_DEFAULT: '/displaywords/',  PAGE_CONTROL: '/game/', PAGE_CONTROL_NO_GAME: '/questionnaire/'}
POST_DEMOGRAPHIC_PANAS = {PAGE_DEFAULT: '/displaywords/',  PAGE_CONTROL: '/game/', PAGE_CONTROL_NO_GAME: '/questionnaire2/'}

WORDS_GAME_RUMI = {'postCognitiveTask': '/demographic/', 
             'postDemographic': POST_DEMOGRAPHIC, 
             'postDisplayWords': '/game/',
             'postGame': '/questionnaire/',
             'postRuminationTest': '/feedback/',
             'postFeedback' : '/goodbye/'}

WORDS_GAME_PANAS = {'postCognitiveTask': '/demographic/', 
             'postDemographic': POST_DEMOGRAPHIC_PANAS, 
             'postDisplayWords': '/game/',
             'postGame': '/questionnaire2/',
             'postRuminationTest': '/feedback/',
             'postFeedback' : '/goodbye/'}

POST_URLS = WORDS_GAME_PANAS

ERROR_PAGES = {'postCognitiveTask': '/failed_math/'}

@csrf_exempt
@never_cache
def postCognitiveTask(request):
    uuid = generateRandomString(5)
    workerID = request.POST['workerID']
    if (request.POST['solved']!='true'):   
        saveLog({'workerID':workerID}, uuid, 'workerID')
        return errorPage();
    else:
        if (checkIfPlayerHasAlreadyPlayed(request, workerID)):
            return goToDuplicateWorker()
        else:
            saveLog({'workerID':workerID, 'experiment':request.POST.get('experiment','1')}, uuid, 'workerID')
            initGlobalFields(request,workerID,uuid);        
            return nextPage();

def initGlobalFields(request,workerID,uuid):
    request.session['data']={}
    request.session['data']['experiment']=request.POST.get('experiment','1')
    request.session['data']['fromAmazon']=request.POST['fromAmazon']
    request.session['data']['condition']=request.POST['condition']
    request.session['data']['categoryID']=request.POST['categoryID']
    request.session['data']['uuid'] = uuid
    request.session['data']['workerID'] = workerID
    request.session.modified = True
    print('categoryID: {}'.format(request.session['data']['categoryID']))

@csrf_exempt
@never_cache
def postDemographic(request):
    # Save demographic data
    saveRequest(request,'demographic')
    # Save IP
    saveLog({'ip':get_client_ip(request)}, request.session['data']['uuid'], 'ip')
    uuid = request.session['data']['uuid']
    if (request.session['data']['condition']=='0'):
        request.session['data']['wordsCategory']=str(randrange(4))
    else: 
        request.session['data']['wordsCategory']=request.session['data']['categoryID']
    request.session.modified = True
 
    print('categoryID: {}'.format(request.session['data']['wordsCategory']))
    saveLog({'categoryID':request.session['data']['wordsCategory']}, uuid, 'categoryID')
    if (request.session['data']['wordsCategory']=='0'): # Don't display any words 
        return nextPage(PAGE_CONTROL)
    elif (request.session['data']['wordsCategory']=='-1'): # Don't display any words nor game
        return nextPage(PAGE_CONTROL_NO_GAME)
    else: # display words according to the random category
        return nextPage(PAGE_DEFAULT)

@csrf_exempt 
@never_cache
def postDisplayWords(request):
    # Save click times 
    saveRequest(request,'displayWords')
    return nextPage()

@csrf_exempt
@never_cache
def save_fat(request):
    saveRequest(request,'fat')
    return HttpResponseRedirect('/goodbye/')
     
@csrf_exempt
@never_cache
def postGame(request):
    saveRequest(request,'game')
    return nextPage()

@csrf_exempt
@never_cache
def postRuminationTest(request):
    saveRequest(request,'rumination')
    return nextPage()

@csrf_exempt
@never_cache
def postFeedback(request):
    saveRequest(request,'feedback')
    return nextPage()

     
def checkIfPlayerHasAlreadyPlayed(request, workerID):
    uuidsTup = set((f.name[:5],BASE_DIR) for f in path(BASE_DIR).files('*workerID.pkl')) 
    for historyFolder in HISTORY_LOGS_DIRS:
        history_uuids = set((f.name[:5],historyFolder) for f in path(historyFolder).files('*demographic.pkl'))
        uuidsTup = uuidsTup.union(history_uuids) 
    for uuidTup in uuidsTup:
        if (workerID==getWorkerIDFromLog(uuidTup[0],uuidTup[1])):
            return True
    return False
            
def getWorkerIDFromLog(uuid,folder):
    fileName = os.path.join(folder, '{}_{}.pkl'.format(uuid,'demographic'))
    try:
        with open(fileName, 'r') as pklFile:
            log = pickle.load(pklFile)
            workerID = log['workerID']
        return workerID
    except:
        return ''
    
def goToDuplicateWorker():
    return HttpResponseRedirect('/duplicate_worker/')
        
def saveRequest(request,field):
    data = request.session.get('data',None)
    if (not data):
        request.session['data']={}
    request.session['data'][field]=request.POST
    saveLog(request.POST, request.session['data']['uuid'], field)

def saveLog(obj,uuid,stepName):
    fileName = os.path.join(settings.BASE_DIR, 'logs','%s_%s.pkl' % (uuid,stepName))
    with open(fileName, 'w') as pklFile:
        pickle.dump(obj, pklFile)   

def get_uuid(request):
    data = request.session['data']
    return sendObjectAsJson({'workerID':data.get('workerID',''), 
                             'uuid':data.get('uuid',''), 
                             'fromAmazon':data.get('fromAmazon',1)})

def getEnglishDict(request):
    with open(os.path.join(settings.STATIC_ROOT,'words','words.zip'),'r') as wordsDict:
        response = HttpResponse(wordsDict.read())
        response['Content-Disposition'] = 'attachment; filename=words.zip'
        return response
    return None

def getWorkerID(request):
    data = request.session.get('data',None)
    if (data):
        demographic = request.session['data'].get('demographic',None)
        return demographic.get('workerID','') if demographic else ''
    else:
        return ''
    
def getLogs(request, uuid=''):
    try:
        os.chdir(settings.LOGS_ROOT)
        zbuffer = StringIO.StringIO()
        zipf = zipfile.ZipFile(zbuffer, 'w')
        for logFile in os.listdir(settings.LOGS_ROOT):
            if (uuid=='' or uuid!='' and uuid in logFile):
                zipf.write(logFile)
        zipf.close()
    
        # generate the file
        zbuffer.seek(0)
        response = HttpResponse(zbuffer.read())
        response['Content-Disposition'] = 'attachment; filename={}.zip'.format('logs' if uuid=='' else uuid)
        return response
    except:
        return

def getRemarks(request):
    ret = ''
    # Get all the log files with 'feedback' in their name
    files = (f for f in os.listdir(settings.LOGS_ROOT) if 'feedback' in f)
    for logFile in files:
        with open(os.path.join(settings.LOGS_ROOT,logFile)) as pklFile:
            log = pickle.load(pklFile)
            if (log['notes']!=''):
                ret += '{}\n\n'.format(log['notes'])
    return sendObjectAsJson({'remarks':ret})

def getWorkerSummary(request,uuid):
    ret=''
    for field in ['demographic','clicks','rumination','feedback','ip','fat','game']:
        fileName = os.path.join(settings.LOGS_ROOT, '{}_{}.pkl'.format(uuid,field))
        try:
            with open(fileName, 'r') as pklFile:
                log = pickle.load(pklFile)
                ret += '{}:\n'.format(field)
                ret += ', '.join(['{}: {}'.format(key,val) for key,val in sorted(log.iteritems())])
                ret+='\n\n'
        except:
            ret+= 'No file for {}\n\n'.format(field)
    return sendObjectAsJson({'summary':ret})

@never_cache
def get_words(request):  
    wordsInChain = 12
    chainsNum = 16
    data = request.session.get('data',None)
    if (data):
        categoryID = request.session['data']['wordsCategory'] # request.session['data']['categoryID']
        file_name = os.path.join(settings.STATIC_ROOT, 'bag_of_words','%s.csv' % categoryID)
        words = getWordsListsFromFile(file_name,wordsInChain)
        words = words.reshape((chainsNum,words.size/chainsNum))
        words = shuffle(words)
    else:
        words = []
            
    jsonResponse = sendObjectAsJson(words.tolist())
    return jsonResponse

def getSelctionWords(request, categoryID):
    wordsInChain = 12
    file_name = os.path.join(settings.STATIC_ROOT, 'bag_of_words','%s.csv' % categoryID)
    words = getWordsListsFromFile(file_name,wordsInChain)
    jsonResponse = sendObjectAsJson(words.tolist())
    return jsonResponse

def shuffle(X):
    inds = range(X.shape[0])
    random.shuffle(inds)
    return X[inds,:]

def getWordsListsFromFile(file_name,wordsInChain):    
    try:
        list_of_lists = []
        with open(file_name, 'rU') as csvfile:
            categoryReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in categoryReader:
                list_of_lists.append( [s.lower().strip() for k,s in enumerate(row) if s.strip()!='' and k<wordsInChain] )

    except IOError as e:
        list_of_lists = []
        print "I/O error({0}): {1} ({2})".format(e.errno, e.strerror,file_name)            
    except Exception as e:
        list_of_lists = []
        print('{}'.format(e.message))         
    
    return np.array(list_of_lists)

def generateRandomString(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))
    

def sendObjectAsJson(myObjectDict):
    data = json.dumps(myObjectDict, indent=4)
    resp = HttpResponse(data, content_type='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp
    
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip

def nextPage(action=''):
#     inspect.currentframe().f_code.co_name
    callerName = inspect.currentframe().f_back.f_code.co_name
    if (action==''):
        return HttpResponseRedirect(POST_URLS[callerName])
    else:
        return HttpResponseRedirect(POST_URLS[callerName][action])

def errorPage():
    callerName = inspect.currentframe().f_back.f_code.co_name
    return HttpResponseRedirect(ERROR_PAGES[callerName])
