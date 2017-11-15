import sublime
import sublime_plugin
from .script_manager import ScriptManager
from .steep_server import Server, Client, Disconnect

_connection = None
_scripts = ScriptManager()
_disconnect = None

class SteepConnectCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		global _connection, _scripts, _disconnect
		if self.is_enabled():
			_scripts.clear()
			sublime.run_command("new_window")
			window = sublime.active_window()
			server = Server(_scripts, window)
			client = Client(_scripts, window)
			_connection = (server, client, window)
			_connection[0].start()
			_connection[1].start()
	
	def is_enabled(self):
		global _connection, _disconnect
		return _connection == None and _disconnect == None
		
class SteepDisconnectCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		global _connection, _disconnect
		if self.is_enabled():
			_disconnect = Disconnect(_connection[0], _connection[1], _scripts)
			_disconnect.start()
	
	def is_enabled(self):
		global _connection, _disconnect
		return _connection != None and _disconnect == None

class SteepFinalizeDisconnectCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		global _connection, _disconnect
		_connection[2].run_command("close_window")
		_connection = None
		_disconnect = None
	
	def is_visible(self):
		return False
		
class SteepLoadCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection
		if self.is_enabled():
			_connection[1].get()
	
	def is_enabled(self):
		global _connection
		return _connection != None and _connection[2] == self.window
		
class SteepSaveCommand(sublime_plugin.WindowCommand):
	def run(self):
		global _connection
		if self.is_enabled():
			_connection[1].save()
	
	def is_enabled(self):
		global _connection
		return _connection != None and _connection[2] == self.window

class SteepLoadScriptCommand(sublime_plugin.TextCommand):
	def run(self, edit, tid = None, name = None, value = None):
		global _scripts
		if self.is_enabled():
			if value == None:
				self.view.replace(edit, sublime.Region(0, self.view.size()), _scripts[self.view.id()][2])
				self.view.sel().clear()
	
	def is_enabled(self):
		global _connection, _scripts
		return _connection != None and self.view.id() in _scripts
