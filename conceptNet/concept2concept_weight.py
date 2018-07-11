#!/usr/bin/python
# coding: utf-8

import re
import requests
import urllib2
from bs4 import BeautifulSoup

def conceptnet_web(phrase):
        url = 'http://api.conceptnet.io/c/ja/' + phrase
        obj = requests.get(url).json()

        print len(obj['edges'])
        list =  obj['edges']
        poses = []
        purpose = []                                                                                                                                                         
        rela_weight = {}

        for i in range(len(list)):
                poses.append(list[i][u'@id'])

        for i,ptr in enumerate(poses):
                ptr = ptr.split(',')
                
                #if ( lang1 == 'ja' and lang2 == 'ja' ) :
                if ptr[1].split("/")[3].encode('utf-8') != phrase:
                    text = ptr[1].split('/')[3]
                else:
                    text = ptr[2].split('/')[3]
                purpose.append(text)
                rela_weight[text] =  obj['edges'][i][u'weight']

        for word,weight in rela_weight.items():
            print word + ":" + str(weight)
        purpose = set(purpose)
        return (purpose)

'''
def conceptnet_dic(phrase):
        f = open('conceptnet5_ja.lis','r')

        pattern = re.compile(phrase)
        lines = []
        poses = []
        purpose = []

#       for line in f:
#               if relations in line:
#                       lines.append(line)

        for l in f:
                l = re.sub("[()' ]",'',l)
                l = re.sub("\n",'',l)
                l = l.split(',')
                poses.append(l)

        for pose in poses:
                if not pattern.match(pose[0]) == None and not pose[2] in purpose:
                        purpose.append(pose[2])
#                       print pose[2], pose[1]

        return (purpose)
'''

if __name__ == "__main__":

        phrase = raw_input("Query::")

#       list_dic = conceptnet_dic(phrase)
#       for l in list_dic:
#               print l

        list_web = conceptnet_web(phrase)
#       for l in list_web:
#               print l