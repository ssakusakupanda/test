#coding: utf-8
"""Similarity N-best using Word2Vec.

usage:
    python2 thisScript.py yourmodel.model

"""
from __future__ import print_function
from gensim.models import word2vec
import logging
import readline
import numpy
import commands
import re
import sys
import subprocess

ENC = "utf-8"
dai = re.compile(ur'代表表記:([^/]+)/')

MODEL_PATH = "/FORALL/w2vcorpus_from_yacis/full/yacis_full_juman.model"

class WordNotInVocabulary(Exception):
    """語彙に語が存在しない例外"""
    def __init__(self, word):
        self.word = word
    def __str__(self):
        return repr(self.word)

def get_stem_juman(word):
    """Gets the word's stem using JUMAN"""
    cmd = "echo %s | juman" % word.encode(ENC)
    juman_out = commands.getoutput(cmd)
    joA = juman_out.strip().split("\n")
    jo0 = joA[0].decode(ENC) # 最初行
    mtch = dai.search(jo0)
    if not mtch:
        return u""
    yomi = mtch.group(1)
    return yomi

def s(model, posi, nega=[], n=5, prev=u"", root=u""):
    tries = 0
    dic   = {}
    try:
        print("posi:", posi)
        result = model.most_similar(positive=posi, negative=nega, topn=n)
        print("%s\t%s%s%s" % ('順位', '語', "  "*14, '類似度'))
        wf = open('w2v.txt','a+')
        #wf.write("keyword\t"+posi.encode('utf-8')+"\n")
        for rank, r in enumerate(result):
            r_wd, r_sim = r
            spc = "  " * (15 - len(r_wd))
            print("%2d\t%s%s%f" % (rank + 1, r_wd, spc, r_sim, ))
            #wf.write(str(rank+1) + "\t" + r_wd.encode('utf-8') + "\t" + str(r_sim) + "\n")
            if dic.has_key(r_wd) == False:
               dic[r_wd] = 1
            else:
               dic[r_wd] += 1

            leaf = model.most_similar(positive=r_wd, negative=nega, topn=n)
            for rank_leaf, r_leaf in enumerate(leaf):
                r_wd_leaf, r_sim_leaf = r_leaf
                spc_leaf = "  " * (15 - len(r_wd_leaf))
                #print("%2d\t%s%s%f" % (rank_leaf + 1, r_wd_leaf, spc_leaf, r_sim_leaf, ))
                if dic.has_key(r_wd_leaf) == False:
                     dic[r_wd_leaf] = 1
                else:
                     dic[r_wd_leaf] += 1


        #print("ranking:")
        wf.write('[')
        for key, value in sorted(dic.iteritems(), key=lambda x: -x[1]):
             print("key: %s,\t value:%d" %(key, value))
             wf.write("'%s',\n" %(key.encode('utf-8')))
        wf.write(']\n')

    except KeyError:
        print("%s (length %d) not found in vocabulary, changing its form" %\
                (posi.encode(ENC), len(posi), ))
        if prev == posi:
            raise WordNotInVocabulary(root.encode(ENC))
        g = get_stem_juman(posi)
        s(model, g, nega, n, posi, root)
    except Exception as e:
        print("Error:", e, type(e))

def load_model(fname_model):
    print("Loading:", fname_model)
    model = word2vec.Word2Vec.load(fname_model)
    return model

def prepare_model(fname=""):
    if not fname:
        fname_model = MODEL_PATH
    else:
        fname_model = fname

    print("Preparing:", fname_model)
    model = load_model(fname_model)
    print(repr(model))

    return model

def main():
    wf = open('w2v.txt','w')
    if len(sys.argv) > 1:
        fname_model = sys.argv[1]
    else:
        fname_model = ""
    try:
        model = prepare_model(fname_model)
        print("qで終了")
        while 1:
            ipt0 = raw_input("ameblo2> ").decode(ENC)
            if not ipt0:
                continue
            if ipt0 == 'q':
                break
            s(model, ipt0, n=10, root=ipt0)
    except WordNotInVocabulary as wniv:
        print("'%s' doesn't exist in vocabulary!" % (wniv.word, ))
    except (KeyboardInterrupt, EOFError):
        print("")
        pass

if __name__ == '__main__':
    main()
