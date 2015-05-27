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


if __name__ == "__main__":
    result = cPickle.load(open(sys.argv[1],'rb'))
    for label,n in result:
        print label,",",n/float(25)
