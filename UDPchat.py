import socket
import threading
import sys
import os
import time
import queue
from datetime import datetime
from queue import Queue


def send_messages(name, sock: socket, host, port, messages, q):
    counter = 0
    while True:

        data = input('{}: '.format(name))
        if data == "qqq":
            break
        elif data == "":
            continue

        if q.empty() == False:
            counter = q.get()

        now = datetime.now()
        data = name + ': ' + data + '/' + str(counter) + '/' + str(now)
        sock.sendto(data.encode('utf-8'), (host, port))
        mes = (counter, data, str(now))
        messages.append(mes)
        print_chat(messages)
        counter += 1


def recieve_messages(sock: socket, host, port, messages, q):
    templist = list()
    while True:
        try:
            data, addr = sock.recvfrom(1024)

            if data:
                message = data.decode('utf-8')
                if message[0] == '/':
                    print("Some messages were lost")
                    message = message.replace('/', '')
                    lost_message = messages[message]
                    sock.sendto(lost_message[1].encode('utf-8'), (host, port))

                templist = message.split('/')
                temp = templist[1]
                now = str(templist[2])
                mess = (temp, message, now)
                messages.append(mess)
                print_chat(messages)
                counter = int(templist[1]) + 1
                if q.empty() == False:
                    q.get()
                q.put(counter)
            else:
                print("The connection was lost")
        except:
            pass


def print_chat(messages):
    clear = lambda: os.system('clear')
    clear()
    messages.sort(key=lambda tup: tup[2])
    for a in messages:
        temp_content = a[1].split('/')
        print(temp_content[0])


def check_messages(messages, sock, host, port):
    while True:
        time.sleep(1)
        length = len(messages)
        a = 0
        temp = ()
        while a < length:
            temp = messages[a]
            if a == int(temp[0]):
                continue
            else:
                print("Some messages were lost")
                data = '/' + str(counter)
                sock.sendto(data.encode('utf-8'), (host, port))

            a += 1


if __name__ == '__main__':
    messages = []
    counter = 0
    queue = Queue()
    if len(sys.argv) == 4:
        host = sys.argv[1]
        port = int(sys.argv[2])
        port2 = int(sys.argv[3])
        print("Trying to connect to {}:{}...".format(host, port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        print('Successfully connected to {}:{}....'.format(host, port))
        print()
        name = input('Your name: ')
        print()
        print("Ready to recieve messages")
        send_messages = threading.Thread(target=send_messages, args=(name, sock, host, port2, messages, queue,))
        recieve_messages = threading.Thread(target=recieve_messages, args=(sock, host, port2, messages, queue,))
        send_messages.start()
        recieve_messages.start()
        check_messages(messages, sock, host, port2)
