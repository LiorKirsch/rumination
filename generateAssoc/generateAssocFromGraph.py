#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import cPickle as pickle
import random

'''
    Edge attribute 'GroupSize'
        Number of participants producing the response. 
    Edge attribute 'Normed'
        Whether the relationship was normed (1) or not (0). 
    Edge attribute 'NormingSize'
        Number of participant serving in the group norming the word. 
    Vertex attribute 'Concreteness'
        Concreteness of the word, on a scale between one and seven. 
    Vertex attribute 'Homograph'
        Whether the word is a homograph (non-empty string) or not (empty string). 
    Vertex attribute 'PartOfSpeech'
        Part of speech: Noun (N), Verb (V), Adjective (AJ), Adverb (AD), Pronoun (P), Preposition (PP), Interjection (I), or Conjunction (C) 
    Vertex attribute 'PrintedFreq'
        Frequency of the word, in printing. 
    Vertex attribute 'name'
'''

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def getThreeClosestCircles(vertex):
    distance_zero = g.neighborhood(vertices=[vertex], order=0, mode='out')[0]
    distance_one = g.neighborhood(vertices=[vertex], order=1, mode='out')[0]
    distance_two = g.neighborhood(vertices=[vertex], order=2, mode='out')[0]
    distance_three = g.neighborhood(vertices=[vertex], order=3, mode='out')[0]
    
    only_first_circle = set(distance_one) - set(distance_zero)
    only_second_circle = set(distance_two) - set(distance_one) - set(distance_zero)
    only_third_circle = set(distance_three) - set(distance_two) - set(distance_zero)
    
    # get only the Nouns
    only_first_circle_nouns = g.vs[only_first_circle](PartOfSpeech='N')['name']
    only_second_circle_nouns = g.vs[only_second_circle](PartOfSpeech='N')['name']
    only_third_circle_nouns = g.vs[only_third_circle](PartOfSpeech='N')['name']
    
    only_first_circle_nouns = random.sample(only_first_circle_nouns ,num_close_circle)
    only_second_circle_nouns = random.sample(only_second_circle_nouns ,num_close_circle)
    only_third_circle_nouns = random.sample(only_third_circle_nouns ,num_third_circle)
    
    print('%s \t\t %s \t\t  %s  \t\t  %s'% (vertex['name'], only_first_circle_nouns, only_second_circle_nouns, only_third_circle_nouns))
        
if __name__ == "__main__":
    n = 1000
    
    num_close_circle = 5
    num_third_circle = 5
    
    g = pickle.load(open('freeassoc.pickle'))
    g = g['freeassoc']
    
    
    onlyNouns = g.vs(PartOfSpeech='N')
#     subsetOfVertcies = random.sample(onlyNouns ,n)

    words = {}
    for vertex in onlyNouns:
        ''' 
         For each word get its associations and the number of times
         people choose that association
        '''
        
        current_word = vertex['name']
        distance_zero = g.neighborhood(vertices=[vertex], order=0, mode='out')[0]
        distance_one = g.neighborhood(vertices=[vertex], order=1, mode='out')[0]
        only_first_circle = set(distance_one) - set(distance_zero)
        only_first_circle_nouns = g.vs[only_first_circle](PartOfSpeech='N')
        
        associations = {}
        for neighbor in only_first_circle_nouns:
            edge_between = g.es.select(_source=vertex.index ).select(_target=neighbor.index)[0]
            neighbor_association = neighbor['name']
            groupSize = edge_between['GroupSize']
            associations[neighbor_association] = groupSize
            
#         associations = sorted(associations.items(), key=lambda x: x[1], reverse=True)    
        print('%s \t\t %s' % (current_word,associations))
        
        words[ current_word ] = associations
        
        
    with open('word_assoc.pickle', 'wb') as handle:
        pickle.dump(words, handle)

    with open('word_assoc.pickle', 'wb') as handle:
         words = pickle.load(handle)

        
        
        
        
        
    
    
    
    