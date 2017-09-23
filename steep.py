import sublime
import sublime_plugin
from .script_manager import ScriptManager
from .steep_server import Server, Client


_connection = None
_scripts = ScriptManager()

class SteepConnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection, _scripts
		_scripts.clear()
		server = Server(_scripts, self.window)
		client = Client(_scripts, self.window, server)
		_connection = (server, client, self.window)
		_connection[0].start()
		_connection[1].start()
	
	def is_enabled(self):
		global _connection
		return _connection == None
		
class SteepDisconnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection, _scripts
		if _connection != None:
			_connection[1].exit_thread()
			_connection[0].exit_thread()
			_connection[1].join()
			_connection[0].join()
			_scripts.clear()
			_connection = None
	
	def is_enabled(self):
		global _connection
		return _connection != None
		
class SteepLoadCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection
		if _connection != None and _connection[2] == self.window:
			_connection[1].get()
	
	def is_enabled(self):
		global _connection
		return _connection != None and _connection[2] == self.window
		
class SteepSaveCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection
		if _connection != None and _connection[2] == self.window:
			_connection[1].save()
	
	def is_enabled(self):
		global _connection
		return _connection != None and _connection[2] == self.window

class SteepLoadScriptCommand(sublime_plugin.TextCommand):
	def run(self, edit, tid = None, name = None, value = None):
		global _connection, _scripts
		if _connection != None:
			if value == None:
				if self.view.id() in _scripts:
					self.view.replace(edit, sublime.Region(0, self.view.size()), _scripts[self.view.id()][2])
					self.view.sel().clear()
	
	def is_enabled(self):
		global _connection, _scripts
		return _connection != None and self.view.id() in _scripts

# TODO: Add event listener
