import os
import sys
import getopt
import cPickle
import cv2

def usage():
    print 'caculate SIFT feature'
    print 'usage: calcsift.py [-i input_file] [-o output_file]'
    print 'every line in @param input_file is a path to image'
    print 'the result was saved to @param output_file'

if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"hi:o:")
    input_file=''
    output_file=''
    for op,value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-h':
            usage()
            sys.exit()
    if input_file == '' or output_file == '':
        usage()
        sys.exit()
    
    #read image and calc SIFT
    fail = 0
    fail_list = []
    succ = 0
    result = []
    sift = cv2.SIFT()
    with open(input_file,'r') as ls:
        for l in ls:
            l = l.strip()
            img = cv2.imread(l)
            if img == None:
                fail += 1
                fail_list.append(l)
                continue
            kp,des = sift.detectAndCompute(img,None)
            succ += 1
            result.append((l,des))

    print 'total:', succ+fail
    print 'success:',succ, ' fail:', fail
    for l in fail_list:
        print l
    
    cPickle.dump(result,open(output_file,'wb'),-1)
