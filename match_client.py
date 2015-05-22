import socket
import sys
import cPickle 


if __name__ == '__main__':
    HOST, PORT = "10.21.25.102", 1027

    if len(sys.argv) != 2:
        print 'usage:', sys.argv[0], ' <image_to_match>'
        sys.exit(1)

    data = open(sys.argv[1],'rb').read()

    # Create a socket (SOCK_STREAM means a TCP socket)
    print 'conecting to server'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((HOST, PORT))

    print 'sending data'
    sock.sendall(data)
    
    result = cPickle.loads(sock.recv(10*1024*1024))
    print result

