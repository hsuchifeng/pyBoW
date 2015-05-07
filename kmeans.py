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
    
    feats = np.empty([0,128])
    start = time.time()
    for d,dn,filenames in os.walk(input_dir):
        for f in filenames:
            print 'reading file', f
            feats_list = cPickle.load(open(os.path.join(d,f),'rb'))
            for temp in feats_list:
                feats = np.concatenate([feats,temp])
    print 'time elapsed for load file:', time.time()-start

    #k-means
    print 'reading SIFT features'
    start = time.time()
    i = 0
    for s,feat in feats_list:
        feats = np.concatenate([feats,feat])
        i +=1
        if i%100 == 0:
            print i ,' images features read'
    del feats_list
    print 'clustering'
    k_means = cluster.MiniBatchKMeans(n_clusters=k,compute_labels=False)
    k_means.fit(feats)
    center = k_means.cluster_centers_ 
    print 'time elapsed for k-means:',time.time()-start
    
    #save center
    cPickle.dump(center,open(output_file,'wb'),-1)
    print 'finished'
