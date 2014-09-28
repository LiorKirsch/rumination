'''
Created on Jan 27, 2014

@author: noam
'''

import csv
import os 
import numpy as np
import utils
from xlrd import open_workbook


BASE_DIR = os.path.join(os.path.dirname(__file__), 'files','matrices')

def loadMatrices():
    files = utils.filesInFolder(BASE_DIR, '*.xls')
    for file in files:
        book = open_workbook(file,on_demand=True)
        sheet = book.sheet_by_index(0)
        for rownum in xrange(sheet.nrows):
            line = sheet.row_values(rownum)
            if (line[0]=='__________'):
                print('new matrix')


if __name__ == '__main__':
    loadMatrices()