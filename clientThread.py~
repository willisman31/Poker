#!usr/bin/python
from socket import *
#Importing all from thread
from thread import *
import time
#host = 'localhost' # '127.0.0.1' can also be used
#port = 52001

class ClientThread(object):

    def __init__(self,host,port):

        sock = socket()
        #Connecting to socket
        sock.connect(("127.0.0.1", 52001)) #Connect takes tuple of host and port

        start_new_thread(self.client_thread,(sock,))

    def client_thread(self,sock):
        #Infinite loop to keep client running.
        while True:
            #data = sock.recv(1024)
            #print data
            text = raw_input("Enter Text : ")
            sock.send(text)

        sock.close()

def main():
    host = 'localhost' # '127.0.0.1' can also be used
    port = 52001

    obj = ClientThread(host,port)
    time.sleep(60)

if __name__ == '__main__':
    main()
