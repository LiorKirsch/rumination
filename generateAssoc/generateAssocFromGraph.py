#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import cPickle as pickle
import random
import numpy as np
from collections import OrderedDict

FREE_ASSOC_GRAPH_FILE_NAME = '/Users/noampeled/Dropbox/postDocMoshe/rumination/rumination/trunk/generateAssoc/freeassoc.pickle'

from composeWords.createWordsByValances import (loadWarrinerTable,
    valanceValToCategory, CATEGORY_NEUTRAL)

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


def is_word_neutral_cl(anewDict):
    def is_it(word):
        val = anewDict.get(word.lower(), None)
#         print(word, val)
        return (val is not None and valanceValToCategory(val) == CATEGORY_NEUTRAL)
    return is_it


def read_word_assoc_dists():
    anewDict = loadWarrinerTable()
    is_word_neutral = is_word_neutral_cl(anewDict)
    with open('word_assoc_vals.pkl', 'r') as handle:
        all_dists, all_neutral, all_words, all_assoc = pickle.load(handle)
    words_num = 0
    words, strongAssoc, weakAssoc = [], [], []
    for dists, is_neutral, word, assocs in zip(all_dists,
            all_neutral, all_words, all_assoc):
        dists = np.array(dists)
        is_neutral = np.array(is_neutral)
        assocs = np.array(assocs)
        idx1 = (dists > 0.07) & (dists < 0.2)
        if (sum(idx1) < 4):
            continue
        idx2 = (dists < 0.04) & (dists >= 0.015)
        if (sum(idx2) < 4):
            continue
        neutral_idx1 = np.array([is_word_neutral(ass[0].lower()) for ass in assocs[idx1]])
        neutral_idx2 = np.array([is_word_neutral(ass[0].lower()) for ass in assocs[idx2]])
        if (sum(neutral_idx1) < 4 or sum(neutral_idx2) < 4):
            continue
        assoc1 = assocs[idx1][neutral_idx1][:4]
        assoc2 = assocs[idx2][neutral_idx2][:4]
        words_num += 1
        words.append(word.lower())
        print(word.lower())
        strongAssoc.append([ass[0].lower() for ass in assoc1])
        weakAssoc.append([ass[0].lower() for ass in assoc2])
    print ('words num {}'.format(words_num))
    retAss = {}
    for word, strongAss, weakAss in zip(words, strongAssoc, weakAssoc):
        print(word)
        print('strong:', strongAss)
        print('weak:', weakAss)
        retAss[word] = {'strong': strongAss, 'weak': weakAss}
    with open('words_strong_weak_assoc.pkl', 'w') as handle:
        pickle.dump(retAss, handle)


def shuffleAssocs():
    ret = []
    with open('words_strong_weak_assoc.pkl', 'r') as assFile:
        retAss = pickle.load(assFile)
        # shuffle
        words = retAss.keys()
        print(words)
        random.shuffle(words)
        print(words)
        for word in words:
            random.shuffle(retAss[word]['strong'])
            random.shuffle(retAss[word]['weak'])
            ret.append((word, retAss[word]['strong'], retAss[word]['weak']))
        print(ret)

def save_neutral_words():
    g = pickle.load(open(FREE_ASSOC_GRAPH_FILE_NAME))
    g = g['freeassoc']

    onlyNouns = g.vs(PartOfSpeech='N')
#     subsetOfVertcies = random.sample(onlyNouns ,n)

    words = {}
    all_dists, all_words, all_assoc, all_neutral = [], [], [], []
    anewDict = loadWarrinerTable()
    is_word_neutral = is_word_neutral_cl(anewDict)

    for vertex in onlyNouns:
        '''
         For each word get its associations and the number of times
         people choose that association
        '''
        current_word = vertex['name']
        if (not is_word_neutral(current_word)):
            continue
        distance_zero = g.neighborhood(vertices=[vertex], order=0, mode='out')[0]
        distance_one = g.neighborhood(vertices=[vertex], order=1, mode='out')[0]
        only_first_circle = set(distance_one) - set(distance_zero)
        only_first_circle_nouns = g.vs[only_first_circle](PartOfSpeech='N')

        associations = {}
        if (len(only_first_circle_nouns) < 8):
            continue
        for neighbor in only_first_circle_nouns:
            edge_between = g.es.select(_source=vertex.index).select(_target=neighbor.index)[0]
            neighbor_association = neighbor['name']
            groupSize = edge_between['GroupSize'] 
            NormingSize = edge_between['NormingSize']
            # NormingSize
            # Number of participant serving in the group norming the word.
            associations[neighbor_association] = groupSize / float(NormingSize)

        print(current_word)
        associations = sorted(associations.items(), key=lambda t: t[1], reverse=True)
#         neutral_first_ass = np.all([is_word_neutral(ass[0].lower()) for ass in associations[:4]])
#         rest_ass = sum([is_word_neutral(ass[0].lower()) and ass[1]>=0.01 for ass in associations[4:]])>=4 
#         if (neutral_first_ass and rest_ass):
        all_dists.append([ass[1] for ass in associations])
        all_neutral.append([is_word_neutral(ass[0].lower()) for ass in associations])
        all_words.append(current_word)
        all_assoc.append(associations)
#         strong_first_ass = np.all([ass[1] >= 0.1 for ass in associations[:4]])
#         weak_last_ass = np.all([(ass[1] <= 0.05 and ass[1] >= 0.02) for ass in associations[-4:]])
#         neutral_first_ass = np.all([is_word_neutral(ass[0].lower()) for ass in associations[:4]])
#         neutral_last_ass = np.all([is_word_neutral(ass[0].lower()) for ass in associations[-4:]])
# 
#         if (strong_first_ass and weak_last_ass and neutral_first_ass and neutral_last_ass):
#             print('Yes!')
#             words[current_word] = associations
#             print(len(words))
#         else:
#             print('{}: nop'.format(current_word))
# 
#         print('%s \t\t %s' % (current_word, associations))
#         print([anewDict.get(association[0].lower()) for association in associations])

    all_dists = np.array(all_dists)
    with open('word_assoc_vals.pkl', 'w') as handle:
        pickle.dump((all_dists, all_neutral, all_words, all_assoc), handle)

if __name__ == "__main__":
#     save_neutral_words()
    read_word_assoc_dists()
#     shuffleAssocs()
