import socket
from thread import *
import pickle
import numpy
import math

Buffer_Size = 1024


class cal(object):
    pass


# Function for Addition of two values

def add(link, a, b):
    sum = int(a) + int(b)
    link.send(str(sum) + ' ')
    return


# Function for Calculating the value of Pi

def calculate_pi(link):
    s = math.pi
    link.send(str(s))
    return


# Function for Sorting an Array

def sort(link, A):
    A = A.split(" ", 1)
    B = pickle.loads(A[1])
    B.x = [int(i) for i in B.x]
    B.x.sort()
    x = pickle.dumps(B)
    link.send(x)
    return


# Function for Multiplying three Matrices

def matrix_multiply(link, A):
    A = A.split(" ", 1)
    B = pickle.loads(A[1])
    x = numpy.array(B.x)
    y = numpy.array(B.y)
    z = numpy.array(B.z)
    B.x = numpy.dot(numpy.dot(x, y), z)
    serial = pickle.dumps(B)
    link.send(serial)
    return


def thread(link, addrs):
    while True:
        input = link.recv(Buffer_Size)
        Client_msg = input.split(' ')

        if Client_msg[0] == "add":
            add(link, Client_msg[1], Client_msg[2])

        elif Client_msg[0] == "pi":
            calculate_pi(link)

        elif Client_msg[0] == "sort":
            sort(link, input)

        elif Client_msg[0] == "mat":
            matrix_multiply(link, input)

        elif Client_msg[0] == "exit":
            break


    link.close()
    print "Connection closed: ", addrs


def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s" % (PORT, HOST)
    s.bind((HOST, PORT))
    s.listen(3)

    try:

        while True:
            print "waiting for link..."
            link, addrs = s.accept()
            print "Got link from ", addrs
            print "Sending acknowledgment.."
            link.send("1")
            start_new_thread(thread, (link, addrs,))
    except KeyboardInterrupt:
        pass
    print "\n server closed.."
    s.close()


if __name__ == '__main__':
    main()