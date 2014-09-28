'''
Created on Jun 18, 2014

@author: noampeled
'''

import zipfile

def readZipWords():
    archive = zipfile.ZipFile('words.zip', 'r')    
    wordsFile = archive.open('words')
    for word in wordsFile:
        print(word)
    print(len(wordsFile))

    

if __name__ == '__main__':
    readZipWords()