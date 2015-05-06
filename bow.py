import os
import sys
import getopt
import cPickle
import cv2

def usage():
    print 'caculate visual words histgram using k-means'
    print 'usage: calcsift.py [-i input_file] [-o output_file] [-k k]'
    print 'every line in @param input_file is a path to image'
    print 'the result was saved to @param output_file'

if __name__ == "__main__":
    opts,args=getopt.getopt(sys.argv[1:],"hi:o:k:")
    input_file=''
    output_file=''
    k = 0;
    for op,value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-k':
            k = value
        elif op == '-h':
            usage()
            sys.exit()
    if input_file == '' or output_file == '' or k == 0:
        usage()
        sys.exit()
    
    feats_list = cPickle.load(open(input_file,'rb'))
    for s,feats in feats_list:
        print s,feats
