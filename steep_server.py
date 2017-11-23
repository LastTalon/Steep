import sublime
import sublime_plugin
import threading
import socket
import json
from time import sleep
from queue import Queue, Empty
from .script_manager import ScriptManager

def _update_script(script, scripts, view):
	scripts.set(view.id(), script["guid"], script["name"], script["script"].replace("\r", ""))
	view.set_name(script["guid"] + " - " + script["name"])
	view.run_command("steep_load_script")

def _create_script(script, scripts, window):
	view = window.new_file()
	view.set_scratch(True)
	view.set_syntax_file("Packages/Lua/Lua.tmLanguage")
	_update_script(script, scripts, view)

def _update_scripts(message, scripts, window, purge = False):
	if purge:
		for i in scripts:
			for j in message["scriptStates"]:
				if scripts[i][0] == j["guid"]:
					break
			else:
				del scripts[i]
	for i in message["scriptStates"]:
		id = scripts.get_tid(i["guid"])
		if id is not None:
			for j in window.views():
				if j.id() == id:
					_update_script(i, scripts, j)
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
				if serverSocket is None:
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
				if serverSocket is not None and (error or self._exit.is_set()):
					serverSocket.close()
					serverSocket = None
					error = False
				if connection is not None:
					connection.close()
					connection = None
				for i in sublime.windows():
					if i is self._window:
						break
				else:
					sublime.run_command("steep_disconnect")
	
	def _read_data(self, connection):
		with connection.makefile("r") as f:
			try:
				message = json.load(f)
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
	def __init__(self, scripts, window):
		super().__init__()
		self._scripts = scripts
		self._window = window
		self._exit = threading.Event()
		self._queue = Queue()
	
	def run(self):
		while not self._exit.is_set():
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
			sleep(0.5)
	
	def _open_socket(self):
		connection = socket.socket()
		connection.settimeout(1)
		try:
			connection.connect(("127.0.0.1", 39999))
		except socket.timeout:
			pass
		except OSError:
			pass
		else:
			return connection
		connection.close()
		return None
	
	def _send_get(self):
		message = dict()
		message["messageID"] = 0
		
		try:
			clientSocket = self._open_socket()
			if clientSocket is not None:
				self._send_data(clientSocket, message)
				message = self._read_data(clientSocket)
				
				if message is not None and message["messageID"] == 0:
					_update_scripts(message, self._scripts, self._window, True)
		finally:
			if clientSocket is not None:
				clientSocket.close()
	
	def _send_save(self):
		message = dict()
		message["messageID"] = 1
		message["scriptStates"] = list()
		for i in self._window.views():
			if i.id() in self._scripts:
				script = dict()
				script["guid"] = self._scripts[i.id()][0]
				script["script"] = i.substr(sublime.Region(0, i.size()))
				message["scriptStates"].append(script)
		
		try:
			clientSocket = self._open_socket()
			if clientSocket is not None:
				self._send_data(clientSocket, message)
		finally:
			if clientSocket is not None:
				clientSocket.close()
	
	def _send_data(self, connection, message):
		with connection.makefile("w") as stream:
			try:
				json.dump(message, stream)
			except connection.timeout:
				pass
	
	def _read_data(self, connection):
		with connection.makefile("r") as stream:
			try:
				message = json.load(stream)
			except connection.timeout:
				pass
			else:
				return message
		return None
	
	def get(self):
		self._queue.put(0, False)
	
	def save(self):
		self._queue.put(1, False)
	
	def exit_thread(self):
		self._exit.set()

class Disconnect(threading.Thread):
	def __init__(self, server, client, scripts):
		super().__init__()
		self._server = server
		self._client = client
		self._scripts = scripts
		self._disconnected = False
		self._cancel = False
	
	def run(self):
		self._client.exit_thread()
		self._server.exit_thread()
		self._client.join()
		self._server.join()
		if not self._cancel:
			self._scripts.clear()
			sublime.run_command("steep_finalize_disconnect")
	
	def cancel_finalize(self):
		self._cancel = True
