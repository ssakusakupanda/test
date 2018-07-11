#!/usr/bin/python
# coding: utf-8

import re
import requests
import urllib2
from bs4 import BeautifulSoup

def conceptnet_web(phrase):
        url = 'http://api.conceptnet.io/c/ja/' + phrase
        obj = requests.get(url).json()
        list =  obj['edges']
        poses = []
        purpose = []

        for i in range(len(list)):
                poses.append(list[i]['@id'])

        for ptr in poses:
                ptr = ptr.split(',')
                lang1 = ptr[1].split("/")[2]
                lang2 = ptr[2].split("/")[2]
                #print(lang)

                if ( lang1 == 'ja' and lang2 == 'ja' ) :
                        text = ptr[2].split('/')[3]
                        purpose.append(text)

        purpose = set(purpose)
        return (purpose)

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

if __name__ == "__main__":

        phrase = raw_input("Query::")

        list_dic = conceptnet_dic(phrase)
#       for l in list_dic:
#               print l
        list_web = conceptnet_web(phrase)
#       for l in list_web:
#               print l

        list = []
        list.extend(list_dic)
        list.extend(list_web)
        list = set(list)
        for l in list:
                print l