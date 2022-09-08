import socket
from thread import *
import pickle
import numpy
import math


Buffer_Size = 1024

Data_Save = {'add': 0, 'pie': 0, 'sort': [], 'mat': []}


class cal(object):
    pass


def add(a, b):
    s = int(a) + int(b)
    Data_Save.update({'add': s})
    print Data_Save['add']
    return


def get_add(link):
    link.send(str(Data_Save['add']) + ' ')


def calculate_pi():
    s = math.pi
    Data_Save.update({'pie': s})
    return


def get_pi(link):
    link.send(str(Data_Save['pie']))
    return


def sort(A):
    A = A.split(" ", 1)
    B = pickle.loads(A[1])
    B.x = [int(i) for i in B.x]
    print B.x
    B.x.sort()
    Data_Save.update({'sort': B.x})
    print "sort is", Data_Save['sort']
    return


def get_sort(link):
    serial = pickle.dumps(Data_Save['sort'])
    print serial
    link.send(serial)
    return


def matrix_multiply(A):
    A = A.split(" ", 1)
    B = pickle.loads(A[1])
    x = numpy.array(B.x)
    y= numpy.array(B.y)
    z = numpy.array(B.z)
    B.x = numpy.dot(numpy.dot(x,y),z)
    Data_Save.update({'mat': B.x})
    print "matrix is", Data_Save['mat']
    return


def get_matrix_mul(link):
    serial = pickle.dumps(Data_Save['mat'])
    print serial
    link.send(serial)
    return


def thread(link, addrs):
    while True:
        input = link.recv(Buffer_Size)
        client_msg = input.split(' ')

        if client_msg[0] == "ADD":
            add(client_msg[1], client_msg[2])

        elif client_msg[0] == "getadd":
            get_add(link)

        elif client_msg[0] == "calculate_pi":
            calculate_pi()

        elif client_msg[0] == "getpie":
            get_pi(link)

        elif client_msg[0] == "sort":
            sort(input)

        elif client_msg[0] == "getsort":
            get_sort(link)

        elif client_msg[0] == "mat":
            matrix_multiply(input)

        elif client_msg[0] == "getmat":
            get_matrix_mul(link)

        elif client_msg[0] == "exit":
            break

    link.close()
    print "Connection closed: ", addrs


def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s" % (PORT, HOST)
    s_socket.bind((HOST, PORT))
    s_socket.listen(3)
    try:

        while True:
            link, addrs = s_socket.accept()
            print "Got connection from ", addrs
            print "Sending acknowledgment.."
            link.send("1")
            start_new_thread(thread, (link, addrs,))

    except KeyboardInterrupt:
        pass
    print "\n server closed.."

    s_socket.close()


if __name__ == '__main__':
    main()