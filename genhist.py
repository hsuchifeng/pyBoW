import os
import sys
import getopt
import cPickle
import numpy as np
import time
import cv2
from sklearn import cluster
from scipy.cluster.vq import vq

def usage():
    print 'caculate visual words histgram' 
    print 'usage: python bow.py [-c centoid file] [-s sift_dir] [-o output_dir]'

if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"hc:s:o:")
    centriod_file=''
    sift_dir = ''
    output_dir=''
    k = 0;
    for op,value in opts:
        if op == '-c':
            centriod_file= value
        elif op == '-s':
            sift_dir = value
        elif op == '-o':
            output_dir= value
        elif op == '-h':
            usage()
            sys.exit()
    if output_dir== '' or centriod_file== '' or sift_dir == '':
        usage()
        sys.exit()
    #load centriod
    centriod = cPickle.load(open(centriod_file))
    if centriod is None:
        print 'cannot load centriod'
        sys.exit()
    k,_ = centriod.shape
    
    #calculate histgram
    i = 0
    for d,dn,filenames in os.walk(sift_dir):
        for f in filenames:
            feat = cPickle.load(open(os.path.join(d,f),'rb'))
            label,_ = vq(feat, centriod)
            hist = np.zeros(k)
            for t in label:
                hist[t] += 1
            hist /=  label.shape[0]
            # .sift
            target = os.path.join(output_dir, f[:-5] + '.hist')
            cPickle.dump(hist,open(target,'wb'),-1)
            i +=1
            if i%100 == 0:
                print i, ' images histgram were gennerated'




            
