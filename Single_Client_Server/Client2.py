import os
import socket

HOST = "127.0.0.1"
PORT = 8080
Buffer_Size = 1024

#Client_Directory =/home/zahid/Server Client Project/Client2/  #For linux
#Client_Directory = "F:\ALL THESIS\Server Client Project\Client2"  #For windows


# Function for Connecting with server

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to port %s and server %s"%(PORT,HOST)
    s.connect((HOST, PORT))
    ack = s.recv(Buffer_Size)

    if ack == "1":
        print " got acknowledgments"
        return s


# Function for uploading file

def upload(file_name, link):
    link.send("upload " + file_name)
    file_path = Client_Directory + file_name

    if os.path.isfile(file_path):

        with open(file_path, 'rb') as f_send:
            data = f_send.read()
            link.send(data)
        link.close()

        print "File Upload Completed ", file_name

    else:
        print "File not found"

    link.close()
    return


# Function for downloading file

def download(file_name, link):
    link.send("download " + file_name)
    message = link.recv(Buffer_Size)
    file_path = Client_Directory + file_name

    if message == "do":

        with open(file_path, 'wb') as f_write:

            while True:
                print "receiving data.."
                data = link.recv(Buffer_Size)

                if not data:
                    break
                f_write.write(data)
            f_write.close()
        print "File Download completed"

    else:
        print "Error in Download"

    link.close()
    return


# Function for renaming file

def rename(prev_name, current_name, link):
    link.send("rename " + prev_name + " " + current_name)
    success = link.recv(Buffer_Size)
    print "Server Message: ", success
    link.close()
    return

# Function for deleting file


def delete(file_name, link):
    link.send("delete " + file_name)
    message = link.recv(Buffer_Size)
    print "Server Message: ", message
    link.close()
    return


# Main function for Client to operate

def client_option():
    while True:
        link = get_socket()
        menu = raw_input("Enter your choices from 1 to 5 (integer): \n 1.upload, \n 2.download, \n 3.rename, \n 4.delete, \n 5.exit: ")

        if menu == "1":
            file_name = raw_input("Enter File name to upload: ")
            upload(file_name, link)

        elif menu == "2":
            file_name = raw_input("File name to download: ")
            download(file_name, link)

        elif menu == "3":
            prev_name = raw_input("Previous name of File: ")
            new_name = raw_input("New name of File: ")
            rename(prev_name, new_name, link)

        elif menu == "4":
            file_name = raw_input("File name to delete: ")
            delete(file_name, link)

        elif menu == "5":
            link.send("exit ")
            break

        else:
            print "Invalid choices, choose again"
    print "Closing link..."

    link.close()


client_option()