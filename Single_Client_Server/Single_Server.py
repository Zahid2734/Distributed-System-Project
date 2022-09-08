import os
import socket

#Server_Directory =/home/zahid/Server Client Project/Single_Client_Server/  #For linux
# Server_Directory = "F:\ALL THESIS\Server Client Project\Single_Client_Server" #For windows
Buffer_Size = 1024

# Function for uploading file

def upload(filename, link, addrs):
    print "[" + str(addrs) + "] Uploading File..."
    file_path = Server_Directory + filename

    with open(file_path, 'wb') as f_write:

        while True:
            data = link.recv(1024)

            if not data:
                break
            f_write.write(data)
        f_write.close()
    print "[" + str(addrs) + "] File Upload Completed: ", filename
    link.close()
    return

# Function for downloading file

def download(file_name, link, addrs):
    file_name = Server_Directory + file_name
    print "Downloading file..."

    if os.path.isfile(file_name):
        link.send("do")

        with open(file_name, 'rb') as f_send:
            data = f_send.read()
            link.send(data)
        print "[" + str(addrs) + "] File download completed"

    else:
        print "[" + str(addrs) + "] File not exists"
    return

# Function for renaming file

def rename(prev_name, current_name, link, addrs):
    print "[" + str(addrs) + "] Renaming file..."
    prev_name = Server_Directory + prev_name
    current_name = Server_Directory + current_name

    if not os.path.isfile(prev_name):
        print "[" + str(addrs) + "] File not found"
        link.send("File not found")

    else:
        os.rename(prev_name, current_name)
        print "[" + str(addrs) + "] File rename completed: " + prev_name + " ->" + current_name
        link.send("rename completed")
    return

# Function for deleting file

def delete(file_name, link, addrs):
    print "[" + str(addrs) + "] File Deletion operation.."
    file_path = Server_Directory + file_name

    if os.path.isfile(file_path):
        os.remove(file_path)
        print "[" + str(addrs) + "] File delete completed"
        link.send("Delete completed")

    else:
        print "[" + str(addrs) + "] File not found"
        link.send("File not found")
    return




def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Server port %s and host %s" % (PORT, HOST)
    s_socket.bind((HOST, PORT))
    s_socket.listen(3)

    while True:
        print "waiting for client..."
        link, addrs = s_socket.accept()
        print "Got link from ", addrs
        print "Sending acknowledgment.."
        link.send("1")
        input = link.recv(1024)
        Client_msg = input.split(' ')

        if Client_msg[0] == "upload":
            upload(Client_msg[1], link, addrs)

        elif Client_msg[0] == "download":
            download(Client_msg[1], link, addrs)

        elif Client_msg[0] == "rename":
            rename(Client_msg[1], Client_msg[2], link, addrs)

        elif Client_msg[0] == "delete":
            delete(Client_msg[1], link, addrs)

        elif Client_msg[0] == "exit":
            pass
        link.close()
        print "[" + str(addrs) + "]" + " Connection closed"



if __name__ == '__main__':
    main()

