'''
Created on Mar 12, 2014

@author: noampeled
'''
import csv

def get_words(categoryID='1'):
    
    try:
        file_name = '%s.csv' % categoryID

        list_of_lists = []
        with open(file_name, 'rU') as csvfile:
            categoryReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in categoryReader:
                list_of_lists.append( row )
            
    except IOError as e:
        print "I/O error({0}): {1} ({2})".format(e.errno, e.strerror,file_name)            
    except Exception as e:
        list_of_lists = [[e.message]]
        print('{}'.format(e.message))

    return list_of_lists

if __name__ == '__main__':
    print(get_words())