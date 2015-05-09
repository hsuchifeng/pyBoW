import os
import sys
import getopt
import cPickle
import cv2
import numpy as np
import time
from multiprocessing import Pool

def usage():
    print 'caculate SIFT feature'
    print 'usage: calcsift.py [-i input_file] [-o output_dir] [-n n_process]'
    print 'every line in @param input_file is a path to image'
    print 'the result was saved to @param output_file'

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
        for i in range(wanted_parts) ]

def calcsift(l):
    # @param l = [dirname,image_path_lists]
    #read image and calc SIFT
    start = time.time()
    d,files = l
    fail = 0
    fail_list = []
    nosift = 0
    nosift_list = []
    succ = 0
    sift = cv2.SIFT()
    for f in files:
        img = cv2.imread(f)
        if img is None:
            fail += 1
            fail_list.append(f)
            continue
        kp,des = sift.detectAndCompute(img,None)
        if des is not None:
            succ += 1
            temp = '[' + os.path.dirname(f).replace('/','-') + ']'
            temp += os.path.basename(f) + '.sift'
            cPickle.dump(des,open(os.path.join(d,temp),'wb'), -1)
        else:
            nosift +=1
            nosift_list.append(f)
    
        
    for t in range(50):
        sys.stdout.write('=')
    print ''
    print 'pid:', os.getpid(), ' ppid:', os.getppid()    
    print 'total:\t', succ+fail+nosift
    print 'fail:\t', fail
    for t in fail_list:
        print t
    print 'no sift:', nosift
    for t in nosift_list:
        print t
    print 'time elapsed:', time.time() - start
    for t in range(50):
        sys.stdout.write('=')
    print '' 


if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"hi:o:n:")
    input_file=''
    output_file=''
    nprocess = 1
    for op,value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-n':
            nprocess = int(value)
        elif op == '-h':
            usage()
            sys.exit()
    if input_file == '' or output_file == '':
        usage()
        sys.exit()
    files = []
    with open(input_file,'r') as ls:
        for l in ls:
            files.append(l.strip())
    files = split_list(files,nprocess)
    params = []
    for f in files:
        params.append([output_file,f])
    p = Pool(nprocess)
    p.map(calcsift,params)
