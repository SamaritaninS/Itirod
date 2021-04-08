
import socket
import threading
import queue
import sys
import random
import os
import time
from datetime import datetime
from queue import Queue
from collections import OrderedDict

def message_send(name, sock:socket, host, port2, order, q):

	index = 0
	while True:
		if not bool(order) == False:
			index_list = list(order.keys())
			index = (index_list[-1])
			index += 1

		message = input('{}: '.format(name))
		data = name + ':' + message

		sock.sendto(data.encode('utf-8'),(host, port2))
		print(data)
		order[index] = message
		index += 1

def message_recieve(sock:socket, host, port, symbol, order, q):

	while True:
		try:
			data,addr = sock.recvfrom(1024)
			index_list = list(order.keys())
			index = int(index_list[-1])
			message = data.decode('utf-8')
			#print(message)
			if data:

				if message[0] == symbol:
					print(message)
					get_chat_history(sock, host, port2)

				elif ':' not in message:
					temp_list = message.split('/')
					mess = order[int(temp_list[0])]
					sock.secondto(mess.encode('utf-8'), addr)

				else:
					index += 1
					order[index] = message
					print(message)
					continue_chat(sock, host, port, order)


			else:
				print("The connection was lost")
			
		except:
			pass


def continue_chat(sock, host, port, order):
	if(message_check(order, sock, host, port)):
		for x in order.keys():
			print(order[x])


def message_check(order, sock, host, port):
	id_list = []
	for a in order.keys():
		id_list.add(a)

	if id_list.length() > 1:
		if id_list[-1] - id_list[-2] != 1:
			print("The message was lost")
			message = str(id_list[-1]) + '/' + 'Messages were lost'
			sock.sendto(message.encode('utf-8'), (host, port))
			return False
		else:
			return True

	else:
		return True

def get_chat_history(sock, host, port):
	for x in order.keys():
		mess = order[x]
		sock.sendto(mess.encode('utf-8'), (host, port))


if __name__ == '__main__':
	messages = []
	counter = 0
	symbol = '@'
	queue = Queue()
	order = OrderedDict()
	print("Input the host you want to connect")
	host = input()
	print("Input your port")
	port = int(input())
	print("Input port you want to connect")
	port2 = int(input())

	print("Trying to connect to {}:{}...".format(host, port))
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind((host, port))
	print('Successfully connected to {}:{}....'.format(host, port))
	print()
	name = input('Your name: ')
	print()
	print("Ready to recieve messages")
	message = symbol + "Successfully connected"
	sock.sendto(message.encode('utf-8'), (host, port2))
	message_send = threading.Thread(target=message_send, args=(name, sock, host, port2, order, queue,  ))
	message_recieve = threading.Thread(target=message_recieve, args=(sock, host, port2, symbol, order, queue, ))
	message_send.start()
	message_recieve.start()






