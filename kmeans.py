import os
import sys
import getopt
import cPickle
import numpy as np
import time
import cv2
from sklearn import cluster

def usage():
    print 'caculate visual words histgram using k-means'
    print 'usage: python bow.py [-i input_dir] [-o output_file] [-k k]'

if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"hi:o:k:")
    input_dir=''
    output_file=''
    k = 0;
    for op,value in opts:
        if op == '-i':
            input_dir= value
        elif op == '-o':
            output_file= value
        elif op == '-k':
            k = int(value)
        elif op == '-h':
            usage()
            sys.exit()
    if input_dir== '' or output_file == '' or k == 0:
        usage()
        sys.exit()
    print 'getting feats count'
    feats_count = 0
    for d,dn,filenames in os.walk(input_dir):
        for f in filenames:
            feat = cPickle.load(open(os.path.join(d,f),'rb'))
            t, _ =feat.shape
            feats_count += t

    feats = np.empty([feats_count,128])
    i = 0
    feats_index = 0
    for d,dn,filenames in os.walk(input_dir):
        for f in filenames:
            i += 1
            start = time.time()
            feat = cPickle.load(open(os.path.join(d,f),'rb'))
            if i%100 == 0:
                print i
                print 'load file:', time.time() - start
            start = time.time()
            t, _ = feat.shape
            # modify element of feats
            row = range(feats_index, feats_index +t)
            feats[row,] = feat
            feats_index += t
            if i%100 == 0:
                print 'merge array:', time.time() - start
    print 'time elapsed for load file:', time.time()-start

    #k-means
    del feat
    print 'clustering'
    k_means = cluster.MiniBatchKMeans(n_clusters=k,compute_labels=False)
    k_means.fit(feats)
    center = k_means.cluster_centers_ 
    print 'time elapsed for k-means:',time.time()-start
    
    #save center
    cPickle.dump(center,open(output_file,'wb'),-1)
    print 'finished'
