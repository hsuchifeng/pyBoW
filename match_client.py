# -*- coding: cp936 -*-
import socket
import sys
import cPickle
import Image
import tempfile

if __name__ == '__main__':
    HOST, PORT = "10.21.25.102", 1027

    if len(sys.argv) != 2:
        print 'usage:', sys.argv[0], ' <image_to_match>'
        sys.exit(1)

    print 'conecting to server'
    sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    f = open(sys.argv[1],'rb')
    data = f.read()
    sock.sendto(data, (HOST,PORT))

    data,server = sock.recvfrom(8*1024*1024)
    print data,server
    sock.close()
