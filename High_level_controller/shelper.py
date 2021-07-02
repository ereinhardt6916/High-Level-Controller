import socket
import logging

class Shelper:
	def __init__(self, host, port):
		self.__host = host
		self.__port = port
		self.__sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		self.__sckt.connect((self.__host, self.__port))
		logging.info("[main]socket connected")

	def send_data(self, content):
		self.__sckt.send(content)

	def read_data(self):
		buf = self.__sckt.recv(1024)
		return buf

	def close_socket(self):
		self.__sckt.close()
		logging.info("[main]socket closed")


