'''
Created on Mar 19, 2014

@author: noampeled
'''

BASE_DIR = '/Users/noampeled/Dropbox/postDocMoshe/rumination/MasonWordsSite/composeWords/files/Moshe Words'

from path3 import path

def readFiles():
    for fileName in path(BASE_DIR).files('*'):
        with open(fileName,'r') as f:
            print(f)

if __name__ == '__main__':
    readFiles()