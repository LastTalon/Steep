import sublime
import sublime_plugin
import threading
import socket
import json
from time import sleep
from queue import Queue, Empty
from .script_manager import ScriptManager

def _create_script(script, scripts, window):
	view = window.new_file()
	scripts.set(view.id(), script["guid"], script["name"], script["script"].replace("\r", ""))
	view.set_scratch(True)
	view.set_name(script["guid"] + " - " + script["name"])
	view.set_syntax_file("Packages/Lua/Lua.tmLanguage")
	view.run_command("steep_load_script")

def _update_scripts(message, scripts, window, purge = False):
	if purge:
		scripts.clear()
	for i in message["scriptStates"]:
		id = scripts.get_tid(i["guid"])
		if id != None:
			scripts.set(id, i["guid"], i["name"], i["script"].replace("\r", ""))
			for j in window.views():
				if j.id() == id:
					j.set_name(i["guid"] + " - " + i["name"])
					j.run_command("steep_load_script")
					break
			else:
				del scripts[id]
				_create_script(i, scripts, window)
		else:
			_create_script(i, scripts, window)
	if purge:
		for i in window.views():
			for j in scripts:
				if i.id() == j:
					break
			else:
				i.close()


class Server(threading.Thread):
	def __init__(self, scripts, window):
		super().__init__()
		self._scripts = scripts
		self._window = window
		self._exit = threading.Event()
	
	def run(self):
		serverSocket = None
		connection = None
		address = None
		error = False
		
		while not self._exit.is_set():
			try:
				if serverSocket == None:
					serverSocket = socket.socket()
					serverSocket.settimeout(1)
					serverSocket.bind(("127.0.0.1", 39998))
					serverSocket.listen(1)
				connection, address = serverSocket.accept()
			except socket.timeout:
				pass
			except OSError:
				error = True
				sleep(0.5)
			else:
				self._read_data(connection)
			finally:
				if serverSocket != None and (error or self._exit.is_set()):
					serverSocket.close()
					serverSocket = None
				if connection != None:
					connection.close()
					connection = None
	
	def _read_data(self, connection):
		with connection.makefile("r") as f:
			try:
				message = json.load(f)
				# print("Loaded")
				# print("Server:", connection.recv(4096))
				# sleep(.5)
			except socket.timeout:
				pass
			else:
				if message["messageID"] == 0:
					_update_scripts(message, self._scripts, self._window)
				elif message["messageID"] == 1:
					_update_scripts(message, self._scripts, self._window, True)
				elif message["messageID"] == 2:
					pass
				elif message["messageID"] == 3:
					pass
	
	def exit_thread(self):
		self._exit.set()


class Client(threading.Thread):
	def __init__(self, scripts, window, server):
		super().__init__()
		self._scripts = scripts
		self._window = window
		self._server = server
		self._exit = threading.Event()
		self._queue = Queue()
		self._socket = socket.socket()
		self._timeouts = 0
		self._continuing = False
	
	def run(self):
		while not self._exit.is_set():
			self._socket.settimeout(1)
			self._timeouts = 0
			try:
				self._socket.connect(("127.0.0.1", 39999))
			except socket.timeout:
				pass
			except OSError:
				sleep(1)
			else:
				while not self._exit.is_set() and self._timeouts < 10:
					while not self._queue.empty():
						try:
							command = self._queue.get(False)
						except Empty:
							pass
						else:
							if command == 0:
								self._send_get()
							elif command == 1:
								self._send_save()
					self._read_data()
			finally:
				self._socket.close()
				self._socket = socket.socket()
	
	def _send_get(self):
		message = dict()
		message["messageID"] = 0
		
		with self._socket.makefile("w") as f:
			try:
				json.dump(message, f)
				self._timouts = 0
			except socket.timeout:
				self._timouts += 1
				self._queue.put(0, False)
	
	def _send_save(self):
		message = dict()
		message["messageID"] = 1
		message["scriptStates"] = list()
		for i in self._window.views():
			if i.id() in self._scripts:
				script = dict()
				script["guid"] = self._scripts[i][0]
				script["script"] = i.substr(sublime.Region(0, i.size()))
				message["scriptStates"].append(script)
		
		with self._socket.makefile("w") as f:
			try:
				json.dump(message, f)
				self._timouts = 0
			except socket.timeout:
				self._queue.put(1, False)
				self._timouts += 1
	
	def _read_data(self):
		with self._socket.makefile("r") as f:
			try:
				# TODO: Sends one message at a time then closes stream...
				# message = json.load(f)
				# print("Loaded")
				print("Client:", self._socket.recv(4096))
				sleep(.5)
			except socket.timeout:
				pass
			# else:
			# 	self._timouts = 0
			# 	if message["messageID"] == 0:
			# 		_update_scripts(message, self._scripts, self._window)
			# 		for i in self._scripts:
			# 			for j in self._window.views():
			# 				if i == j.id():
			# 					break
			# 			else:
			# 				del self._scripts[i]
	
	def get(self):
		self._queue.put(0, False)
	
	def save(self):
		self._queue.put(1, False)
	
	def exit_thread(self):
		self._exit.set()
