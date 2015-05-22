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
import SocketServer
import socket
import tempfile
import Image

def usage():
    print 'match image server' 
    print 'usage: python match_server.py [-c centoid file] [-h hist_dir] [-p listen-port[default=1027]] [-n result-to-show[default=5]]'

if __name__ == "__main__":
    #check parameter
    opts,args=getopt.getopt(sys.argv[1:],"h:c:p:n:")
    centriod_file=''
    hist_dir = ''
    nport = 1027
    nresult = 5
    for op,value in opts:
        if op == '-c':
            centriod_file= value
        elif op == '-h':
            hist_dir= value
        elif op == '-p':
            nport = int(value) 
        elif op == '-n':
            nresult = int(value)
    if centriod_file== '' or hist_dir == '' :
        usage()
        sys.exit()

    #load centriod
    print 'loading centriod'
    centriod = cPickle.load(open(centriod_file))
    if centriod is None:
        print 'cannot load centriod'
        sys.exit()
    k,_ = centriod.shape

    #load histgram
    print 'loading histgram'
    hist_img = []
    for d,dn,filenames in os.walk(hist_dir):
        for f in filenames:
            hist= cPickle.load(open(os.path.join(d,f),'rb'))
            hist_img.append((hist,f))
    print 'total image:' , len(hist_img)
          
    #create udp server
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(('10.21.25.102',nport))
    #deal request
    while True:
        img_path  = tempfile.mktemp()
        temp = open(img_path,'wb')
       
        #receive file
        data,addr = server.recvfrom(8*1024*1024)
        temp.write(data)
        temp.close()

        #gen image-to-match hist
        print 'matching'
        sift = cv2.SIFT()
        map_cls = {}
        img = cv2.imread(img_path)
        if img is None:
            print 'cannot read image:', image_file
        kp,feat= sift.detectAndCompute(img,None)
        label,_ = vq(feat, centriod)

        #initial image histgram
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

        #gen image path
        h = 128
        res = Image.new('RGB',(2500,h))
        im = Image.open(img_path)
        p = float(h)/im.size[1]
        im = im.resize((int(im.size[0]*p),h),Image.ANTIALIAS)
        res.paste(im,(0,0))
        x = im.size[0] +5

        result = []
        resultf = tempfile.mktemp()
        #print dist_img[:5]
        for i in range(nresult):
            l = len('256_ObjectCategories')
            t = dist_img[i][1][1:-5]
            t = t.replace('-','/',1)
            t = t.replace(']','/')
            result.append(t)
            im =  Image.open(t)
            p = float(h)/im.size[1]
            im = im.resize((int(im.size[0]*p),h),Image.ANTIALIAS)
            res.paste(im,(x,0))
            x += im.size[0] + 2
        res = res.crop((0,0,x,h))
        res.save(resultf,'JPEG')
        print result
        
        f = open(resultf,'rb')
        res = f.read()
        server.sendto(res,addr)
        f.close()

        print 'finish'
