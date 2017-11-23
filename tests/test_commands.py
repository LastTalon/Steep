import sublime
import unittest
from Steep import steep

class TestCommands(unittest.TestCase):
	def setUp(self):
		settings = sublime.load_settings("Preferences.sublime-settings")
		settings.set("close_windows_when_empty", False)
	
	def test_load(self):
		dummy = steep.SteepLoadCommand(sublime.active_window())
		
		self.assertFalse(dummy.is_enabled())
		
		sublime.run_command("steep_connect")
		dummy2 = steep.SteepLoadCommand(steep._connection[2])
		
		self.assertFalse(dummy.is_enabled())
		self.assertTrue(dummy2.is_enabled())
		
		steep._connection[2].run_command("is_enabled")
		
		self.assertFalse(dummy.is_enabled())
		self.assertTrue(dummy2.is_enabled())
		
		sublime.run_command("steep_disconnect")
	
	def test_save(self):
		pass
	
	def test_load_script(self):
		pass
