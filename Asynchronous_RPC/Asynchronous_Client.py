import socket
import pickle

HOST = "127.0.0.1"
PORT = 8080
Buffer_Size = 1024


def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to port %s and server %s" % (PORT, HOST)
    s.connect((HOST, PORT))
    ack = s.recv(Buffer_Size)

    if ack == "1":
        print "Connected to server and got acknowledgments: ", ack
        return s


class cal(object):
    pass


def add(x, y, link):
    s = 0
    link.send("ADD " + x + ' ' + y)
    return

def get_add(link):
    link.send("getadd" + '')
    s = link.recv(Buffer_Size)
    s = s.split(' ')
    print " sum =", int(s[0])


def calculate_pi(link):
    link.send("calculate_pi ")
    return


def get_pi(link):
    link.send("getpie" + '')
    print "value of pie is:", link.recv(Buffer_Size)
    return


def sort(link):
    cobj = cal()
    A = list()
    n = raw_input("enter the size of array")
    print"enter the numbers in array"

    for i in range(int(n)):
        x = raw_input("num" + str(i) + ":")
        A.append(x)
    print "The Unsorted Array: ", A
    cobj.x = A
    serial = pickle.dumps(cobj)
    link.send("sort " + serial)
    return


def get_sort(link):
    link.send("getsort " + '')
    A= link.recv(Buffer_Size)
    B = pickle.loads(A)
    print "The sorted Array: ", B
    return


def matrix_multiplication(connection):
    mat1 = list()
    mat2 = list()
    mat3 = list()
    print "* Condition for multiplying three matrices \n1. Column of matrix-1 must be equal to Row of matrix-2 \n2.Column of matrix-2 must be equal to Row of matrix-3"
    print"\n Enter size of matix 1 row as n and column as m:"
    n1 = int(input("n1: "))
    m1 = int(input("m1: "))
    print"Enter size of matix 2 row as n and column as m:"
    n2 = int(input("n2: "))
    m2 = int(input("m2: "))
    print"Enter size of matix 3 row as n and column as m:"
    n3 = int(input("n3: "))
    m3 = int(input("m3: "))

    if m1 != n2 & m2 != n3:
        print"cannot multiply"
        return
    print "enter matrix 1"
    mat1 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m1)] for j in range(n1)]
    print "enter matrix 2"
    mat2 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m2)] for j in range(n2)]
    print "enter matrix 3"
    mat3 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m3)] for j in range(n3)]

    cobj = cal()
    cobj.x = mat1
    cobj.y = mat2
    cobj.z = mat3
    serial = pickle.dumps(cobj)
    print "The matrices are:", "\n", mat1, "\n", mat2, "\n", mat3
    connection.send("mat " + serial)
    return


def get_matrix_mul(connection):
    connection.send("getmat" + '')
    A = connection.recv(Buffer_Size)
    B = pickle.loads(A)
    print "\nThe result of matrix Multiplication: ","\n", B
    return


def client_option():
    link = get_socket()

    while True:
        menu = raw_input("Enter your choices from 1 to 9: \n 1.add, \n 2.get_add_value, \n 3.calculate_pi, \n 4.get pi- value, \n 5.sort, \n 6.get_sorted_array, \n 7.matrix_multiply, \n 8.get_matrix_mul_value, \n 9.exit: ")

        if menu == "1":
            x = raw_input("Enter First Number:  ")
            y = raw_input("Enter Second Number:  ")
            add(x, y, link)

        elif menu == "2":
            get_add(link)

        elif menu == "3":
            calculate_pi(link)

        elif menu == "4":
            get_pi(link)

        elif menu == "5":
            sort(link)

        elif menu == "6":
            get_sort(link)

        elif menu == "7":
            matrix_multiplication(link)

        elif menu == "8":
            get_matrix_mul(link)

        elif menu == "9":
            link.send("exit ")
            break

        else:
            print "Invalid choices, choose again"
    print "Closing connection..."

    link.close()


client_option()