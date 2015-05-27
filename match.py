import os
import sys
import getopt
import cPickle
import numpy as np
import time
import cv2
import scipy
from sklearn import cluster
from scipy.cluster.vq import vq

def usage():
    print 'match image' 
    print 'usage: python bow.py [-c centoid file] [-h hist_dir] [-i images_to_match] [-r result_file] [-n nresult]'

if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"h:n:c:i:r:")
    centriod_file=''
    hist_dir = ''
    image_file = '' 
    res_file = ''
    nresul = 5
    k = 0;
    for op,value in opts:
        if op == '-c':
            centriod_file= value
        elif op == '-h':
            hist_dir= value
        elif op == '-i':
            image_file= value
        elif op == '-r':
            res_file = value
        elif op == '-n':
            nresult = int(value)
    if centriod_file== '' or hist_dir == '' or image_file == '':
        usage()
        sys.exit()
    #load centriod
    print 'load centriod'
    centriod = cPickle.load(open(centriod_file))
    if centriod is None:
        print 'cannot load centriod'
        sys.exit()
    k,_ = centriod.shape

    #load histgram
    print 'load histgram'
    hist_img = []
    for d,dn,filenames in os.walk(hist_dir):
        for f in filenames:
            hist= cPickle.load(open(os.path.join(d,f),'rb'))
            hist_img.append((hist,f))
           
    #gen image-to-match hist
    print 'matching'
    sift = cv2.SIFT()
    map_cls = {}
    with open(image_file) as imgs:
        for im in imgs:
            img = cv2.imread(im.strip())
            if img is None:
                print 'cannot read image:', image_file
                continue
            kp,feat= sift.detectAndCompute(img,None)
            label,_ = vq(feat, centriod)
            image_hist = np.zeros(centriod.shape[0])
            for t in label:
                image_hist[t] +=1
            image_hist /= centriod.shape[0]
            #match
            dist_img = []
            for h,f in hist_img:
                sim= 1- scipy.spatial.distance.cosine(h,image_hist)
                dist_img.append((sim,f))     
            dist_img.sort(key=lambda t: t[0], reverse=True) 
    
            #get label
            cls =  os.path.basename(os.path.dirname(im))

            j = 0.0
            #match top-nresult
            for i in range(nresult):
                if cls in  dist_img[i][1]:
                    j +=1
            #prevent no element
            if cls not in map_cls:
                map_cls[cls] = 0
            map_cls[cls] += j
    resf = open(res_file,'w')
    result = []
    for k in map_cls:
        resf.write(k+","+ str(map_cls[k])+'\n')
        print k,',',map_cls[k]
    resf.close()
